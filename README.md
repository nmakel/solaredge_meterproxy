# solaredge_meterproxy

solaredge_meterproxy is a python tool that responds to Modbus requests from SolarEdge power inverters with data from unsupported kWh meters. While SolarEdge only supports a [limited number](https://www.solaredge.com/se-supported-devices) of revenue meters, by masquerading as a supported meter it is possible to supply your own meter values to the SolarEdge inverter for production, consumption, import/export monitoring, and export limitation.

This tool simulates one or more [WattNode WNC-3Y-400-MB](https://ctlsys.com/product/wattnode-modbus/) revenue meters, functionally similar to the rebranded SE-WNC-3Y-400-MB-K1. The Modbus registers of these simulated meters can then be updated with values from otherwise unsupported kWh meters, or sourced from a variety of data sources.

SolarEdge inverters only use Modbus RTU over RS485 to communicate with meters, this project supports both Modbus RTU when connected directly to an inverter over RS485, *and* Modbus TCP in case a Modbus TCP gateway is connected to the inverter. This functionality has been tested using an [ICP-DAS tGW-715](https://www.icpdas.com/en/product/tGW-715) and [Elfin EE11](http://www.hi-flying.com/elfin-ee10-elfin-ee11) Modbus TCP to RTU gateway.

Supported devices and data sources:

* [Eastron SDM120M](https://www.eastroneurope.com/products/view/sdm120modbus)
* [Eastron SDM230M](https://www.eastroneurope.com/products/view/sdm230modbus)
* [Eastron SDM630M](https://www.eastroneurope.com/products/view/sdm630modbus)
* InfluxDB


## Usage

Decide whether you will be running a Modbus RTU or Modbus TCP server. If your device is directly connected to the inverter via RS485 using a serial device or USB dongle, choose Modbus RTU. If you have a Modbus TCP gateway connected to your inverter, choose Modbus TCP.

### Modbus RTU

Run `semp-rtu.py` on a device connected via RS485 to a SolarEdge inverter. 
```
    usage: semp-rtu.py [-h] [-c CONFIG] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
      -v, --verbose
```

By default, `semp-rtu.py` assumes your RS485 device is located at `/dev/ttyUSB0` with a baud rate of `9600`. While configuring and testing solaredge_meterproxy, you should run `semp-rtu.py` in verbose mode. The Modbus server and source meter configurations can be set in `semp-rtu.conf`. See [Configuration File](https://github.com/nmakel/solaredge_meterproxy#configuration-file) for more information.

### Modbus TCP

Run `semp-tcp.py` on a device on the same network as a Modbus TCP gateway connected via RS485 to a SolarEdge inverter. 
```
    usage: semp-tcp.py [-h] [-c CONFIG] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
      -v, --verbose
```

Before running `semp-tcp.py`, configure a TCP IP and port for it to listen on. Your Modbus TCP gateway will need to be configured as *TCP client*, connecting to the IP and port you assigned `semp-tcp.py`. While configuring and testing solaredge_meterproxy, you should run `semp-tcp.py` in verbose mode. The Modbus server and source meter configurations can be set in `semp-tcp.conf`. See [Configuration File](https://github.com/nmakel/solaredge_meterproxy#configuration-file) for more information.

### Configure your SolarEdge Inverter

Configuration of the inverter takes place in the SetApp interface or the LCD display on the inverter. For more information, please read [SolarEdge's SetApp documentation](https://www.solaredge.com/products/installer-tools/setapp). You will need a SolarEdge installer account to access the SetApp application. The account is free, and the app is available on both iOS and Android.

__If you have multiple SolarEdge inverters connected via Modbus, are currently using the SunSpec Modbus logger function, or have one or more revenue meters connected via Modbus, please read _all_ instructions below to be sure you know what you are doing. This guide assumes both RS485 ports are unused and disconnected.__

First, ensure your SolarEdge inverter's Modbus address is set to 1:

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

The SolarEdge inverter will now try to connect to a meter with Modbus address 2 on the RS485 device you selected. If you have configured and started solaredge_meterproxy with a matching meter configuration you should see a _Meters_ section at the bottom of the _Status_ page. Depending on the _function_ selected, metering functionality should now be available.

If, after configuring a meter in the SetApp interface, you see only meter connection errors, set `log_level` to `DEBUG` in your configuration file. After starting solaredge_meterproxy you should see Modbus read requests from the inverter. If you do, please open an issue with copies of these and your configuration file. If you don't, check your connection, RS485 adapter, or Modbus TCP gateway settings.

### Configuration file

The server, and one or more source meters, can be configured in a python `configparser` formatted configuration file. If a configuration file is not specified, and `semp-rtu.conf` of `semp-tcp.conf` are not found, generic defaults will be loaded. Provide an alternate configuration file using the `--config` parameter.

For an overview of all configurable parameters, see `semp-rtu.conf` or `semp-tcp.conf`.

Device scripts contain additional, often required, configuration parameters. Consult the relevant device script for an overview when configuring source meters.

An example **Modbus RTU** configuration, with a SDM120 source that is accessible over Modbus TCP:

```
[server]
device = /dev/ttyUSB0
baud = 9600
log_level = INFO
meters = meter1

[meter1]
type=sdm120
host=10.0.0.124
port=502
src_address=1
dst_address=2
```

An example **Modbus TCP** configuration, with a SDM120 source that is accessible over Modbus RTU:

```
[server]
address = 10.0.0.123
port = 5502
log_level = INFO
meters = sdm120

[sdm120]
type=sdm120
device=/dev/ttyUSB0
baud=9600
src_address=1
dst_address=2
```

If you receive `DEBUG: Frame check failed, ignoring!!` errors, the Modbus TCP gateway is probably sending you RTU frames inside TCP packets. In that case, set the `framer = rtu` configuration parameter inside the `[server]` block.


## Creating Device Scripts

Support for various kWh meters can be added by creating a Python script in the `devices` directory. This script should adhere to the following:

* Its name corresponds to the device or source it masquerades.
* It contains a `device()` function.
* It contains a `values()` function.
* Both functions accept the variables as defined in `/devices/generic.py`.

For a skeleton implementation, see `/devices/generic.py`.

### device()

The `device()` function is called _once_. It gets passed a `configparser` object with the device's configuration parameters, as configured in the configuration file. It must return a data structure which contains either an active connection, or enough information to identify the device in a data store. This data structure will be passed to the `values()` function.

While the intent is to masquerade another Modbus RTU or Modbus TCP device, it is possible to use virtually any type of data store. InfluxDB, or SQLite, for example.

### values()

The `values()` function is called every `refresh_rate` seconds. It gets passed the data structure returned by `device()`, and must return a `dict`. The `/devices/generic.py` script contains a list of all possible dictionary keys. It is not required to return all, or in fact any, keys. Functionality of the SolarEdge inverter will depend on the values provided.

Single phase devices should put the single phase values in the generic _and_ first phase specific values, for example: `power_active` and `p1_power_active`, but also `voltage_ln` and `p1n_voltage`.


## Contributing

Contributions are more than welcome, especially new device scripts, or modifications which broaden the use case of this tool.