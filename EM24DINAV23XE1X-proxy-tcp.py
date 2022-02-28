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

sys.path.append('C:/gitHubClones/modbus/solaredge_modbus/src')
class EM24SlaveContext(ModbusSlaveContext):
    def getValues(self, fx, address, count=1):
        if (address == 11 and count==1):
            print("Return Gavazzi Model number 1648")
            return [1648]
        return super().getValues(fx, address, count)



def t_update(ctx, stop, module, device, refresh):

    this_t = threading.currentThread()
    logger = logging.getLogger()

    while not stop.is_set():
        try:
            values = {}
            values = device.read_all()
            meters = device.meters()
            batteries = device.batteries()
            values["meters"] = {}
            values["batteries"] = {}

            for meter, params in meters.items():
                meter_values = params.read_all()
                values["meters"][meter] = meter_values

            for battery, params in batteries.items():
                battery_values = params.read_all()
                values["batteries"][battery] = battery_values

            meterValues = values["meters"]["Meter1"]

            

            # print("current:"+str(meterValues['current']))

            # print(meterValues['current']*10**meterValues['current_scale'])
            # print(meterValues['p1_current']*10**meterValues['current_scale'])
            # print(meterValues['p2_current']*10**meterValues['current_scale'])
            # print(meterValues['p3_current']*10**meterValues['current_scale'])

            # print(meterValues['voltage_ln']*10**meterValues['voltage_scale'])
            # print(meterValues['p1n_voltage']*10**meterValues['voltage_scale'])
            # print(meterValues['p2n_voltage']*10**meterValues['voltage_scale'])
            # print(meterValues['p3n_voltage']*10**meterValues['voltage_scale'])
            
            # print(meterValues['voltage_ll']*10**meterValues['voltage_scale'])
            # print(meterValues['p12_voltage']*10**meterValues['voltage_scale'])
            # print(meterValues['p23_voltage']*10**meterValues['voltage_scale'])
            # print(meterValues['p31_voltage']*10**meterValues['voltage_scale'])
            
            # print(meterValues['frequency']*10**meterValues['frequency_scale'])

            # print(meterValues['power']*10**meterValues['power_scale'])
            # print(meterValues['p1_power']*10**meterValues['power_scale'])
            # print(meterValues['p2_power']*10**meterValues['power_scale'])
            # print(meterValues['p3_power']*10**meterValues['power_scale'])

            # print(meterValues['power_apparent']*10**meterValues['power_apparent_scale'])
            # print(meterValues['p1_power_apparent']*10**meterValues['power_apparent_scale'])
            # print(meterValues['p2_power_apparent']*10**meterValues['power_apparent_scale'])
            # print(meterValues['p3_power_apparent']*10**meterValues['power_apparent_scale'])

            # print(meterValues['power_reactive']*10**meterValues['power_reactive_scale'])
            # print(meterValues['p1_power_reactive']*10**meterValues['power_reactive_scale'])
            # print(meterValues['p2_power_reactive']*10**meterValues['power_reactive_scale'])
            # print(meterValues['p3_power_reactive']*10**meterValues['power_reactive_scale'])

            # print(meterValues['power_factor']*10**meterValues['power_factor_scale'])
            # print(meterValues['p1_power_factor']*10**meterValues['power_factor_scale'])
            # print(meterValues['p2_power_factor']*10**meterValues['power_factor_scale'])
            # print(meterValues['p3_power_factor']*10**meterValues['power_factor_scale'])

            # print(meterValues['export_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p1_export_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p2_export_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p3_export_energy_active']*10**meterValues['energy_active_scale'])

            # print(meterValues['import_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p1_import_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p2_import_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p3_import_energy_active']*10**meterValues['energy_active_scale'])


            values = module.values(device)

            if not values:
                logger.debug(f"{this_t.name}: no new values")
                continue         

            block_1001 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
            block_1001.add_32bit_float(values.get("energy_active", 0)) # total active energy
            block_1001.add_32bit_float(meterValues['import_energy_active']*10**meterValues['energy_active_scale']) # imported active energy
            block_1001.add_32bit_float(values.get("energy_active", 0)) # total active energy non-reset
            block_1001.add_32bit_float(meterValues['import_energy_active']*10**meterValues['energy_active_scale']) # imported active energy non-reset
            block_1001.add_32bit_float(values.get("power_active", 0)) # total power
            block_1001.add_32bit_float(values.get("p1_power_active", 0)) # power l1
            block_1001.add_32bit_float(values.get("p2_power_active", 0)) # power l2
            block_1001.add_32bit_float(values.get("p3_power_active", 0)) # power l3
            block_1001.add_32bit_float(meterValues['voltage_ln']*10**meterValues['voltage_scale']) # l-n voltage
            block_1001.add_32bit_float(meterValues['p1n_voltage']*10**meterValues['voltage_scale']) # l1-n voltage
            block_1001.add_32bit_float(meterValues['p2n_voltage']*10**meterValues['voltage_scale']) # l2-n voltage
            block_1001.add_32bit_float(meterValues['p3n_voltage']*10**meterValues['voltage_scale']) # l3-n voltage
            block_1001.add_32bit_float(meterValues['voltage_ll']*10**meterValues['voltage_scale']) # l-l voltage
            block_1001.add_32bit_float(meterValues['p12_voltage']*10**meterValues['voltage_scale']) # l1-l2 voltage
            block_1001.add_32bit_float(meterValues['p23_voltage']*10**meterValues['voltage_scale']) # l2-l3 voltage
            block_1001.add_32bit_float(meterValues['p31_voltage']*10**meterValues['voltage_scale']) # l3-l1 voltage
            block_1001.add_32bit_float(meterValues['frequency']*10**meterValues['frequency_scale']) # line frequency
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
            block_1101.add_32bit_float(meterValues['p1_current']*10**meterValues['current_scale']) # current l1
            block_1101.add_32bit_float(meterValues['p2_current']*10**meterValues['current_scale']) # current l2
            block_1101.add_32bit_float(meterValues['p3_current']*10**meterValues['current_scale']) # current l3
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

                slave_ctx = EM24SlaveContext()
                # slave_ctx = ModbusSlaveContext()

                # block_11 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                # block_11.add_16bit_int(1648)
                # slave_ctx.setValues(3, 11, block_11.to_registers())


                block_1001 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                slave_ctx.setValues(3, 1000, block_1001.to_registers())

                block_1101 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                slave_ctx.setValues(3, 1100, block_1101.to_registers())

                update_t_stop = threading.Event()
                update_t = threading.Thread(
                    target=t_update,
                    name=f"t_update_{address}",
                    args=(
                        slave_ctx,
                        update_t_stop,
                        meter_module,
                        meter_device,
                        confparser[meter].getfloat("refresh_rate", fallback=default_config["meters"]["refresh_rate"])
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
