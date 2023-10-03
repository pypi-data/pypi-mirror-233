import kubernetes_asyncio
import resemble.templates.tools as template_tools
from enum import Enum
from google.protobuf import struct_pb2
from resemble.aio.types import ConsensusName, ServiceName
from resemble.controller.envoy_filter import EnvoyFilter
from resemble.controller.settings import (
    ISTIO_INGRESSGATEWAY_LABEL_NAME,
    ISTIO_INGRESSGATEWAY_LABEL_VALUE,
    RESEMBLE_CONSENSUS_LABEL_NAME,
    RESEMBLE_CONSENSUS_LABEL_VALUE,
    USER_CONTAINER_PORT,
)
from resemble.v1alpha1.istio.envoy_filter_spec_pb2 import \
    EnvoyFilter as EnvoyFilterSpec
from resemble.v1alpha1.istio.envoy_filter_spec_pb2 import WorkloadSelector
from typing import Optional


def generate_lua_routing_filter(
    consensuses_by_service: dict[ServiceName, ConsensusName]
) -> str:
    """
    Generates Lua code that Envoy will accept as part of an `inline_code` block.
    NOTE: will generate this code with a base indentation of 0; you must indent it appropriately
          to make it part of valid YAML.
    """
    template_input = {
        "consensuses_by_service": consensuses_by_service,
    }
    return template_tools.render_template(
        "routing_filter.lua.j2", template_input
    )


class FilterContext(Enum):
    GATEWAY = 'gateway'
    MESH = 'mesh'


def generate_istio_routing_filter(
    namespace: str,
    name: str,
    consensuses_by_service: dict[ServiceName, ConsensusName],
    context: FilterContext,
) -> EnvoyFilter:
    """
    Generates a `EnvoyFilter` (which is a `CustomObject` representing an Istio
    `EnvoyFilter`) that contains the Lua routing filter.
    """
    lua_filter_code = generate_lua_routing_filter(consensuses_by_service)
    patch_value_struct = struct_pb2.Struct()
    patch_value_struct.update(
        {
            'name': 'envoy.filters.http.lua',
            'typed_config':
                {
                    '@type':
                        'type.googleapis.com/envoy.extensions.filters.http.lua.v3.Lua',
                    'inline_code':
                        lua_filter_code
                }
        }
    )

    match_spec: Optional[EnvoyFilterSpec.EnvoyConfigObjectMatch] = None
    selector_labels: dict[str, str] = {}
    if context == FilterContext.GATEWAY:
        # The gateway matches all traffic. We don't want to specify a listener,
        # since we don't know on what port the traffic will be coming in.
        match_spec = EnvoyFilterSpec.EnvoyConfigObjectMatch(
            context=EnvoyFilterSpec.PatchContext.GATEWAY,
        )
        # The gateway routing filter should be applied to Istio ingress
        # gateways.
        selector_labels = {
            ISTIO_INGRESSGATEWAY_LABEL_NAME: ISTIO_INGRESSGATEWAY_LABEL_VALUE,
        }
    else:
        assert context == FilterContext.MESH
        # The internal routing filter only matches traffic outbound to the user
        # container port.
        match_spec = EnvoyFilterSpec.EnvoyConfigObjectMatch(
            context=EnvoyFilterSpec.PatchContext.SIDECAR_OUTBOUND,
            listener=EnvoyFilterSpec.ListenerMatch(
                filter_chain=EnvoyFilterSpec.ListenerMatch.FilterChainMatch(
                    filter=EnvoyFilterSpec.ListenerMatch.FilterMatch(
                        name='envoy.filters.network.http_connection_manager',
                        sub_filter=EnvoyFilterSpec.ListenerMatch.
                        SubFilterMatch(name='envoy.filters.http.router'),
                    )
                ),
                port_number=USER_CONTAINER_PORT
            )
        )
        # The internal routing filter should be applied to all pods that are
        # part of a Resemble consensus.
        selector_labels = {
            RESEMBLE_CONSENSUS_LABEL_NAME: RESEMBLE_CONSENSUS_LABEL_VALUE
        }

    return EnvoyFilter(
        metadata=kubernetes_asyncio.client.V1ObjectMeta(
            namespace=namespace,
            name=name,
        ),
        spec=EnvoyFilterSpec(
            workload_selector=WorkloadSelector(
                # Deploy this EnvoyFilter to the right pods.
                labels=selector_labels
            ),
            config_patches=[
                EnvoyFilterSpec.EnvoyConfigObjectPatch(
                    apply_to=EnvoyFilterSpec.ApplyTo.HTTP_FILTER,
                    match=match_spec,
                    patch=EnvoyFilterSpec.Patch(
                        operation=EnvoyFilterSpec.Patch.Operation.INSERT_FIRST,
                        value=patch_value_struct
                    )
                )
            ]
        )
    )
