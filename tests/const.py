"""General test constants."""
from custom_components.thermal_comfort.const import (
    CONF_HUMIDITY_SENSOR,
    CONF_POLL,
    CONF_PRESSURE_SENSOR,
    CONF_TEMPERATURE_SENSOR,
)
from custom_components.thermal_comfort.sensor import (
    CONF_CUSTOM_ICONS,
    CONF_ENABLED_SENSORS,
    CONF_SCAN_INTERVAL,
)
from homeassistant.const import CONF_NAME

# What the frontend submits. An optional entity selector left empty is omitted
# from the submitted data rather than sent as an empty value.
USER_INPUT = {
    CONF_NAME: "New name",
    CONF_TEMPERATURE_SENSOR: "sensor.test_temperature_sensor",
    CONF_HUMIDITY_SENSOR: "sensor.test_humidity_sensor",
    CONF_POLL: False,
    CONF_CUSTOM_ICONS: False,
    CONF_SCAN_INTERVAL: 30,
}

ADVANCED_USER_INPUT = {
    **USER_INPUT,
    CONF_NAME: "test_thermal_comfort",
    CONF_ENABLED_SENSORS: [],
}

# What the flows persist. Optional entity selectors are normalized to an
# explicit None so that clearing one actually removes it, instead of falling
# back to the value stored in config_entry.data.
STORED_USER_INPUT = {**USER_INPUT, CONF_PRESSURE_SENSOR: None}

STORED_ADVANCED_USER_INPUT = {**ADVANCED_USER_INPUT, CONF_PRESSURE_SENSOR: None}
