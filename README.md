# solaredge_meterproxy

solaredge_meterproxy is a python tool that proxies Modbus requests from SolarEdge power inverters to unsupported kWh meters. While SolarEdge only supports a [limited number](https://www.solaredge.com/se-supported-devices) of revenue meters, by masquerading as a supported meter it is possible to supply your own meter values to the SolarEdge inverter for production, consumption, import/export monitoring, and export limitation.


## Usage

Todo.

### Configure your SolarEdge inverter

Todo.

### Configure semp.conf

Todo.

## Creating Device Scripts

Support for various kWh meters can be added by creating a Python script in the `devices` directory, which adheres to the following:

* It is named according to the device it masquerades, after which it can be used as a `type` when configuring meters.
* It contains a `device()` function, which returns a device handle, active connection object, or other unique identifier.
* It contains a `values()` function, which returns a `dict` containing new meter values when passed the result of `device()`.
* The `device()` and `values()` functions adhere to their function prototypes in `/devices/generic.py`.

For a skeleton implementation, see `/devices/generic.py`.

### device()

The `device()` function is called _once_, and is passed a number of device specific variables which can be set in the global configuration file. It must return a data structure which contains either an active connection, or enough information to identify the device in your datastore, when it is passed to the `values()` function. `host`, `port` and `device` are not replaced by default values, which permits you to infer whether the connection should be made via Modbus or ModbusTCP. 

Note that it should be possible to use virtually any type of data store, including InfluxDB, or SQLite.

Each masqueraded meter is updated, every `refresh_rate` seconds, in its own thread. When spawned, this thread is provided the `type` module, and the device handle as returned by `device()`.

### values()

The `values()` function is called every `refresh_rate` seconds, and is passed the device handle, as returned by `device()`, and must return a (partial) `dict`. The `/devices/generic.py` script contains a list of all possible meter values. It is not necessary to provide all, or any, values. Functionality of the SolarEdge inverter will require more or less values to be provided.

Single phase meters should put their single phase values in the generic _and_ phase 1 specific values, for example: `voltage_ln` and `p1n_voltage`, or `power_active` and `p1_power_active`.


## Contributing

Contributions are more than welcome.