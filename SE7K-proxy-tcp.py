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


class EM24SlaveContext(ModbusSlaveContext):
    def getValues(self, fx, address, count=1):
        #if (address == 11 and count==1):
        #    print("Return Gavazzi Model number 1648")
        #    return [1648]
        return super().getValues(fx, address, count)


def setMeterValues(values, block):
    if not values:
        block.add_16bit_uint(0)
        block.add_16bit_uint(0)
        return

    block.add_16bit_uint(1)
    block.add_16bit_uint(65)
    block.add_string    (values.get("c_manufacturer_str"  ,"12345678901234567890123456789012").ljust(32,' '))
    block.add_string    (values.get("c_model_str"         ,"12345678901234567890123456789012").ljust(32,' '))
    block.add_string    (values.get("c_option_str"        ,"1234567890123456").ljust(16,' '))
    block.add_string    (values.get("c_version_str"       ,"1234567890123456").ljust(16,' '))
    block.add_string    (values.get("c_serialnumber_str"  ,"12345678901234567890123456789012").ljust(32,' '))
    block.add_16bit_int (values.get("c_deviceaddress_int" , 0))

    block.add_16bit_int (values.get("c_sunspec_did_int"   , 103))
    block.add_16bit_int (values.get("c_sunspec_length_int", 50))    
    block.add_16bit_uint(values.get("current_int" , 0))
    block.add_16bit_uint(values.get("l1_current_int" , 0))
    block.add_16bit_uint(values.get("l2_current_int" , 0))
    block.add_16bit_uint(values.get("l3_current_int" , 0))
    block.add_16bit_int (values.get("current_scale_int" , 0))

    block.add_16bit_uint(values.get("voltage_ln_int" , 0))
    block.add_16bit_uint(values.get("l1n_voltage_int" , 0))
    block.add_16bit_uint(values.get("l2n_voltage_int" , 0))
    block.add_16bit_uint(values.get("l3n_voltage_int" , 0))
    block.add_16bit_uint(values.get("voltage_ll_int" , 0))
    block.add_16bit_uint(values.get("l1n_voltage_int" , 0))
    block.add_16bit_uint(values.get("l2n_voltage_int" , 0))
    block.add_16bit_uint(values.get("l3n_voltage_int" , 0))
    block.add_16bit_int (values.get("voltage_scale_int" , 0))
    
    block.add_16bit_uint(values.get("frequency_int" , 0))
    block.add_16bit_int (values.get("frequency_scale_int" , 0))

    block.add_16bit_int(values.get("power_int" , 0))
    block.add_16bit_int(values.get("l1_power_int" , 0))
    block.add_16bit_int(values.get("l2_power_int" , 0))
    block.add_16bit_int(values.get("l3_power_int" , 0))
    block.add_16bit_int (values.get("power_scale_int" , 0))

    block.add_16bit_int(values.get("power_apparent_int" , 0))
    block.add_16bit_int(values.get("l1_power_apparent_int" , 0))
    block.add_16bit_int(values.get("l2_power_apparent_int" , 0))
    block.add_16bit_int(values.get("l3_power_apparent_int" , 0))
    block.add_16bit_int (values.get("power_apparent_scale_int" , 0))

    block.add_16bit_int(values.get("power_reactive_int" , 0))
    block.add_16bit_int(values.get("l1_power_reactive_int" , 0))
    block.add_16bit_int(values.get("l2_power_reactive_int" , 0))
    block.add_16bit_int(values.get("l3_power_reactive_int" , 0))
    block.add_16bit_int (values.get("power_reactive_scale_int" , 0))

    block.add_16bit_int(values.get("power_factor_int" , 0))
    block.add_16bit_int(values.get("l1_power_factor_int" , 0))
    block.add_16bit_int(values.get("l2_power_factor_int" , 0))
    block.add_16bit_int(values.get("l3_power_factor_int" , 0))
    block.add_16bit_int (values.get("power_factor_scale_int" , 0))

    block.add_32bit_uint(values.get("export_energy_active_int" , 0))
    block.add_32bit_uint(values.get("l1_export_energy_active_int" , 0))
    block.add_32bit_uint(values.get("l2_export_energy_active_int" , 0))
    block.add_32bit_uint(values.get("l3_export_energy_active_int" , 0))
    block.add_32bit_uint(values.get("import_energy_active_int" , 0))
    block.add_32bit_uint(values.get("l1_import_energy_active_int" , 0))
    block.add_32bit_uint(values.get("l2_import_energy_active_int" , 0))
    block.add_32bit_uint(values.get("l3_import_energy_active_int" , 0))
    block.add_16bit_int (values.get("energy_active_scale_int" , 0))

    block.add_32bit_uint(values.get("export_energy_apparent_int", 0))
    block.add_32bit_uint(values.get("l1_export_energy_apparent_int" , 0))
    block.add_32bit_uint(values.get("l2_export_energy_apparent_int" , 0))
    block.add_32bit_uint(values.get("l3_export_energy_apparent_int" , 0))
    block.add_32bit_uint(values.get("import_energy_apparent_int" , 0))
    block.add_32bit_uint(values.get("l1_import_energy_apparent_int" , 0))
    block.add_32bit_uint(values.get("l2_import_energy_apparent_int" , 0))
    block.add_32bit_uint(values.get("l3_import_energy_apparent_int" , 0))
    block.add_16bit_int (values.get("energy_apparent_scale_int" , 0))

    block.add_32bit_uint(values.get("import_energy_reactive_q1_int" , 0))
    block.add_32bit_uint(values.get("l1_import_energy_reactive_q1_int" , 0))
    block.add_32bit_uint(values.get("l2_import_energy_reactive_q1_int" , 0))
    block.add_32bit_uint(values.get("l3_import_energy_reactive_q1_int" , 0))
    block.add_32bit_uint(values.get("import_energy_reactive_q2_int" , 0))
    block.add_32bit_uint(values.get("l1_import_energy_reactive_q2_int" , 0))
    block.add_32bit_uint(values.get("l2_import_energy_reactive_q2_int" , 0))
    block.add_32bit_uint(values.get("l3_import_energy_reactive_q2_int" , 0))
    block.add_32bit_uint(values.get("export_energy_reactive_q3_int" , 0))
    block.add_32bit_uint(values.get("l1_export_energy_reactive_q3_int" , 0))
    block.add_32bit_uint(values.get("l2_export_energy_reactive_q3_int" , 0))
    block.add_32bit_uint(values.get("l3_export_energy_reactive_q3_int" , 0))
    block.add_32bit_uint(values.get("export_energy_reactive_q4_int" , 0))
    block.add_32bit_uint(values.get("l1_export_energy_reactive_q4_int" , 0))
    block.add_32bit_uint(values.get("l2_export_energy_reactive_q4_int" , 0))
    block.add_32bit_uint(values.get("l3_export_energy_reactive_q4_int" , 0))
    block.add_16bit_int (values.get("energy_reactive_scale_int" , 0))

    block.add_32bit_uint(values.get("events_int" , 0))
    #


def setBatteryValues(values, block):
    if not values:
        block.add_16bit_uint(0)
        block.add_16bit_uint(0)
        return

    block.add_16bit_uint(1)    ## TODO set correct values
    block.add_16bit_uint(65)   ## TODO set correct values

def t_update(ctx, stop, module, device, refresh):

    this_t = threading.currentThread()
    logger = logging.getLogger()

    while not stop.is_set():
        try:
            values = module.values(device)

            if not values:
                logger.debug(f"{this_t.name}: no new values")
                continue

            block_40000 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
            block_40000.add_string("SunS") 
            block_40000.add_16bit_int(1)
            block_40000.add_16bit_int (values.get("C_SunSpec_Length_int", 65))
            block_40000.add_string    (values.get("c_manufacturer_str"  ,"12345678901234567890123456789012").ljust(32,' '))
            block_40000.add_string    (values.get("c_model_str"         ,"12345678901234567890123456789012").ljust(32,' '))
            block_40000.add_string    (                              "NOT_IMPLEMENTED.".ljust(16,' '))
            block_40000.add_string    (values.get("c_version_str"       ,"1234567890123456").ljust(16,' '))
            block_40000.add_string    (values.get("c_serialnumber_str"  ,"12345678901234567890123456789012").ljust(32,' '))
            block_40000.add_16bit_int (values.get("c_deviceaddress_int" , 0))

            block_40000.add_16bit_int (values.get("c_sunspec_did_int"   , 103))
            block_40000.add_16bit_int (50)
            block_40000.add_16bit_uint(values.get("current_int" , 0))
            block_40000.add_16bit_uint(values.get("l1_current_int" , 0))
            block_40000.add_16bit_uint(values.get("l2_current_int" , 0))
            block_40000.add_16bit_uint(values.get("l3_current_int" , 0))
            block_40000.add_16bit_int (values.get("current_scale_int" , 0))

            block_40000.add_16bit_uint(values.get("l1_voltage_int" , 0))
            block_40000.add_16bit_uint(values.get("l2_voltage_int" , 0))
            block_40000.add_16bit_uint(values.get("l3_voltage_int" , 0))
            block_40000.add_16bit_uint(values.get("l1n_voltage_int" , 0))
            block_40000.add_16bit_uint(values.get("l2n_voltage_int" , 0))
            block_40000.add_16bit_uint(values.get("l3n_voltage_int" , 0))
            block_40000.add_16bit_int (values.get("voltage_scale_int" , 0))

            block_40000.add_16bit_int(values.get("power_ac_int" , 0))
            block_40000.add_16bit_int (values.get("power_ac_scale_int" , 0))

            block_40000.add_16bit_uint(values.get("frequency_int" , 0))
            block_40000.add_16bit_int (values.get("frequency_scale_int" , 0))

            block_40000.add_16bit_int(values.get("power_apparent_int" , 0))
            block_40000.add_16bit_int (values.get("power_apparent_scale_int" , 0))

            block_40000.add_16bit_int(values.get("power_reactive_int" , 0))
            block_40000.add_16bit_int (values.get("power_reactive_scale_int" , 0))

            block_40000.add_16bit_int(values.get("power_factor_int" , 0))
            block_40000.add_16bit_int (values.get("power_factor_scale_int" , 0))

            block_40000.add_32bit_uint(values.get("energy_total_int" , 0))
            block_40000.add_16bit_int (values.get("energy_total_scale_int" , 0))

            block_40000.add_16bit_uint(values.get("current_dc_int" , 0))
            block_40000.add_16bit_int (values.get("current_dc_scale_int" , 0))

            block_40000.add_16bit_uint(values.get("voltage_dc_int" , 0))
            block_40000.add_16bit_int (values.get("voltage_dc_scale_int" , 0))

            block_40000.add_16bit_int(values.get("power_dc_int" , 0))
            block_40000.add_16bit_int (values.get("power_dc_scale_int" , 0))

            block_40000.add_16bit_int(0)  # 1 dummy word

            block_40000.add_16bit_int(values.get("temperature_int" , 0))
            block_40000.add_16bit_int(values.get("temperature_scale_int" , 0))

            block_40000.add_16bit_int(0)  # 1 dummy word
            block_40000.add_16bit_int(0)  # 1 dummy word

            block_40000.add_16bit_uint(values.get("status_int" , 0))
            block_40000.add_16bit_uint(values.get("vendor_status_int" , 0))

            block_40000.add_16bit_uint(values.get("rrcr_state_int" , 0))
            block_40000.add_16bit_int(values.get("active_power_limit_int" , 0))
            block_40000.add_32bit_float(values.get("cosphi" , 0))

            block_40000.add_string("123456789012345678901234") # 12 dummy worter = 24 Byte
            ctx.setValues(3, 40000, block_40000.to_registers())

            block_40121 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
            setMeterValues(values["connected_meters"]["Meter1"],block_40121)
            ctx.setValues(3, 40121, block_40121.to_registers())
            
            # block_40295 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
            # ctx.setValues(3, 40295, block_40295.to_registers())
            # block_40469 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
            # ctx.setValues(3, 40469, block_40469.to_registers())

            # block_57598 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
            # ctx.setValues(3, 57598, block_57598.to_registers())
            # block_57854 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
            # ctx.setValues(3, 57854, block_57854.to_registers())
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
            "refresh_rate": 2
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

                #slave_ctx = EM24SlaveContext()
                slave_ctx = ModbusSlaveContext()

                block_40000 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                slave_ctx.setValues(3, 40000, block_40000.to_registers())

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
