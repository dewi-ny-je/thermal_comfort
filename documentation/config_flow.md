# Initial Configuration
## In your Home Assistant UI go to "Configuration", then click "Devices & Services"

![Config Dashboard](https://raw.githubusercontent.com/dolezsa/thermal_comfort/master/screenshots/config_dashboard.png)

## Make sure Integrations is selected and click the "+" button in the bottom right corner

![Config Integrations](https://raw.githubusercontent.com/dolezsa/thermal_comfort/master/screenshots/config_integrations.png)

## Search for or scroll down to find "Thermal Comfort" and select it

![Config Integrations Search](https://raw.githubusercontent.com/dolezsa/thermal_comfort/master/screenshots/config_integrations_search.png)

## Name your virtual device and select the temperature, humidity and, optionally, pressure sensor you want to use

*Note: Sensors carrying the matching device class are listed first, followed by
any other entity which could plausibly hold a temperature or humidity value, so
sensors without a device class can be selected as well.*

*The pressure sensor is optional and only affects the moist air enthalpy. Both
the `pressure` and the `atmospheric_pressure` device classes are offered. If it
is left empty, the pressure is derived from the elevation configured in Home
Assistant. Prefer a sensor reporting absolute (station) pressure: many weather
integrations report pressure normalised to mean sea level, and at higher
elevations leaving this empty is then more accurate.*

![Config Thermal Comfort](https://raw.githubusercontent.com/dolezsa/thermal_comfort/master/screenshots/config_thermal_comfort.png)

## A virtual device is created to manage your calculated sensors

![Config Virtual Device](https://raw.githubusercontent.com/dolezsa/thermal_comfort/master/screenshots/config_devices_thermal_comfort.png)

# Configuration Options

## Click configure on the configuration to set additional options

![Config Virtual Device](https://raw.githubusercontent.com/dolezsa/thermal_comfort/master/screenshots/config_options_thermal_comfort.png)

<dl>
  <dt><strong>Enable Polling</strong> <code>boolean</code></dt>
  <dd>
    Enable this if you want the sensors to be polled. This can avoid double
    calculated values if your input sensors split change updates for humidity
    and temperature.
  </dd>
  <dt><strong>Use custom icons pack</strong>  <code>boolean</code></dt>
  <dd>
    Enable this if you have the <a href="https://github.com/dolezsa/thermal_comfort/blob/master/README.md#custom-icons">custom icon pack</a>
    installed and want to use it as default icons for the sensors
  </dd>
</dl>
