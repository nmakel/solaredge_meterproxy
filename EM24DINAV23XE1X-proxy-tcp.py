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

            

            print("current:"+str(meterValues['current']))
            print(str(meterValues['current']*10**meterValues['current_scale']))
            #print(meterValues['p1_current']*10**meterValues['current_scale'])
            #print(meterValues['p2_current']*10**meterValues['current_scale'])
            #print(meterValues['p3_current']*10**meterValues['current_scale'])
            print(meterValues['current_scale'])

            print("voltage_ln:"+str(meterValues['voltage_ln']))
            print(meterValues['voltage_ln']*10**meterValues['voltage_scale'])
            # print(meterValues['p1n_voltage']*10**meterValues['voltage_scale'])
            # print(meterValues['p2n_voltage']*10**meterValues['voltage_scale'])
            # print(meterValues['p3n_voltage']*10**meterValues['voltage_scale'])
            print(meterValues['voltage_scale'])

            print("voltage_ll:"+str(meterValues['voltage_ll']))          
            print(meterValues['voltage_ll']*10**meterValues['voltage_scale'])
            # print(meterValues['p12_voltage']*10**meterValues['voltage_scale'])
            # print(meterValues['p23_voltage']*10**meterValues['voltage_scale'])
            # print(meterValues['p31_voltage']*10**meterValues['voltage_scale'])
            print(meterValues['voltage_scale'])

            
            print("frequency:"+str(meterValues['frequency']))          
            print(meterValues['frequency']*10**meterValues['frequency_scale'])

            print("power:"+str(meterValues['power']))          
            print(meterValues['power']*10**meterValues['power_scale'])
            # print(meterValues['p1_power']*10**meterValues['power_scale'])
            # print(meterValues['p2_power']*10**meterValues['power_scale'])
            # print(meterValues['p3_power']*10**meterValues['power_scale'])
            print(meterValues['power_scale'])

            print("power_apparent:"+str(meterValues['power_apparent']))          
            print(meterValues['power_apparent']*10**meterValues['power_apparent_scale'])
            # print(meterValues['p1_power_apparent']*10**meterValues['power_apparent_scale'])
            # print(meterValues['p2_power_apparent']*10**meterValues['power_apparent_scale'])
            # print(meterValues['p3_power_apparent']*10**meterValues['power_apparent_scale'])
            print(meterValues['power_apparent_scale'])

            print("power_reactive:"+str(meterValues['power_reactive']))          
            print(meterValues['power_reactive']*10**meterValues['power_reactive_scale'])
            # print(meterValues['p1_power_reactive']*10**meterValues['power_reactive_scale'])
            # print(meterValues['p2_power_reactive']*10**meterValues['power_reactive_scale'])
            # print(meterValues['p3_power_reactive']*10**meterValues['power_reactive_scale'])
            print(meterValues['power_reactive_scale'])

            print("power_factor:"+str(meterValues['power_factor']))          
            print(meterValues['power_factor']*10**meterValues['power_factor_scale'])
            # print(meterValues['p1_power_factor']*10**meterValues['power_factor_scale'])
            # print(meterValues['p2_power_factor']*10**meterValues['power_factor_scale'])
            # print(meterValues['p3_power_factor']*10**meterValues['power_factor_scale'])
            print(meterValues['power_factor_scale'])

            print("export_energy_active:"+str(meterValues['export_energy_active']))          
            print(meterValues['export_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p1_export_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p2_export_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p3_export_energy_active']*10**meterValues['energy_active_scale'])
            print(meterValues['energy_active_scale'])

            print("import_energy_active:"+str(meterValues['import_energy_active']))          
            print(meterValues['import_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p1_import_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p2_import_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p3_import_energy_active']*10**meterValues['energy_active_scale'])
            print(meterValues['energy_active_scale'])

            print("import_energy_apparent:"+str(meterValues['import_energy_apparent']))          
            print(meterValues['import_energy_apparent']*10**meterValues['energy_apparent_scale'])
            # print(meterValues['p1_import_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p2_import_energy_active']*10**meterValues['energy_active_scale'])
            # print(meterValues['p3_import_energy_active']*10**meterValues['energy_active_scale'])
            print(meterValues['energy_apparent_scale'])


            values = module.values(device)

            if not values:
                logger.debug(f"{this_t.name}: no new values")
                continue         

            block_0 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
            block_0.add_32bit_int(int(meterValues['p1n_voltage']/10)) # l1-n voltage    * 10
            block_0.add_32bit_int(int(meterValues['p2n_voltage']/10)) # l2-n voltage
            block_0.add_32bit_int(int(meterValues['p3n_voltage']/10)) # l3-n voltage
            block_0.add_32bit_int(int(meterValues['p12_voltage']/10)) # l1-l2 voltage
            block_0.add_32bit_int(int(meterValues['p23_voltage']/10)) # l2-l3 voltage
            block_0.add_32bit_int(int(meterValues['p31_voltage']/10)) # l3-l1 voltage
            block_0.add_32bit_int(meterValues['p1_current']*100) # current l1      * 1000
            block_0.add_32bit_int(meterValues['p2_current']*100) # current l2
            block_0.add_32bit_int(meterValues['p3_current']*100) # current l3
            block_0.add_32bit_int(meterValues['p1_power']*10) # power l1   *10
            block_0.add_32bit_int(meterValues['p2_power']*10) # power l2
            block_0.add_32bit_int(meterValues['p3_power']*10) # power l3
            block_0.add_32bit_int(meterValues['p1_power_apparent']*10) # apparent power l1   *10
            block_0.add_32bit_int(meterValues['p2_power_apparent']*10) # apparent power l2
            block_0.add_32bit_int(meterValues['p3_power_apparent']*10) # apparent power l3
            block_0.add_32bit_int(meterValues['p1_power_reactive']*10) # reactive power l1   *10
            block_0.add_32bit_int(meterValues['p2_power_reactive']*10) # reactive power l2
            block_0.add_32bit_int(meterValues['p3_power_reactive']*10) # reactive power l3
            block_0.add_32bit_int(int(meterValues['voltage_ln']/10)) # l-n voltage                *10
            block_0.add_32bit_int(int(meterValues['voltage_ll']/10)) # l-l voltage
            block_0.add_32bit_int(meterValues['power']*10) # total power              *10
            block_0.add_32bit_int(meterValues['power_apparent']*10) # total apparent power
            block_0.add_32bit_int(meterValues['power_reactive']*10) # total reactive power
            block_0.add_16bit_int(int(meterValues['p1_power_factor']/10)) # power factor l1       *1000
            block_0.add_16bit_int(int(meterValues['p2_power_factor']/10)) # power factor l2
            block_0.add_16bit_int(int(meterValues['p3_power_factor']/10)) # power factor l3
            block_0.add_16bit_int(int(meterValues['power_factor']/10)) # power factor
            block_0.add_16bit_int(0) # Value –1 correspond to L1-L3-L2 sequence, value 0 correspond to L1-L2-L3 sequence (this value is meaningful only in case of 3-phase systems)
            
            block_0.add_16bit_uint(int(meterValues['frequency']/10)) # line frequency           *10

            block_0.add_32bit_int(int(meterValues['import_energy_active']/100)) # imported active energy
            block_0.add_32bit_int(int(meterValues['import_energy_apparent']/100)) # imported active energy
            block_0.add_32bit_int(56) # demand power
            block_0.add_32bit_int(58) # maximum demand power
            block_0.add_32bit_int(int(meterValues['import_energy_active']/100)) # imported active energy
            block_0.add_32bit_int(int(meterValues['import_energy_apparent']/100)) # imported active energy
            block_0.add_32bit_int(int(meterValues['p1_import_energy_active']/100)) # imported active energy l1
            block_0.add_32bit_int(int(meterValues['p2_import_energy_active']/100)) # imported active energy l2
            block_0.add_32bit_int(int(meterValues['p3_import_energy_active']/100)) # imported active energy l3
            block_0.add_32bit_int(10) # total active energy Tarif 1
            block_0.add_32bit_int(20) # total active energy Tarif 2
            block_0.add_32bit_int(30) # total active energy Tarif 3
            block_0.add_32bit_int(40) # total active energy Tarif 4
            block_0.add_32bit_int(int(meterValues['export_energy_active']/100)) # total exported active energy non-reset   /100)
            block_0.add_32bit_int(int(meterValues['export_energy_apparent']/100)) # imported active energy non-reset
            block_0.add_32bit_int(2400) # hour                                                             *100
            block_0.add_32bit_int(11) # total apparent energy Tarif 1                                      *10
            block_0.add_32bit_int(22) # total apparent energy Tarif 2
            block_0.add_32bit_int(33) # total apparent energy Tarif 3
            block_0.add_32bit_int(44) # total apparent energy Tarif 4
            block_0.add_32bit_int(118) # apparent demand power
            block_0.add_32bit_int(120) # apparent demand power max
            block_0.add_32bit_int(122) # DMD A max                        *10
            ctx.setValues(3, 0, block_0.to_registers())

            ## unused values
            # "energy_reactive"              # total reactive energy
            # "p1_export_energy_active", 0)) # exported energy l1
            # "p2_export_energy_active", 0)) # exported energy l2
            # "p3_export_energy_active", 0)) # exported energy l3
            # "p1_energy_reactive", 0)) # reactive energy l1
            # "p2_energy_reactive", 0)) # reactive energy l2
            # "p3_energy_reactive", 0)) # reactive energy l3
            # "p1_energy_apparent", 0)) # apparent energy l1
            # "p2_energy_apparent", 0)) # apparent energy l2
            # "p3_energy_apparent", 0)) # apparent energy l3
            # "minimum_demand_power_active", 0)) # minimum demand power
            # "p1_demand_power_active", 0)) # demand power l1
            # "p2_demand_power_active", 0)) # demand power l2
            # "p3_demand_power_active", 0)) # demand power l3
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

                block_0 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_0.add_32bit_int(1234)
                slave_ctx.setValues(3, 0, block_0.to_registers())

                block_770 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_770.add_16bit_int(4126) # Version and revision measurment module
                block_770.add_16bit_int(68)   # 
                block_770.add_16bit_int(4127) # Version and revision communication module
                block_770.add_16bit_int(67)   # 
                block_770.add_16bit_int(0)    # Current tariff 
                slave_ctx.setValues(3, 770, block_770.to_registers())

                block_848 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_848.add_16bit_int(4128) # Measurement module’s firmware CRC
                slave_ctx.setValues(3, 848, block_848.to_registers())

                block_20480 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_20480.add_string("MB24DINAV23XE1X") 
                slave_ctx.setValues(3, 20480, block_20480.to_registers())

                block_41216 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_41216.add_16bit_int(3) # Front selector status
                slave_ctx.setValues(3, 41216, block_41216.to_registers())

                block_4096 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_4096.add_16bit_int(9999) # PASSWORD
                block_4096.add_16bit_int(0)     # unused
                block_4096.add_16bit_int(0)    # Measuring system
                block_4096.add_32bit_int(10)   # Current transformer ratio
                block_4096.add_32bit_int(10)   # Voltage transformer ratio 
                block_4096.add_16bit_int(1)     # unused
                block_4096.add_16bit_int(2)     # unused
                block_4096.add_16bit_int(3)     # unused
                block_4096.add_16bit_int(4)     # unused
                block_4096.add_16bit_int(5)     # unused
                block_4096.add_16bit_int(6)     # unused
                block_4096.add_16bit_int(7)     # unused
                block_4096.add_16bit_int(8)     # unused
                block_4096.add_16bit_int(9)     # unused
                block_4096.add_32bit_int(15)   # Interval time 
                slave_ctx.setValues(3, 4096, block_4096.to_registers())

                block_4360 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_4360.add_16bit_int(2) # PASSWORD
                block_4360.add_16bit_int(2) # PASSWORD
                slave_ctx.setValues(3, 4360, block_4360.to_registers())

                block_40960 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_40960.add_16bit_int(1) # Type of application
                block_40960.add_16bit_int(3) # Default page for selector position “LOCK”
                block_40960.add_16bit_int(1) # Default page for selector position “1”
                block_40960.add_16bit_int(3) # Default page for selector position “2”
                block_40960.add_16bit_int(3) # Default page for selector position “kvarh”
                block_40960.add_16bit_int(1) # ID code of user 1
                block_40960.add_16bit_int(2) # ID code of user 2
                block_40960.add_16bit_int(3) # ID code of user 3
                slave_ctx.setValues(3, 40960, block_40960.to_registers())

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
