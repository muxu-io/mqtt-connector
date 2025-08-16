# This file marks the directory as a Python package.
# It can be used to define what is exported when the package is imported.

from .connector import MqttConnector

__version__ = "0.1.0"
__author__ = "Alex Gonzalez"
__email__ = "alex@muxu.io"
__description__ = "Low-level MQTT connection management"
__license__ = "MIT"

__all__ = ["MqttConnector", "__version__"]
