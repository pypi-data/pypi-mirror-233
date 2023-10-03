"""Initialize MQTT subscribe and publish for Home Assistant sensors."""

import asyncio
import json
from asyncio import Task
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import TYPE_CHECKING
from typing import Tuple
from typing import Union

from aiomqtt import Client

from unipi_control.config import UNIPI_LOGGER
from unipi_control.features.extensions import EastronMeter
from unipi_control.helpers.log import LOG_MQTT_PUBLISH
from unipi_control.helpers.text import slugify
from unipi_control.mqtt.discovery.mixin import HassDiscoveryMixin
from unipi_control.neuron import Neuron

if TYPE_CHECKING:
    from unipi_control.helpers.typing import HardwareDefinition


class HassSensorsDiscovery(HassDiscoveryMixin):
    """Provide the sensors (e.g. meter) as Home Assistant MQTT discovery."""

    publish_feature_types: ClassVar[List[str]] = ["METER"]

    def _get_via_device(self, feature: EastronMeter) -> Optional[str]:
        if (device_name := self.config.device_info.name) != self._get_device_name(feature):
            return device_name

        return None

    def _get_device_name(self, feature: EastronMeter) -> str:
        suggested_area: Optional[str] = feature.hardware.definition.suggested_area
        device_name: str = self.config.device_info.name
        definition: HardwareDefinition = feature.hardware.definition

        if definition.device_name:
            device_name = definition.device_name

        if suggested_area:
            device_name = f"{device_name} - {suggested_area}"

        return device_name

    def get_discovery(self, feature: Union[EastronMeter]) -> Tuple[str, Dict[str, Any]]:
        """Get Mqtt topic and message for publish with mqtt.

        Parameters
        ----------
        feature:
            All meter features.

        Returns
        -------
        tuple:
            Return mqtt topic and message as tuple.
        """
        topic: str = (
            f"{self.config.homeassistant.discovery_prefix}/sensor"
            f"/{slugify(self.config.device_info.name)}"
            f"/{feature.object_id}/config"
        )

        device_name: str = self._get_device_name(feature)

        message: Dict[str, Any] = {
            "name": feature.friendly_name,
            "unique_id": feature.unique_id,
            "state_topic": f"{feature.topic}/get",
            "qos": 2,
            "force_update": True,
            "device": {
                "name": device_name,
                "identifiers": slugify(device_name),
                "model": self._get_device_model(feature),
                "sw_version": "" if feature.sw_version is None else str(feature.sw_version),
                "manufacturer": self._get_device_manufacturer(feature),
            },
        }

        if feature.object_id:
            message["object_id"] = feature.object_id

        if feature.icon:
            message["icon"] = feature.icon

        if feature.device_class:
            message["device_class"] = feature.device_class

        if feature.state_class:
            message["state_class"] = feature.state_class

        if feature.unit_of_measurement:
            message["unit_of_measurement"] = feature.unit_of_measurement

        if feature.hardware.definition.suggested_area:
            message["device"]["suggested_area"] = feature.hardware.definition.suggested_area

        if via_device := self._get_via_device(feature):
            message["device"]["via_device"] = via_device

        return topic, message

    async def publish(self) -> None:
        """Publish MQTT Home Assistant discovery topics for sensors."""
        for feature in self.neuron.features.by_feature_types(self.publish_feature_types):
            if isinstance(feature, EastronMeter):
                topic, message = self.get_discovery(feature)
                json_data: str = json.dumps(message)
                await self.mqtt_client.publish(topic=topic, payload=json_data, qos=2, retain=True)
                UNIPI_LOGGER.debug(LOG_MQTT_PUBLISH, topic, json_data)


class HassSensorsMqttPlugin:
    """Provide Home Assistant MQTT commands for sensors."""

    def __init__(self, neuron: Neuron, mqtt_client: Client) -> None:
        self.hass = HassSensorsDiscovery(neuron, mqtt_client)

    async def init_tasks(self, tasks: Set[Task]) -> None:
        """Initialize MQTT tasks for publish MQTT topics.

        Parameters
        ----------
        tasks: set
            A set of all MQTT tasks.
        """
        task: Task = asyncio.create_task(self.hass.publish())
        tasks.add(task)
