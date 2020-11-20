# solaredge_meterproxy

solaredge_meterproxy is a python tool that proxies Modbus requests from SolarEdge power inverters to unsupported kWh meters. While SolarEdge only supports a [limited number](https://www.solaredge.com/se-supported-devices) of revenue meters, by masquerading as a supported meter it is possible to supply your own meter values to the SolarEdge inverter for production, consumption, import/export monitoring, and export limitation.

This tool simulates one or more [WattNode WNC-3Y-400-MB](https://ctlsys.com/product/wattnode-modbus/) revenue meters, functionally similar to the rebranded SE-WNC-3Y-400-MB-K1 and SE-RGMTR-3D-208V-A/SE-RGMTR-3Y-208V-A. The Modbus registers of these simulated meters can then be updated with values from otherwise unsupported kWh meters.

Supported devices and data sources:

* SDM120 (Modbus RTU, TCP)
* SDM230 (Modbus RTU, TCP)
* SDM630 (Modbus RTU, TCP)
* InfluxDB


## Usage

Run `semp-rtu.py` on a device physically connected via RS485 &mdash; either natively or via USB adapter &mdash; to a SolarEdge inverter. 
```
    usage: semp-rtu.py [-h] [-c CONFIG] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
      -v, --verbose
```

By default, `semp-rtu.py` assumes your RS485 device is located at `/dev/ttyUSB0` with a baud rate of `9600`. The device you will probably need to change, the baud you should not. While configuring and testing solaredge_meterproxy, you should probably run `semp-rtu.py` in debug mode.

RS485 server and proxied meter configurations can be set in `semp.conf`, see [Configuration File](https://github.com/nmakel/solaredge_meterproxy#configuration-file).

### Configure your SolarEdge Inverter

Configuration of the inverter takes place in the SetApp interface. For more information, please read [SolarEdge's SetApp documentation](https://www.solaredge.com/products/installer-tools/setapp). You will need a suitable SolarEdge account to access the SetApp application, available for iOS and Android. While solaredge_meterproxy _should_ work with non-SetApp enabled inverters, this has not been tested.

__If you have multiple SolarEdge inverters connected via Modbus, are currently polling the SunSpec Modbus API, or have one or more revenue meters connected via Modbus, please read _all_ instructions below to be sure you know what you are doing. This guide assumes the RS485 ports are unused and disconnected.__

Once connected to the SetApp interface, you will need to go to the __Site Communication__ settings.

First, ensure your SolarEdge inverter is set to Modbus ID #1:

- Choose the first available RS485 device, in most cases __RS485-1__.
- Set the __Protocol__ to __SunSpec (Non-SE Logger)__.
- Set the __Device ID__ to __1__.

Now, add a meter:

- Set the __Protocol__ to __Modbus (Multi-Device)__.
- Choose __Add Modbus Device__.
- Choose __Meter__.
- Select the newly added __Meter 1__.
- Set __Meter Function__ to the functionality of the meter you will be proxying.
- Set __Meter Protocol__ to __SolarEdge__.
- Set __Device ID__ to __2__, or another unused Modbus ID if you have multiple devices connected.
- Set the appropriate __CT Rating__ and __Grid Topology__ depending on your situation.

The SolarEdge inverter will now be polling a meter with Modbus id 2 on the physical RS485 connection you selected. If you have configured and started solaredge_meterproxy with the corresponding meter configuration, and have physically connected the RS485 adapter to the inverter's RS485 port, you should see a _Meters_ section at the bottom of the _Status_ page. Depending on the _function_ selected, metering functionality should now be available.

If, after configuring a meter in the SetApp interface, you only see meter connection errors, set `log_level` to `debug` in your configuration file. After starting solaredge_meterproxy you should see Modbus read requests from the inverter. If you do, please open an issue with copies of these and your configuration file. If you don't, check your physical connection and RS485 adapter.

### Configuration file

The serial server, and one or more source meters, can be configured in a python `configparser` formatted configuration file. If a file named `semp.conf` is present, this will be loaded by default. If this file does not exist, generic defaults will be loaded. Provide your own configuration file using the `--config` parameter.

For an overview of all configurable parameters, see `semp.conf`.

## Creating Device Scripts

Support for various kWh meters can be added by creating a Python script in the `devices` directory. This script should adhere to the following:

* Its name corresponds to the device type it masquerades.
* It contains a `device()` function.
* It contains a `values()` function.
* Both functions accept the variables as defined in `/devices/generic.py`.

For a skeleton implementation, see `/devices/generic.py`.

### device()

The `device()` function is called _once_. It gets passed a number of device specific variables, as configured in the global configuration file. It must return a data structure which contains either an active connection, or enough information to identify the device in your datastore. This data structure will be passed to the `values()` function. `host`, `port` and `device` are not substituted by default values if left blank. 

While the intent is to masquerade another Modbus or ModbusTCP device, it should be possible to use virtually any type of data store. InfluxDB, or SQLite, for example.

Each masqueraded meter is updated every `refresh_rate` seconds in its own thread. This thread is provided the `type` module and the data structure returned by `device()`.

### values()

The `values()` function is called every `refresh_rate` seconds. It gets passed the data structure returned by `device()`, and must return a `dict`. The `/devices/generic.py` script contains a list of all possible dictionary keys. It is not required to return all, or in fact any, keys. Functionality of the SolarEdge inverter will depend on the values provided.

Single phase devices should put the single phase values in the generic _and_ first phase specific values, for example: `power_active` and `p1_power_active`, but also `voltage_ln` and `p1n_voltage`.


## Contributing

Contributions are more than welcome, especially new device scripts, or modifications which broaden the use case of this tool.