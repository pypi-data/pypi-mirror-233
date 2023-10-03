"""Unit tests MQTT for Home Assistant covers."""

import asyncio
from asyncio import Task
from typing import Any
from typing import Dict
from typing import List
from typing import Set
from unittest.mock import AsyncMock

import pytest
from _pytest.logging import LogCaptureFixture
from aiomqtt import Client

from tests.conftest_data import CONFIG_CONTENT
from tests.conftest_data import EXTENSION_HARDWARE_DATA_CONTENT
from tests.conftest_data import HARDWARE_DATA_CONTENT
from unipi_control.config import DEVICE_CLASSES
from unipi_control.integrations.covers import CoverMap
from unipi_control.mqtt.discovery.covers import HassCoversMqttPlugin
from unipi_control.neuron import Neuron


class TestHappyPathHassCoversMqttPlugin:
    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        "config_loader", [(CONFIG_CONTENT, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT)], indirect=True
    )
    async def test_init_tasks(self, neuron: Neuron, covers: CoverMap, caplog: LogCaptureFixture) -> None:
        """Test MQTT output after initialize Home Assistant covers."""
        covers.init()
        mock_mqtt_client: AsyncMock = AsyncMock(spec=Client)
        plugin: HassCoversMqttPlugin = HassCoversMqttPlugin(neuron=neuron, mqtt_client=mock_mqtt_client, covers=covers)

        tasks: Set[Task] = set()

        await plugin.init_tasks(tasks)
        await asyncio.gather(*tasks)

        for task in tasks:
            assert task.done() is True

        logs: List[str] = [record.getMessage() for record in caplog.records]

        assert (
            "[MQTT] [homeassistant/cover/mocked_unipi/mocked_blind_topic_name/config] "
            "Publishing message: {"
            '"name": "MOCKED_FRIENDLY_NAME - BLIND", '
            '"unique_id": "mocked_unipi_mocked_blind_topic_name", '
            '"object_id": "mocked_blind_topic_name", '
            '"device_class": "blind", '
            '"command_topic": "mocked_unipi/mocked_blind_topic_name/cover/blind/set", '
            '"state_topic": "mocked_unipi/mocked_blind_topic_name/cover/blind/state", '
            '"qos": 2, '
            '"optimistic": false, '
            '"device": {'
            '"name": "MOCKED UNIPI", '
            '"identifiers": "mocked_unipi", '
            '"model": "MOCKED_NAME MOCKED_MODEL", '
            '"manufacturer": "Unipi technology", '
            '"suggested_area": "MOCKED AREA"'
            "}, "
            '"position_topic": "mocked_unipi/mocked_blind_topic_name/cover/blind/position", '
            '"set_position_topic": "mocked_unipi/mocked_blind_topic_name/cover/blind/position/set", '
            '"tilt_status_topic": "mocked_unipi/mocked_blind_topic_name/cover/blind/tilt", '
            '"tilt_command_topic": "mocked_unipi/mocked_blind_topic_name/cover/blind/tilt/set"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/cover/mocked_unipi/mocked_shutter_topic_name/config] "
            "Publishing message: {"
            '"name": "MOCKED_FRIENDLY_NAME - SHUTTER", '
            '"unique_id": "mocked_unipi_mocked_shutter_topic_name", '
            '"object_id": "mocked_shutter_topic_name", '
            '"device_class": "shutter", '
            '"command_topic": "mocked_unipi/mocked_shutter_topic_name/cover/shutter/set", '
            '"state_topic": "mocked_unipi/mocked_shutter_topic_name/cover/shutter/state", '
            '"qos": 2, '
            '"optimistic": false, '
            '"device": {'
            '"name": "MOCKED UNIPI", '
            '"identifiers": "mocked_unipi", '
            '"model": "MOCKED_NAME MOCKED_MODEL", '
            '"manufacturer": "Unipi technology", '
            '"suggested_area": "MOCKED AREA"'
            "}"
            "}" in logs
        )
        assert len(logs) == 3

    @pytest.mark.parametrize(
        ("config_loader", "expected"),
        [
            (
                (CONFIG_CONTENT, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                [
                    {
                        "message": {
                            "name": "MOCKED_FRIENDLY_NAME - BLIND",
                            "unique_id": "mocked_unipi_mocked_blind_topic_name",
                            "object_id": "mocked_blind_topic_name",
                            "device_class": "blind",
                            "command_topic": "mocked_unipi/mocked_blind_topic_name/cover/blind/set",
                            "state_topic": "mocked_unipi/mocked_blind_topic_name/cover/blind/state",
                            "qos": 2,
                            "optimistic": False,
                            "device": {
                                "name": "MOCKED UNIPI",
                                "identifiers": "mocked_unipi",
                                "model": "MOCKED_NAME MOCKED_MODEL",
                                "manufacturer": "Unipi technology",
                                "suggested_area": "MOCKED AREA",
                            },
                            "position_topic": "mocked_unipi/mocked_blind_topic_name/cover/blind/position",
                            "set_position_topic": "mocked_unipi/mocked_blind_topic_name/cover/blind/position/set",
                            "tilt_status_topic": "mocked_unipi/mocked_blind_topic_name/cover/blind/tilt",
                            "tilt_command_topic": "mocked_unipi/mocked_blind_topic_name/cover/blind/tilt/set",
                        },
                        "topic": "homeassistant/cover/mocked_unipi/mocked_blind_topic_name/config",
                    },
                    {
                        "message": {
                            "name": "MOCKED_FRIENDLY_NAME - SHUTTER",
                            "unique_id": "mocked_unipi_mocked_shutter_topic_name",
                            "object_id": "mocked_shutter_topic_name",
                            "device_class": "shutter",
                            "command_topic": "mocked_unipi/mocked_shutter_topic_name/cover/shutter/set",
                            "state_topic": "mocked_unipi/mocked_shutter_topic_name/cover/shutter/state",
                            "qos": 2,
                            "optimistic": False,
                            "device": {
                                "name": "MOCKED UNIPI",
                                "identifiers": "mocked_unipi",
                                "model": "MOCKED_NAME MOCKED_MODEL",
                                "manufacturer": "Unipi technology",
                                "suggested_area": "MOCKED AREA",
                            },
                        },
                        "topic": "homeassistant/cover/mocked_unipi/mocked_shutter_topic_name/config",
                    },
                ],
            ),
        ],
        indirect=["config_loader"],
    )
    def test_discovery_message(self, neuron: Neuron, covers: CoverMap, expected: List[Dict[str, Any]]) -> None:
        """Test MQTT topic and message when publish a feature."""
        covers.init()
        mock_mqtt_client: AsyncMock = AsyncMock(spec=Client)
        plugin: HassCoversMqttPlugin = HassCoversMqttPlugin(neuron=neuron, mqtt_client=mock_mqtt_client, covers=covers)

        for index, cover in enumerate(covers.by_device_classes(DEVICE_CLASSES)):
            topic, message = plugin.hass.get_discovery(cover)

            assert message == expected[index]["message"]
            assert topic == expected[index]["topic"]
