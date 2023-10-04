from __future__ import annotations

import aiohttp
import asyncio
import os
import resemble.aio.signals as signals
import resemble.templates.tools as template_tools
import signal
import socket
import subprocess
import tempfile
import threading
from resemble.aio.servicers import Serviceable
from resemble.aio.types import ServiceName
from resemble.helpers import (
    add_file_descriptor_to_file_descriptor_set,
    base64_serialize_proto_descriptor_set,
    generate_proto_descriptor_set,
)
from resemble.settings import ENVOY_PROXY_IMAGE
from resemble.v1alpha1 import react_pb2
from typing import Optional


class LocalEnvoy:
    """Wrapper class for setting up a local Envoy outside of Kubernetes. This
    runs Envoy in a Docker container, not in process.

    The user of this class is responsible for calling .start() and .stop().

    Args:
        - proxied_server_host: the host address of the server Envoy proxies to.
        - proxied_server_port: the port address of the server Envoy proxies to.
        - servicers: the servicers to proxy.
        - envoy_port: (optional) the Envoy proxy's port.
    Sample use:
        envoy = LocalEnvoy(
            proxied_server_host='127.0.0.1',
            proxied_server_port=5001,
            servicers=[MyGreeterServicer]
        )
        await envoy.start()
        await envoy.stop()
    """

    # LocalEnvoy needs to know something about Resemble servicers in the
    # current implementation.
    # TODO: create a generic abstraction, e.g. LocalEnvoyBase, that doesn't
    # know anything about Resemble.
    def __init__(
        self,
        *,
        proxied_server_host: str,
        proxied_server_port: int,
        serviceables: list[Serviceable],
        envoy_port: Optional[int] = None
    ):
        self._envoy_host: Optional[str] = None
        self._envoy_port: Optional[int] = envoy_port
        self._container_id: Optional[str] = None

        proto_descriptor_set = generate_proto_descriptor_set(serviceables)

        # We also add the 'React' service so our react specific
        # generated code can make calls into the server.
        add_file_descriptor_to_file_descriptor_set(
            proto_descriptor_set,
            react_pb2.DESCRIPTOR.services_by_name['React'].file
        )

        base64_encoded_proto_desc_set = base64_serialize_proto_descriptor_set(
            proto_descriptor_set
        )

        service_names = [s.service_name() for s in serviceables]

        # Also need 'React' service name.
        service_names.append('resemble.v1alpha1.React')

        # Generate envoy config and write it to a temporary file that gets
        # cleaned up on .stop().
        self._tmp_envoy_yaml_dir = tempfile.TemporaryDirectory()
        self._tmp_envoy_file_name = f'{self._tmp_envoy_yaml_dir.name}/envoy.yaml'

        with open(self._tmp_envoy_file_name, 'w') as tmp_envoy_file:
            path_to_template = os.path.join(
                os.path.dirname(__file__), 'local_envoy_config.yaml.j2'
            )
            yaml = self._generate_envoy_transcoding_yaml(
                proxied_server_host=proxied_server_host,
                proxied_server_port=proxied_server_port,
                proto_descriptor_bin=base64_encoded_proto_desc_set,
                template_path=path_to_template,
                service_names=service_names,
                envoy_port=self._envoy_port or 0
            )
            tmp_envoy_file.write(yaml)

        # Open a server socket that listens for connections from the
        # 'local_envoy_nanny' so that in the event our process is
        # killed abruptly the nanny will get an EOF (or error) and
        # send a SIGTERM to envoy which should stop the container.
        self._nanny_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._nanny_socket.bind(('127.0.0.1', 0))

        # Indicator of whether or not we are stopping. Used at the
        # least by the nanny server thread to avoid spamming stderr
        # with exceptions when the server socket gets closed.
        self._stopping = False

    def admin_endpoint(self, route: str = '') -> str:
        """Returns the URI of the Envoy admin endpoint.
        """
        if self._envoy_host is None or self._envoy_admin_port is None:
            raise ValueError(
                'LocalEnvoy .start() must be called before' \
                '.admin_endpoint() can be called'
            )
        return f'http://{self._envoy_host}:{self._envoy_admin_port}{route}'

    @property
    def port(self) -> int:
        """Returns the port of the Envoy proxy.
        """
        if self._envoy_host is None or self._envoy_port is None:
            raise ValueError(
                'LocalEnvoy.start() must be called before you can get the port'
            )
        return self._envoy_port

    async def start(self) -> None:
        """Starts Envoy in a container on an unused port. The port started on
        is retrieved and saved.
        """

        # There is a race between when we've sucessfully started the
        # Envoy container and when we get the nanny started where a
        # container may get orphaned if our process gets terminated or
        # our coroutine is cancelled.
        #
        # We minimize the likelyhood of an orphaned container here by
        # registering a cleanup handler to be executed when a SIGINT
        # or SIGTERM signal is raised that will stop the container (if
        # it was started).
        def stop_on_sigint_sigterm():
            if self._container_id is not None:
                subprocess.run(
                    ['docker', 'stop', self._container_id],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

        with signals.cleanup_on_raise(
            [signal.SIGINT, signal.SIGTERM], stop_on_sigint_sigterm
        ):
            # Shell out to docker to start envoy and return a container id.
            self._container_id = await LocalEnvoy._docker_run_envoy(
                self._tmp_envoy_file_name
            )

            # Now 'docker exec' the local envoy nanny inside the
            # container we just started with envoy.
            await self._exec_local_envoy_nanny()

        # Wait for admin endpoint to start and log its host and port.
        self._envoy_host, self._envoy_admin_port = await self._envoy_admin_address_and_port_from_docker_logs(
        )

        # If we specify port 0 in the config then envoy chooses which
        # free port to start on. The admin endpoint, `/listeners`,
        # returns the port.
        #
        # If we specify the port ourselves than we want to validate
        # that it came up on that port.
        #
        # TODO: Allow this to work on more than one listener. Currently, we
        # only return the last one, which is the correct one if there is only
        # one listener.
        # TODO: Once the above TODO is complete, consider allowing users to
        # pass in their own envoy.yaml template.
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.admin_endpoint('/listeners')
            ) as response:
                response_text = await response.text()
                envoy_port = int(response_text.split(":")[-1].strip())
                if self._envoy_port is None or self._envoy_port == 0:
                    self._envoy_port = envoy_port
                else:
                    # Invariant is that if we were given a non-zero
                    # port that is what envoy came up on!
                    assert self._envoy_port == envoy_port

    async def stop(self) -> None:
        """Stop the Envoy container and cleans up temp files.
        """
        self._stopping = True

        if self._container_id is None:
            raise RuntimeError('.start() must be called before .stop()')

        try:
            docker_stop = await asyncio.create_subprocess_exec(
                'docker', 'stop', self._container_id
            )
            await docker_stop.wait()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f'LocalEnvoy .stop() failed with: {str(e)}; '
                'this likely means that .start() was unsuccessful'
            ) from e
        finally:
            self._tmp_envoy_yaml_dir.cleanup()
            self._nanny_socket.close()

    @staticmethod
    async def _async_check_output(*args, **kwargs) -> str:
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            **kwargs
        )

        stdout_data, _ = await process.communicate()
        return stdout_data.decode()

    async def _envoy_admin_address_and_port_from_docker_logs(
        self
    ) -> tuple[str, int]:
        """The logs are the only place currently known to retrieve Envoy's admin
        endpoint. The admin endpoint is required to interrogate which free port
        the Envoy proxy started on.

        This method reads the log output from docker to return the host and port
        of the Envoy admin endpoint.
        """
        assert self._container_id is not None
        process = await asyncio.create_subprocess_exec(
            'docker',
            'logs',
            '-f',
            self._container_id,
            stderr=asyncio.subprocess.STDOUT,
            stdout=asyncio.subprocess.PIPE
        )
        # process.stdout should not be None since we set it to PIPE.
        assert process.stdout is not None

        # Reading the logs is a brittle way to access the admin address but it's
        # the only way we know. It typically takes ~50ms to read the logs for
        # this value. If it takes too long it's possible the log structure of
        # Envoy has changed.
        envoy_admin_address: Optional[tuple[str, int]] = None
        timeout_seconds = 5.0

        async def read_stdout():
            # process.stdout will not be None as long as it is set to PIPE.
            assert process.stdout is not None
            while not process.stdout.at_eof():
                yield await process.stdout.readline()

        async def find_address() -> tuple[str, int]:
            # TODO(riley): improve logging story here.
            # If this errors out, we should dump verbose logs.
            # "Envoy admin address not found" is a bit of a red herring if
            # there are no logs at all.
            async for line in read_stdout():
                # TODO: accumulate logs here.
                address_index = line.decode().find('admin address:')
                if address_index != -1:
                    # TODO: use regex here instead. This is brittle.
                    admin_address = line.rstrip().decode()[address_index +
                                                           15:address_index +
                                                           31]
                    address_and_port = admin_address.rstrip().split(':')
                    envoy_admin_address = (
                        address_and_port[0], int(address_and_port[1])
                    )
                    return envoy_admin_address
            # TODO: print accumulated logs.
            raise ValueError('Envoy admin address not found in docker logs')

        try:
            return await asyncio.wait_for(find_address(), timeout_seconds)
        except Exception as e:
            raise ValueError(
                'Envoy admin address not found in docker logs'
            ) from e
        finally:
            # Whether success or failure, we have what we need from
            # `docker logs`, stop `-f` following.
            process.kill()
            await process.wait()

    @staticmethod
    async def _docker_run_envoy(tmp_envoy_file_name: str) -> str:
        """Checks that Docker is installed and starts up Envoy in a container.
        """
        try:
            await LocalEnvoy._async_check_output('docker', '--version')
        except Exception as e:
            raise RuntimeError(
                'Docker likely not installed; install docker to use LocalEnvoy:'
                f'`docker --version` failed with {str(e)}'
            )

        # NOTE: we pass each necessary file individually than a single
        # directory that includes all of the files because symlinks in
        # dirctories are not accessible from within a Docker container
        # and at least at the time of writing this comment Bazel
        # sometimes uses symlinks for files.

        local_envoy_nanny_path = os.path.join(
            os.path.dirname(__file__), 'local_envoy_nanny'
        )
        if not os.path.isfile(local_envoy_nanny_path):
            raise FileNotFoundError(
                "Expecting 'local_envoy_nanny' executable at path "
                f"'{local_envoy_nanny_path}'"
            )

        localhost_direct_crt = os.path.join(
            os.path.dirname(__file__), 'localhost.direct.crt'
        )
        if not os.path.isfile(localhost_direct_crt):
            raise FileNotFoundError(
                "Expecting 'localhost.direct.crt' at path "
                f"'{localhost_direct_crt}'"
            )

        localhost_direct_key = os.path.join(
            os.path.dirname(__file__), 'localhost.direct.key'
        )
        if not os.path.isfile(localhost_direct_key):
            raise FileNotFoundError(
                "Expecting 'localhost.direct.key' at path "
                f"'{localhost_direct_key}'"
            )

        # TODO(riley): even if we get back a container_id, it doesn't mean
        # everything is good. Envoy may have crashed. Poll this process for
        # a non-0 exit code so we can notify the user that
        # there is likely an issue with their proto descriptor.
        container_id = await LocalEnvoy._async_check_output(
            'docker',
            'run',
            '--detach',
            '--rm',
            # NOTE: invariant here that we run the container with
            # '--net=host' so that the 'local_envoy_nanny' can connect
            # back to 'self._nanny_socket'.
            '--net=host',
            f'--volume={tmp_envoy_file_name}:/etc/envoy/envoy.yaml:ro',
            f'--volume={local_envoy_nanny_path}:/local_envoy_nanny',
            f'--volume={localhost_direct_crt}:/etc/envoy/localhost.direct.crt',
            f'--volume={localhost_direct_key}:/etc/envoy/localhost.direct.key',
            '-e',
            # Run using the current user ID. This both limits the
            # security exposure and makes it so vscode can auto port
            # forward (if we run as root then vscode doesn't have
            # sufficient permissions to see what ports it has opened).
            f'ENVOY_UID={os.getuid()}',
            '-e',
            # Run using the current group ID (same reasoning as
            # ENVOY_UID, see above for more details).
            f'ENVOY_GID={os.getgid()}',
            # NOTE: invariant here that the default entry point of the
            # container will run envoy at PID 1 because that is what
            # the 'local_envoy_nanny' will send a SIGTERM to in the
            # event of orphaning.
            ENVOY_PROXY_IMAGE,
            '-c',
            '/etc/envoy/envoy.yaml',
            # We need to disable hot restarts in order to run multiple
            # proxies at the same time otherwise they will clash
            # trying to create a domain socket. See
            # https://www.envoyproxy.io/docs/envoy/latest/operations/cli#cmdoption-base-id
            # for more details.
            '--disable-hot-restart'
        )

        return container_id.strip()

    @staticmethod
    def _generate_envoy_transcoding_yaml(
        *, proxied_server_host: str, proxied_server_port: int,
        proto_descriptor_bin: bytes, template_path: str,
        service_names: list[str], envoy_port: int
    ) -> str:
        """Takes an Envoy config Jinja template, fills its values and returns a
        yaml string.
        """

        template_input = {
            'proxied_server_host': proxied_server_host,
            'proxied_server_port': proxied_server_port,
            'services': service_names,
            # We have to turn the base64 encoded proto descriptor into a string
            # using .decode() because Jinja can only handle str types.
            'proto_descriptor_bin': proto_descriptor_bin.decode(),
            'envoy_port': envoy_port
        }

        return template_tools.render_template_path(
            template_path, template_input
        )

    async def _exec_local_envoy_nanny(self):
        # Start listening for the 'local_envoy_nanny' to connect. We
        # use a daemon thread which ignores any errors after we've
        # stopped so that we don't spam stderr with an exception.
        self._nanny_socket.listen(1)

        def accept():
            clients: list[socket.socket] = []
            try:
                while True:
                    client, address = self._nanny_socket.accept()
                    clients.append(client)
            except Exception as e:
                if not self._stopping:
                    raise RuntimeError(
                        'Failed to accept on "nanny socket; '
                        '*** ENVOY MAY BECOME AN ORPHANED CONTAINER ***'
                    ) from e

        threading.Thread(target=accept, daemon=True).start()

        host, port = self._nanny_socket.getsockname()

        # Run the nanny which will connect back to our server socket!
        #
        # NOTE: invariant here that the container is run with
        # '--net=host' so that the 'local_envoy_nanny' can connect
        # back to 'self._nanny_socket'.
        local_envoy_nanny_process = await asyncio.create_subprocess_exec(
            'docker',
            'exec',
            '--detach',
            f'{self._container_id}',
            '/local_envoy_nanny',
            f'{host}',
            f'{port}',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        if await local_envoy_nanny_process.wait() != 0:
            stdout_data, _ = await local_envoy_nanny_process.communicate()
            error = RuntimeError(
                f"Failed to run 'local_envoy_nanny': {stdout_data.decode()}"
            )
            try:
                # Try and stop the container so we don't have orphans
                # since our nanny won't be there for them!
                await self.stop()
            except Exception as e:
                raise error from e
            else:
                raise error
