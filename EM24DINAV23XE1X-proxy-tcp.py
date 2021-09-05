#!/usr/bin/env python3

import argparse
import configparser
import importlib
import logging
import sys
import threading
import time

from pymodbus.server.sync import StartTcpServer
from pymodbus.constants import Endian
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.transaction import ModbusSocketFramer
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.datastore import ModbusSlaveContext
from pymodbus.datastore import ModbusServerContext
from pymodbus.payload import BinaryPayloadBuilder


def t_update(ctx, stop, module, device, refresh):

    this_t = threading.currentThread()
    logger = logging.getLogger()

    while not stop.is_set():
        try:
            values = module.values(device)

            if not values:
                logger.debug(f"{this_t.name}: no new values")
                continue

            block_1001 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
            block_1001.add_32bit_float(values.get("energy_active", 0)) # total active energy
            block_1001.add_32bit_float(values.get("import_energy_active", 0)) # imported active energy
            block_1001.add_32bit_float(values.get("energy_active", 0)) # total active energy non-reset
            block_1001.add_32bit_float(values.get("import_energy_active", 0)) # imported active energy non-reset
            block_1001.add_32bit_float(values.get("power_active", 0)) # total power
            block_1001.add_32bit_float(values.get("p1_power_active", 0)) # power l1
            block_1001.add_32bit_float(values.get("p2_power_active", 0)) # power l2
            block_1001.add_32bit_float(values.get("p3_power_active", 0)) # power l3
            block_1001.add_32bit_float(values.get("voltage_ln", 0)) # l-n voltage
            block_1001.add_32bit_float(values.get("p1n_voltage", 0)) # l1-n voltage
            block_1001.add_32bit_float(values.get("p2n_voltage", 0)) # l2-n voltage
            block_1001.add_32bit_float(values.get("p3n_voltage", 0)) # l3-n voltage
            block_1001.add_32bit_float(values.get("voltage_ll", 0)) # l-l voltage
            block_1001.add_32bit_float(values.get("p12_voltage", 0)) # l1-l2 voltage
            block_1001.add_32bit_float(values.get("p23_voltage", 0)) # l2-l3 voltage
            block_1001.add_32bit_float(values.get("p31_voltage", 0)) # l3-l1 voltage
            block_1001.add_32bit_float(values.get("frequency", 0)) # line frequency
            ctx.setValues(3, 1000, block_1001.to_registers())

            block_1101 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
            block_1101.add_32bit_float(values.get("p1_energy_active", 0)) # total active energy l1
            block_1101.add_32bit_float(values.get("p2_energy_active", 0)) # total active energy l2
            block_1101.add_32bit_float(values.get("p3_energy_active", 0)) # total active energy l3
            block_1101.add_32bit_float(values.get("p1_import_energy_active", 0)) # imported active energy l1
            block_1101.add_32bit_float(values.get("p2_import_energy_active", 0)) # imported active energy l2
            block_1101.add_32bit_float(values.get("p3_import_energy_active", 0)) # imported active energy l3
            block_1101.add_32bit_float(values.get("export_energy_active", 0)) # total exported active energy
            block_1101.add_32bit_float(values.get("export_energy_active", 0)) # total exported active energy non-reset
            block_1101.add_32bit_float(values.get("p1_export_energy_active", 0)) # exported energy l1
            block_1101.add_32bit_float(values.get("p2_export_energy_active", 0)) # exported energy l2
            block_1101.add_32bit_float(values.get("p3_export_energy_active", 0)) # exported energy l3
            block_1101.add_32bit_float(values.get("energy_reactive", 0)) # total reactive energy
            block_1101.add_32bit_float(values.get("p1_energy_reactive", 0)) # reactive energy l1
            block_1101.add_32bit_float(values.get("p2_energy_reactive", 0)) # reactive energy l2
            block_1101.add_32bit_float(values.get("p3_energy_reactive", 0)) # reactive energy l3
            block_1101.add_32bit_float(values.get("energy_apparent", 0)) # total apparent energy
            block_1101.add_32bit_float(values.get("p1_energy_apparent", 0)) # apparent energy l1
            block_1101.add_32bit_float(values.get("p2_energy_apparent", 0)) # apparent energy l2
            block_1101.add_32bit_float(values.get("p3_energy_apparent", 0)) # apparent energy l3
            block_1101.add_32bit_float(values.get("power_factor", 0)) # power factor
            block_1101.add_32bit_float(values.get("p1_power_factor", 0)) # power factor l1
            block_1101.add_32bit_float(values.get("p2_power_factor", 0)) # power factor l2
            block_1101.add_32bit_float(values.get("p3_power_factor", 0)) # power factor l3
            block_1101.add_32bit_float(values.get("power_reactive", 0)) # total reactive power
            block_1101.add_32bit_float(values.get("p1_power_reactive", 0)) # reactive power l1
            block_1101.add_32bit_float(values.get("p2_power_reactive", 0)) # reactive power l2
            block_1101.add_32bit_float(values.get("p3_power_reactive", 0)) # reactive power l3
            block_1101.add_32bit_float(values.get("power_apparent", 0)) # total apparent power
            block_1101.add_32bit_float(values.get("p1_power_apparent", 0)) # apparent power l1
            block_1101.add_32bit_float(values.get("p2_power_apparent", 0)) # apparent power l2
            block_1101.add_32bit_float(values.get("p3_power_apparent", 0)) # apparent power l3
            block_1101.add_32bit_float(values.get("p1_current", 0)) # current l1
            block_1101.add_32bit_float(values.get("p2_current", 0)) # current l2
            block_1101.add_32bit_float(values.get("p3_current", 0)) # current l3
            block_1101.add_32bit_float(values.get("demand_power_active", 0)) # demand power
            block_1101.add_32bit_float(values.get("minimum_demand_power_active", 0)) # minimum demand power
            block_1101.add_32bit_float(values.get("maximum_demand_power_active", 0)) # maximum demand power
            block_1101.add_32bit_float(values.get("demand_power_apparent", 0)) # apparent demand power
            block_1101.add_32bit_float(values.get("p1_demand_power_active", 0)) # demand power l1
            block_1101.add_32bit_float(values.get("p2_demand_power_active", 0)) # demand power l2
            block_1101.add_32bit_float(values.get("p3_demand_power_active", 0)) # demand power l3
            ctx.setValues(3, 1100, block_1101.to_registers())
        except Exception as e:
            logger.critical(f"{this_t.name}: {e}")
        finally:
            time.sleep(refresh)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-c", "--config", type=str, default="semp-tcp.conf")
    argparser.add_argument("-v", "--verbose", action="store_true", default=False)
    args = argparser.parse_args()

    default_config = {
        "server": {
            "address": "0.0.0.0",
            "port": 502,
            "framer": "socket",
            "log_level": "INFO",
            "meters": 'Meter1'
        },
        "meters": {
            "dst_address": 2,
            "type": "generic",
            "ct_current": 5,
            "ct_inverted": 0,
            "phase_offset": 120,
            "serial_number": 987654,
            "refresh_rate": 5
        }
    }

    confparser = configparser.ConfigParser()
    confparser.read(args.config)

    if not confparser.has_section("server"):
        confparser["server"] = default_config["server"]

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, confparser["server"].get("log_level", fallback=default_config["server"]["log_level"]).upper()))
    logger.addHandler(log_handler)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    slaves = {}
    threads = []
    thread_stops = []

    try:
        if confparser.has_option("server", "meters"):
            meters = [m.strip() for m in confparser["server"].get("meters", fallback=default_config["server"]["meters"]).split(',')]

            for meter in meters:
                address = confparser[meter].getint("dst_address", fallback=default_config["meters"]["dst_address"])
                meter_type = confparser[meter].get("type", fallback=default_config["meters"]["type"])
                meter_module = importlib.import_module(f"devices.{meter_type}")
                meter_device = meter_module.device(confparser[meter])

                slave_ctx = ModbusSlaveContext()

                block_0x0000 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                                
                block_0x0000.add_32bit_int(   1), #0001 0000h 2 V L1-N INT32 Value weight: Volt*10 N/A 1.0 
                block_0x0000.add_32bit_int(   3), #0003 0002h 2 V L2-N INT32 N/A 1.0 
                block_0x0000.add_32bit_int(   5), #0005 0004h 2 V L3-N INT32 N/A 1.0 
                block_0x0000.add_32bit_int(   7), #0007 0006h 2 V L1-L2 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(   9), #0009 0008h 2 V L2-L3 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  11), #0011 000Ah 2 V L3-L1 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  13), #0013 000Ch 2 A L1 INT32 Value weight: Ampere*1000 N/A 1.0 
                block_0x0000.add_32bit_int(  15), #0015 000Eh 2 A L2 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  17), #0017 0010h 2 A L3 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  19), #0019 0012h 2 W L1 INT32 Value weight: Watt*10 N/A 1.0 
                block_0x0000.add_32bit_int(  21), #0021 0014h 2 W L2 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  23), #0023 0016h 2 W L3 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  25), #0025 0018h 2 VA L1 INT32 Value weight: VA*10 N/A 1.0 
                block_0x0000.add_32bit_int(  27), #0027 001Ah 2 VA L2 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  29), #0029 001Ch 2 VA L3 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  31), #0031 001Eh 2 VAR L1 INT32 Value weight: var*10 N/A 1.0 
                block_0x0000.add_32bit_int(  33), #0033 0020h 2 VAR L2 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  35), #0035 0022h 2 VAR L3 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  37), #0037 0024h 2 V L-N ? INT32 Value weight: Volt*10 N/A 1.0 
                block_0x0000.add_32bit_int(  39), #0039 0026h 2 V L-L ? INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  41), #0041 0028h 2 W ? INT32 Value weight: Watt*10 N/A 1.0 
                block_0x0000.add_32bit_int(  43), #0043 002Ah 2 VA ? INT32 Value weight: VA*10 N/A 1.0 
                block_0x0000.add_32bit_int(  45), #0045 002Ch 2 VAR ? INT32 Value weight: var*10 N/A 1.0 
                block_0x0000.add_16bit_int(  47), #0047 002Eh 1 PF L1 INT16 Negative values correspond to lead(C), positive value correspond to lag(L) Value weight: PF*1000 N/A 1.0 
                block_0x0000.add_16bit_int(  48), #0048 002Fh 1 PF L2 INT16 N/A 1.0 
                block_0x0000.add_16bit_int(  49), #0049 0030h 1 PF L3 INT16 N/A 1.0 
                block_0x0000.add_16bit_int(  50), #0050 0031h 1 PF ? INT16 N/A 1.0 
                block_0x0000.add_16bit_int(  51), #0051 0032h 1 Phase sequence INT16 Value �1 correspond to L1-L3-L2 sequence, value 0 correspond to L1-L2-L3 sequence (this value is meaningful only in case of 3-phase systems) N/A 1.0 
                block_0x0000.add_16bit_uint(  52),#0052 0033h 1 Hz UINT16 Value weight: Hz*10 N/A 1.0 
                block_0x0000.add_32bit_int(  53), #0053 0034h 2 KWh(+) TOT INT32 Value weight: kWh*10 N/A 1.0 
                block_0x0000.add_32bit_int(  55), #0055 0036h 2 Kvarh(+) TOT INT32 Value weight: kvarh*10 N/A 1.0 
                block_0x0000.add_32bit_int(  57), #0057 0038h 2 DMD W ? INT32 Value weight: Watt*10 N/A 1.0 
                block_0x0000.add_32bit_int(  59), #0059 003Ah 2 DMD W ? max INT32 Value weight: Watt*10 N/A 1.0 
                block_0x0000.add_32bit_int(  61), #0061 003Ch 2 KWh(+) PAR INT32 Value weight: kWh*10 N/A 1.0 
                block_0x0000.add_32bit_int(  63), #0063 003Eh 2 Kvarh(+) PAR INT32 Value weight: kvarh*10 N/A 1.0 
                block_0x0000.add_32bit_int(  65), #0065 0040h 2 KWh(+) L1 INT32 Value weight: kWh*10 N/A 1.0 
                block_0x0000.add_32bit_int(  67), #0067 0042h 2 KWh(+) L2 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  69), #0069 0044h 2 KWh(+) L3 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  71), #0071 0046h 2 KWh(+) T1 INT32 Value weight: kWh*10 N/A 1.0 
                block_0x0000.add_32bit_int(  73), #0073 0048h 2 KWh(+) T2 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  75), #0075 004Ah 2 KWh(+) T3 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  77), #0077 004Ch 2 KWh(+) T4 INT32 N/A 1.0 
                block_0x0000.add_32bit_int(  79), #0079 004Eh 2 KWh(-) TOT INT32 Value weight: kWh*10 N/A 1.0 
                block_0x0000.add_32bit_int(  81), #0081 0050h 2 Kvarh(-) TOT INT32 Value weight: kvarh*10 N/A 1.0 
                block_0x0000.add_16bit_int(  83), #0083       1 unused
                block_0x0000.add_16bit_int(  84), #0084       1 unused
                block_0x0000.add_16bit_int(  85), #0085       1 unused
                block_0x0000.add_16bit_int(  86), #0086       1 unused
                block_0x0000.add_16bit_int(  87), #0087       1 unused
                block_0x0000.add_16bit_int(  88), #0088       1 unused
                block_0x0000.add_16bit_int(  89), #0089       1 unused
                block_0x0000.add_16bit_int(  90), #0090       1 unused
                block_0x0000.add_32bit_int(  91), #0091 005Ah 2 Hour INT32 Value weight: hour*100 N/A 1.0 
                block_0x0000.add_16bit_int(  93), #0093       1 unused
                block_0x0000.add_16bit_int(  94), #0094       1 unused
                block_0x0000.add_16bit_int(  95), #0095       1 unused
                block_0x0000.add_16bit_int(  96), #0096       1 unused
                block_0x0000.add_16bit_int(  97), #0096       1 unused
                block_0x0000.add_16bit_int(  98), #0097       1 unused
                block_0x0000.add_16bit_int(  99), #0098       1 unused
                block_0x0000.add_16bit_int( 101), #0099       1 unused
                block_0x0000.add_16bit_int( 102), #0100       1 unused
                block_0x0000.add_16bit_int( 103), #0101       1 unused
                block_0x0000.add_16bit_int( 104), #0102       1 unused
                block_0x0000.add_16bit_int( 105), #0103       1 unused
                block_0x0000.add_16bit_int( 106), #0104       1 unused
                block_0x0000.add_16bit_int( 107), #0105       1 unused
                block_0x0000.add_16bit_int( 108), #0106       1 unused
                block_0x0000.add_16bit_int( 109), #0107       1 unused
                block_0x0000.add_16bit_int( 110), #0108       1 unused
                block_0x0000.add_16bit_int( 110), #0109       1 unused
                block_0x0000.add_16bit_int( 110), #0110       1 unused
                block_0x0000.add_32bit_int( 111), #0111 006Eh 2 Kvarh(+) T1 INT32 Value weight: kvarh*10 N/A 1.0 
                block_0x0000.add_32bit_int( 113), #0113 0070h 2 Kvarh(+) T2 INT32 N/A 1.0 
                block_0x0000.add_32bit_int( 115), #0115 0072h 2 Kvarh(+) T3 INT32 N/A 1.0 
                block_0x0000.add_32bit_int( 117), #0117 0074h 2 Kvarh(+) T4 INT32 N/A 1.0 
                block_0x0000.add_32bit_int( 119), #0119 0076h 2 DMD VA ? INT32 Value weight: VA*10 N/A 1.0 
                block_0x0000.add_32bit_int( 121), #0121 0078h 2 DMD VA ? max INT32 Value weight: VA*10 N/A 1.0 
                block_0x0000.add_32bit_int( 123), #0123 007Ah 2 DMD A max INT32 Value weight: Ampere*1000 N/A 1.0

                slave_ctx.setValues(3, 0x0000, block_0x0000.to_registers())

                block_0x000B = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_0x000B.add_16bit_int(1648), #0012 000Bh 1 Carlo Gavazzi identification code UINT 16 For a valid request, length must be 1, otherwise the request is forwarded to instantaneous variables
                                                  # EM24DINAV23XE1X 1648 (0x670)
                slave_ctx.setValues(3, 0x000B, block_0x000B.to_registers())

                update_t_stop = threading.Event()
                update_t = threading.Thread(
                    target=t_update,
                    name=f"t_update_{address}",
                    args=(
                        slave_ctx,
                        update_t_stop,
                        meter_module,
                        meter_device,
                        confparser[meter].getint("refresh_rate", fallback=default_config["meters"]["refresh_rate"])
                    )
                )

                threads.append(update_t)
                thread_stops.append(update_t_stop)

                slaves.update({address: slave_ctx})
                logger.info(f"Created {update_t}: {meter} {meter_type} {meter_device}")

        if not slaves:
            logger.warning(f"No meters defined in {args.config}")

        config_framer = confparser["server"].get("framer", fallback=default_config["server"]["framer"])
        framer = False

        if config_framer == "socket":
            framer = ModbusSocketFramer
        elif config_framer == "rtu":
            framer = ModbusRtuFramer

        identity = ModbusDeviceIdentification()
        server_ctx = ModbusServerContext(slaves=slaves, single=False)

        time.sleep(1)

        for t in threads:
            t.start()
            logger.info(f"Starting {t}")

        StartTcpServer(
            server_ctx,
            framer=framer,
            identity=identity,
            address=(
                confparser["server"].get("address", fallback=default_config["server"]["address"]),
                confparser["server"].getint("port", fallback=default_config["server"]["port"])
            )
        )
    except KeyboardInterrupt:
        pass
    finally:
        for t_stop in thread_stops:
            t_stop.set()
        for t in threads:
            t.join()
