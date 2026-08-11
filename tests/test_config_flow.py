"""Test integration_blueprint config flow."""

import json
from unittest.mock import MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.thermal_comfort.config_flow import build_schema, get_value
from custom_components.thermal_comfort.const import CONF_PRESSURE_SENSOR, DOMAIN
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResultType

from .const import (
    ADVANCED_USER_INPUT,
    STORED_ADVANCED_USER_INPUT,
    STORED_USER_INPUT,
    USER_INPUT,
)
from .test_sensor import DEFAULT_TEST_SENSORS, PRESSURE_SENSOR_TEST_SENSORS


@pytest.fixture(autouse=True)
def bypass_setup_fixture():
    """Prevent setup."""
    with patch(
        "custom_components.thermal_comfort.async_setup_entry",
        return_value=True,
    ):
        yield


async def _flow_init(hass):
    return await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )


async def _flow_configure(hass, r, _input=ADVANCED_USER_INPUT):
    with patch(
        "homeassistant.helpers.entity_registry.EntityRegistry.async_get",
        return_value=MagicMock(unique_id="foo"),
    ):
        return await hass.config_entries.flow.async_configure(
            r["flow_id"], user_input=_input
        )


@pytest.mark.parametrize(*DEFAULT_TEST_SENSORS)
async def test_successful_config_flow(hass, start_ha):
    """Test a successful config flow."""
    # Initialize a config flow
    result = await _flow_init(hass)

    # Check that the config flow shows the user form as the first step
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await _flow_configure(hass, result)

    assert result["type"] == FlowResultType.CREATE_ENTRY

    assert result["title"] == ADVANCED_USER_INPUT[CONF_NAME]
    assert result["data"] == STORED_ADVANCED_USER_INPUT
    assert result["result"]


@pytest.mark.parametrize(*DEFAULT_TEST_SENSORS)
async def test_failed_config_flow(hass, start_ha):
    """Config flow should fail if ..."""

    # We try to set up second instance for same temperature and humidity sensors
    for _ in [0, 1]:
        result = await _flow_init(hass)
        result = await _flow_configure(hass, result)

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "already_configured"


@pytest.mark.parametrize(*DEFAULT_TEST_SENSORS)
async def test_options_flow(hass, start_ha):
    """Test flow for options changes."""
    # setup entry
    entry = MockConfigEntry(domain=DOMAIN, data=ADVANCED_USER_INPUT, entry_id="test")
    entry.add_to_hass(hass)

    # Initialize an options flow for entry
    result = await hass.config_entries.options.async_init(entry.entry_id)

    # Verify that the first options step is a user form
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "init"

    # Enter some data into the form
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input=USER_INPUT,
    )

    # Verify that the flow finishes
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == ""

    # Verify that the options were updated

    assert entry.options == STORED_USER_INPUT


@pytest.mark.parametrize(*PRESSURE_SENSOR_TEST_SENSORS)
async def test_options_flow_can_clear_pressure_sensor(hass, start_ha):
    """A configured pressure sensor must be removable via the options flow."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            **ADVANCED_USER_INPUT,
            CONF_PRESSURE_SENSOR: "sensor.test_pressure_sensor",
        },
        entry_id="test",
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] == FlowResultType.FORM

    # USER_INPUT omits the key, exactly as ha-form does when the picker is
    # cleared. Without normalization this would fall back to entry.data.
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], user_input=USER_INPUT
    )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert get_value(entry, CONF_PRESSURE_SENSOR) is None


@pytest.mark.parametrize(*PRESSURE_SENSOR_TEST_SENSORS)
async def test_config_flow_pressure_sensor_not_found(hass, start_ha):
    """check_input rejects a pressure entity which has no state."""
    result = await _flow_init(hass)

    # The picker offered the entity, but it is gone by the time we submit.
    hass.states.async_remove("sensor.test_pressure_sensor")
    result = await _flow_configure(
        hass,
        result,
        {**ADVANCED_USER_INPUT, CONF_PRESSURE_SENSOR: "sensor.test_pressure_sensor"},
    )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"]["base"] == "pressure_not_found"


@pytest.mark.parametrize(*PRESSURE_SENSOR_TEST_SENSORS)
async def test_build_schema_offers_atmospheric_pressure_sensors(hass, start_ha):
    """The pressure picker must offer atmospheric_pressure device class sensors."""
    schema = build_schema(config_entry=None, hass=hass)
    assert schema is not None

    marker = next(key for key in schema.schema if str(key) == CONF_PRESSURE_SENSOR)
    assert (
        "sensor.test_pressure_sensor"
        in schema.schema[marker].config["include_entities"]
    )


async def test_config_flow_enabled():
    """Test is manifest.json have 'config_flow': true."""
    with open("custom_components/thermal_comfort/manifest.json") as f:
        manifest = json.load(f)
        assert manifest.get("config_flow") is True


# @pytest.mark.parametrize(*DEFAULT_TEST_SENSORS)
# @pytest.mark.parametrize("sensor", [CONF_TEMPERATURE_SENSOR, CONF_HUMIDITY_SENSOR])
# async def test_missed_sensors(hass, sensor, start_ha):
#    """Test is we show message if sensor missed."""
#
#    result = await _flow_init(hass)
#
#    # Check that the config flow shows the user form as the first step
#    assert result["type"] == FlowResultType.FORM
#    assert result["step_id"] == "user"
#
#    no_sensor = dict(ADVANCED_USER_INPUT)
#    no_sensor[sensor] = "foo"
#    with pytest.raises(vol.error.MultipleInvalid):
#        result = await _flow_configure(hass, result, no_sensor)
#
#    assert result["type"] == FlowResultType.FORM
