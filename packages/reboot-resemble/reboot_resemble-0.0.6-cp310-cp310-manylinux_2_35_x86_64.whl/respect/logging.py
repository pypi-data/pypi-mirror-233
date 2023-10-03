import logging
import os
# Re-export the log levels, so that clients can import them from this module.
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from typing import Optional

# Create log formatter that we'll use with log handler.
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(name)s: %(message)s'
)

# Create log handler and connect it to formatter.
# Note: we set the log level of the stream handler to be as verbose as
# possible: any message passed to the handler from the logger should get
# considered by the stream handler.
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

# Create our respect logger from the root logger and connect the stream
# handler.
# Note: setting the log level is deferred to the end of this module.
logger = logging.getLogger('respect')
logger.addHandler(stream_handler)

# Create a test logger (`respect.test`) that can be used in all of our tests
# that has a default log level of DEBUG. Note, unlike the `respect` logger
# (`logger`), the log level of the test logger is not affected by the
# `RESPECT_LOGGING` environment variable.
test_logger = logger.getChild('test')
test_logger.setLevel(logging.DEBUG)


def set_log_level(log_level: int):
    """ Set the log level for the respect logger. """
    global logger
    logger.setLevel(log_level)


def get_logger(name: Optional[str] = None, parent=None):
    """ Get a named logger.

    If no name is given, return the respect logger, else return a child logger
    of the default respect logger.
    """
    global logger
    parent = parent or logger
    return logger if name is None else parent.getChild(name)


def get_test_logger(name: Optional[str] = None):
    """ Get a named test logger.

    This behaves as `get_logger` but returns a named test logger.
    """
    global test_logger
    return get_logger(name, parent=test_logger)


class DefaultLoggerMixin(object):
    """ Mixin providing class member access to the default logger.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = get_logger()


class LoggerMixin(object):
    """ Mixin providing class member access to named logger.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Name of the logger is the class name.
        self.logger = get_logger(type(self).__name__)


# Initialize the log level for the respect logger.
set_log_level(
    getattr(
        logging,
        os.environ.get('RESPECT_LOGGING', '').upper(), logging.INFO
    )
)
