# solaredge_meterproxy

solaredge_meterproxy is a python tool that proxies Modbus requests from SolarEdge power inverters to unsupported kWh meters. While SolarEdge only supports a [limited number](https://www.solaredge.com/se-supported-devices) of revenue meters, by masquerading as a supported meter it is possible to supply your own meter values to the SolarEdge inverter for production, consumption, import/export monitoring, and export limitation.


## Usage

Todo.

### Configure your SolarEdge inverter

Todo.

### Configure semp.conf

Todo.

## Creating Device Scripts

Support for various kWh meters can be added by creating a Python script in the `devices` directory. This script should adhere to the following:

* Its name corresponds to the device type it masquerades.
* It contains a `device()` function.
* It contains a `values()` function.
* Both functions accept the variables as defined in `/devices/generic.py`.

For a skeleton implementation, see `/devices/generic.py`.

### device()

The `device()` function is called _once_. It gets passed a number of device specific variables, as configured in the global configuration file. It must return a data structure which contains either an active connection, or enough information to identify the device in your datastore. This datastore will be passed to the `values()` function. `host`, `port` and `device` are not substituted by default values if left blank. 

While the intent is to masquerade another Modbus or ModbusTCP device, it should be possible to use virtually any type of data store. InfluxDB, or SQLite, for example.

Each masqueraded meter is updated every `refresh_rate` seconds in its own thread. This thread is provided the `type` module and the data structure returned by `device()`.

### values()

The `values()` function is called every `refresh_rate` seconds. It gets passed the data structure returned by `device()`, and must return a `dict`. The `/devices/generic.py` script contains a list of all possible dictionary keys. It is not required to return all, or in fact any, keys. Functionality of the SolarEdge inverter will depend on the values provided.

Single phase devices should put the single phase values in the generic _and_ first phase specific values, for example: `power_active` and `p1_power_active`, but also `voltage_ln` and `p1n_voltage`.


## Contributing

Contributions are more than welcome, especially new device scripts, or modifications which broaden the use case of this tool.