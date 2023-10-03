"""Unit tests MQTT for Home Assistant sensors."""

import asyncio
from asyncio import Task
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Set
from typing import TYPE_CHECKING
from typing import Union
from unittest.mock import AsyncMock

import pytest
from _pytest.logging import LogCaptureFixture
from aiomqtt import Client

from tests.conftest_data import CONFIG_CONTENT
from tests.conftest_data import EXTENSION_HARDWARE_DATA_CONTENT
from tests.conftest_data import HARDWARE_DATA_CONTENT
from tests.unit.mqtt.discovery.test_sensors_data import discovery_message_expected
from unipi_control.features.extensions import EastronMeter
from unipi_control.mqtt.discovery.sensors import HassSensorsDiscovery
from unipi_control.mqtt.discovery.sensors import HassSensorsMqttPlugin
from unipi_control.neuron import Neuron

if TYPE_CHECKING:
    from unipi_control.features.neuron import DigitalInput
    from unipi_control.features.neuron import DigitalOutput
    from unipi_control.features.neuron import Led
    from unipi_control.features.neuron import Relay


class TestHappyPathHassSensorsMqttPlugin:
    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        "config_loader", [(CONFIG_CONTENT, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT)], indirect=True
    )
    async def test_init_tasks(self, neuron: Neuron, caplog: LogCaptureFixture) -> None:
        """Test mqtt output after initialize Home Assistant sensors."""
        mock_mqtt_client: AsyncMock = AsyncMock(spec=Client)
        plugin: HassSensorsMqttPlugin = HassSensorsMqttPlugin(neuron=neuron, mqtt_client=mock_mqtt_client)

        tasks: Set[Task] = set()

        await plugin.init_tasks(tasks)
        await asyncio.gather(*tasks)

        for task in tasks:
            assert task.done() is True

        logs: List[str] = [record.getMessage() for record in caplog.records]

        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/voltage_1/config] "
            "Publishing message: {"
            '"name": "Voltage", '
            '"unique_id": "mocked_unipi_voltage_1", '
            '"state_topic": "mocked_unipi/meter/voltage_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "voltage_1", '
            '"device_class": "voltage", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "V"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/current_1/config] "
            "Publishing message: {"
            '"name": "Current", '
            '"unique_id": "mocked_unipi_current_1", '
            '"state_topic": "mocked_unipi/meter/current_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "current_1", '
            '"device_class": "current", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "A"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/active_power_1/config] "
            "Publishing message: {"
            '"name": "Active Power", '
            '"unique_id": "mocked_unipi_active_power_1", '
            '"state_topic": "mocked_unipi/meter/active_power_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "active_power_1", '
            '"device_class": "power", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "W"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/mocked_id_apparent_power/config] "
            "Publishing message: {"
            '"name": "MOCKED_FRIENDLY_NAME - APPARENT_POWER", '
            '"unique_id": "mocked_unipi_mocked_id_apparent_power", '
            '"state_topic": "mocked_unipi/meter/apparent_power_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "mocked_id_apparent_power", '
            '"icon": "mdi:power-standby", '
            '"device_class": "apparent_power", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "VA"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/reactive_power_1/config] "
            "Publishing message: {"
            '"name": "Reactive Power", '
            '"unique_id": "mocked_unipi_reactive_power_1", '
            '"state_topic": "mocked_unipi/meter/reactive_power_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "reactive_power_1", '
            '"device_class": "power", '
            '"state_class": "total", '
            '"unit_of_measurement": "W"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/power_factor_1/config] "
            "Publishing message: {"
            '"name": "Power Factor", '
            '"unique_id": "mocked_unipi_power_factor_1", '
            '"state_topic": "mocked_unipi/meter/power_factor_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "power_factor_1", '
            '"device_class": "power_factor", '
            '"state_class": "measurement"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/phase_angle_1/config] "
            "Publishing message: {"
            '"name": "Phase Angle", '
            '"unique_id": "mocked_unipi_phase_angle_1", '
            '"state_topic": "mocked_unipi/meter/phase_angle_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "phase_angle_1", '
            '"state_class": "measurement"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/frequency_1/config] "
            "Publishing message: {"
            '"name": "Frequency", '
            '"unique_id": "mocked_unipi_frequency_1", '
            '"state_topic": "mocked_unipi/meter/frequency_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "frequency_1", '
            '"device_class": "frequency", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "Hz"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/import_active_energy_1/config] "
            "Publishing message: {"
            '"name": "Import Active Energy", '
            '"unique_id": "mocked_unipi_import_active_energy_1", '
            '"state_topic": "mocked_unipi/meter/import_active_energy_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "import_active_energy_1", '
            '"device_class": "energy", '
            '"state_class": "total", '
            '"unit_of_measurement": "kWh"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/export_active_energy_1/config] "
            "Publishing message: {"
            '"name": "Export Active Energy", '
            '"unique_id": "mocked_unipi_export_active_energy_1", '
            '"state_topic": "mocked_unipi/meter/export_active_energy_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "export_active_energy_1", '
            '"device_class": "energy", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "kWh"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/import_reactive_energy_1/config] "
            "Publishing message: {"
            '"name": "Import Reactive Energy", '
            '"unique_id": "mocked_unipi_import_reactive_energy_1", '
            '"state_topic": "mocked_unipi/meter/import_reactive_energy_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "import_reactive_energy_1", '
            '"state_class": "total", '
            '"unit_of_measurement": "kvarh"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/export_reactive_energy_1/config] "
            "Publishing message: {"
            '"name": "Export Reactive Energy", '
            '"unique_id": "mocked_unipi_export_reactive_energy_1", '
            '"state_topic": "mocked_unipi/meter/export_reactive_energy_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "export_reactive_energy_1", '
            '"state_class": "total", '
            '"unit_of_measurement": "kvarh"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/total_system_power_demand_1/config] "
            "Publishing message: {"
            '"name": "Total System Power Demand", '
            '"unique_id": "mocked_unipi_total_system_power_demand_1", '
            '"state_topic": "mocked_unipi/meter/total_system_power_demand_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "total_system_power_demand_1", '
            '"device_class": "power", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "W"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/maximum_total_system_power_demand_1/config] "
            "Publishing message: {"
            '"name": "Maximum Total System Power Demand", '
            '"unique_id": "mocked_unipi_maximum_total_system_power_demand_1", '
            '"state_topic": "mocked_unipi/meter/maximum_total_system_power_demand_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "maximum_total_system_power_demand_1", '
            '"device_class": "power", '
            '"state_class": "total", '
            '"unit_of_measurement": "W"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/import_system_power_demand_1/config] "
            "Publishing message: {"
            '"name": "Import System Power Demand", '
            '"unique_id": "mocked_unipi_import_system_power_demand_1", '
            '"state_topic": "mocked_unipi/meter/import_system_power_demand_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "import_system_power_demand_1", '
            '"device_class": "power", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "W"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/maximum_import_system_power_demand_1/config] "
            "Publishing message: {"
            '"name": "Maximum Import System Power Demand", '
            '"unique_id": "mocked_unipi_maximum_import_system_power_demand_1", '
            '"state_topic": "mocked_unipi/meter/maximum_import_system_power_demand_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "maximum_import_system_power_demand_1", '
            '"device_class": "power", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "W"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/export_system_power_demand_1/config] "
            "Publishing message: {"
            '"name": "Export System Power Demand", '
            '"unique_id": "mocked_unipi_export_system_power_demand_1", '
            '"state_topic": "mocked_unipi/meter/export_system_power_demand_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "export_system_power_demand_1", '
            '"device_class": "power", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "W"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/maximum_export_system_power_demand_1/config] "
            "Publishing message: {"
            '"name": "Maximum Export System Power Demand", '
            '"unique_id": "mocked_unipi_maximum_export_system_power_demand_1", '
            '"state_topic": "mocked_unipi/meter/maximum_export_system_power_demand_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "maximum_export_system_power_demand_1", '
            '"device_class": "power", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "W"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/current_demand_1/config] "
            "Publishing message: {"
            '"name": "Current Demand", '
            '"unique_id": "mocked_unipi_current_demand_1", '
            '"state_topic": "mocked_unipi/meter/current_demand_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "current_demand_1", '
            '"device_class": "current", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "A"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/maximum_current_demand_1/config] "
            "Publishing message: {"
            '"name": "Maximum Current Demand", '
            '"unique_id": "mocked_unipi_maximum_current_demand_1", '
            '"state_topic": "mocked_unipi/meter/maximum_current_demand_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "maximum_current_demand_1", '
            '"device_class": "current", '
            '"state_class": "measurement", '
            '"unit_of_measurement": "A"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/total_active_energy_1/config] "
            "Publishing message: {"
            '"name": "Total Active Energy", '
            '"unique_id": "mocked_unipi_total_active_energy_1", '
            '"state_topic": "mocked_unipi/meter/total_active_energy_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "total_active_energy_1", '
            '"device_class": "energy", '
            '"state_class": "total", '
            '"unit_of_measurement": "kWh"'
            "}" in logs
        )
        assert (
            "[MQTT] [homeassistant/sensor/mocked_unipi/total_reactive_energy_1/config] "
            "Publishing message: {"
            '"name": "Total Reactive Energy", '
            '"unique_id": "mocked_unipi_total_reactive_energy_1", '
            '"state_topic": "mocked_unipi/meter/total_reactive_energy_1/get", '
            '"qos": 2, '
            '"force_update": true, '
            '"device": {'
            '"name": "MOCKED Eastron SDM120M - Workspace", '
            '"identifiers": "mocked_eastron_sdm120m_workspace", '
            '"model": "SDM120M", '
            '"sw_version": "202.04", '
            '"manufacturer": "Eastron", '
            '"suggested_area": "Workspace", '
            '"via_device": "MOCKED UNIPI"'
            "}, "
            '"object_id": "total_reactive_energy_1", '
            '"state_class": "total", '
            '"unit_of_measurement": "kvarh"'
            "}" in logs
        )

    @pytest.mark.parametrize(
        ("config_loader", "expected"),
        [
            (
                (CONFIG_CONTENT, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                discovery_message_expected,
            ),
        ],
        indirect=["config_loader"],
    )
    def test_discovery_message(self, neuron: Neuron, expected: List[Dict[str, Any]]) -> None:
        """Test mqtt topic and message when publish a feature."""
        mock_mqtt_client: AsyncMock = AsyncMock(spec=Client)
        plugin: HassSensorsMqttPlugin = HassSensorsMqttPlugin(neuron=neuron, mqtt_client=mock_mqtt_client)
        features: Iterator[
            Union[DigitalInput, DigitalOutput, Led, Relay, EastronMeter]
        ] = neuron.features.by_feature_types(HassSensorsDiscovery.publish_feature_types)

        for index, feature in enumerate(features):
            if isinstance(feature, EastronMeter):
                topic, message = plugin.hass.get_discovery(feature)

                assert message == expected[index]["message"]
                assert topic == expected[index]["topic"]
