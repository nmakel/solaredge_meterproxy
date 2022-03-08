#!/usr/bin/env python3

import argparse
import configparser
import importlib
import logging
import sys
import threading
import time

sys.path.append('C:\gitHubClones\pymodbus')

from pymodbus.server.sync import StartTcpServer
from pymodbus.server.sync import ModbusTcpServer
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
            logger.info("Gavazzi Model number 1648 supplied")
            return [1648]
        return super().getValues(fx, address, count)



class ModbusMyTcpServer(ModbusTcpServer):
    clientCounter = 0

    def process_request(self, request, client):
        """ Callback for connecting a new client thread

        :param request: The request to handle
        :param client: The address of the client
        """
        self.clientCounter += 1
        logger = logging.getLogger()
        logger.info("Started thread to serve client at " + str(client) + " clientCounter = " + str(self.clientCounter))
        super().process_request(request,client)

    def shutdown(self):
        """ Stops the serve_forever loop.

        Overridden to signal handlers to stop.
        """
        logger = logging.getLogger()
        logger.info("shutdown to serve client")
        super().shutdown()

    def server_close(self):
        """ Callback for stopping the running server
        """
        logger = logging.getLogger()
        logger.debug("Modbus server stopped")
        super().server_close()


# --------------------------------------------------------------------------- #
# Creation Factorie
# --------------------------------------------------------------------------- #
def StartMyTcpServer(context=None, identity=None, address=None,
                   custom_functions=[], **kwargs):
    """ A factory to start and run a tcp modbus server

    :param context: The ModbusServerContext datastore
    :param identity: An optional identify structure
    :param address: An optional (interface, port) to bind to.
    :param custom_functions: An optional list of custom function classes
        supported by server instance.
    :param ignore_missing_slaves: True to not send errors on a request to a
                                      missing slave
    """
    framer = kwargs.pop("framer", ModbusSocketFramer)
    server = ModbusMyTcpServer(context, framer, identity, address, **kwargs)

    for f in custom_functions:
        server.decoder.register(f)
    server.serve_forever()


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
    block.add_16bit_uint(values.get("p1_current_int" , 0))
    block.add_16bit_uint(values.get("p2_current_int" , 0))
    block.add_16bit_uint(values.get("p3_current_int" , 0))
    block.add_16bit_int (values.get("current_scale_int" , 0))

    block.add_16bit_uint(values.get("voltage_ln_int" , 0))
    block.add_16bit_uint(values.get("p1n_voltage_int" , 0))
    block.add_16bit_uint(values.get("p2n_voltage_int" , 0))
    block.add_16bit_uint(values.get("p3n_voltage_int" , 0))
    block.add_16bit_uint(values.get("voltage_ll_int" , 0))
    block.add_16bit_uint(values.get("p1n_voltage_int" , 0))
    block.add_16bit_uint(values.get("p2n_voltage_int" , 0))
    block.add_16bit_uint(values.get("p3n_voltage_int" , 0))
    block.add_16bit_int (values.get("voltage_scale_int" , 0))
    
    block.add_16bit_uint(values.get("frequency_int" , 0))
    block.add_16bit_int (values.get("frequency_scale_int" , 0))

    block.add_16bit_int(values.get("power_int" , 0))
    block.add_16bit_int(values.get("p1_power_int" , 0))
    block.add_16bit_int(values.get("p2_power_int" , 0))
    block.add_16bit_int(values.get("p3_power_int" , 0))
    block.add_16bit_int (values.get("power_scale_int" , 0))

    block.add_16bit_int(values.get("power_apparent_int" , 0))
    block.add_16bit_int(values.get("p1_power_apparent_int" , 0))
    block.add_16bit_int(values.get("p2_power_apparent_int" , 0))
    block.add_16bit_int(values.get("p3_power_apparent_int" , 0))
    block.add_16bit_int (values.get("power_apparent_scale_int" , 0))

    block.add_16bit_int(values.get("power_reactive_int" , 0))
    block.add_16bit_int(values.get("p1_power_reactive_int" , 0))
    block.add_16bit_int(values.get("p2_power_reactive_int" , 0))
    block.add_16bit_int(values.get("p3_power_reactive_int" , 0))
    block.add_16bit_int (values.get("power_reactive_scale_int" , 0))

    block.add_16bit_int(values.get("power_factor_int" , 0))
    block.add_16bit_int(values.get("p1_power_factor_int" , 0))
    block.add_16bit_int(values.get("p2_power_factor_int" , 0))
    block.add_16bit_int(values.get("p3_power_factor_int" , 0))
    block.add_16bit_int (values.get("power_factor_scale_int" , 0))

    block.add_32bit_uint(values.get("export_energy_active_int" , 0))
    block.add_32bit_uint(values.get("p1_export_energy_active_int" , 0))
    block.add_32bit_uint(values.get("p2_export_energy_active_int" , 0))
    block.add_32bit_uint(values.get("p3_export_energy_active_int" , 0))
    block.add_32bit_uint(values.get("import_energy_active_int" , 0))
    block.add_32bit_uint(values.get("p1_import_energy_active_int" , 0))
    block.add_32bit_uint(values.get("p2_import_energy_active_int" , 0))
    block.add_32bit_uint(values.get("p3_import_energy_active_int" , 0))
    block.add_16bit_int (values.get("energy_active_scale_int" , 0))

    block.add_32bit_uint(values.get("export_energy_apparent_int", 0))
    block.add_32bit_uint(values.get("p1_export_energy_apparent_int" , 0))
    block.add_32bit_uint(values.get("p2_export_energy_apparent_int" , 0))
    block.add_32bit_uint(values.get("p3_export_energy_apparent_int" , 0))
    block.add_32bit_uint(values.get("import_energy_apparent_int" , 0))
    block.add_32bit_uint(values.get("p1_import_energy_apparent_int" , 0))
    block.add_32bit_uint(values.get("p2_import_energy_apparent_int" , 0))
    block.add_32bit_uint(values.get("p3_import_energy_apparent_int" , 0))
    block.add_16bit_int (values.get("energy_apparent_scale_int" , 0))

    block.add_32bit_uint(values.get("import_energy_reactive_q1_int" , 0))
    block.add_32bit_uint(values.get("p1_import_energy_reactive_q1_int" , 0))
    block.add_32bit_uint(values.get("p2_import_energy_reactive_q1_int" , 0))
    block.add_32bit_uint(values.get("p3_import_energy_reactive_q1_int" , 0))
    block.add_32bit_uint(values.get("import_energy_reactive_q2_int" , 0))
    block.add_32bit_uint(values.get("p1_import_energy_reactive_q2_int" , 0))
    block.add_32bit_uint(values.get("p2_import_energy_reactive_q2_int" , 0))
    block.add_32bit_uint(values.get("p3_import_energy_reactive_q2_int" , 0))
    block.add_32bit_uint(values.get("export_energy_reactive_q3_int" , 0))
    block.add_32bit_uint(values.get("p1_export_energy_reactive_q3_int" , 0))
    block.add_32bit_uint(values.get("p2_export_energy_reactive_q3_int" , 0))
    block.add_32bit_uint(values.get("p3_export_energy_reactive_q3_int" , 0))
    block.add_32bit_uint(values.get("export_energy_reactive_q4_int" , 0))
    block.add_32bit_uint(values.get("p1_export_energy_reactive_q4_int" , 0))
    block.add_32bit_uint(values.get("p2_export_energy_reactive_q4_int" , 0))
    block.add_32bit_uint(values.get("p3_export_energy_reactive_q4_int" , 0))
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

def t_update_se7k(ctx, stop, module, device, refresh):

    this_t = threading.currentThread()
    logger = logging.getLogger()

    try:
        values = module.values(device)

        if not values:
            return

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
        block_40000.add_16bit_uint(values.get("p1_current_int" , 0))
        block_40000.add_16bit_uint(values.get("p2_current_int" , 0))
        block_40000.add_16bit_uint(values.get("p3_current_int" , 0))
        block_40000.add_16bit_int (values.get("current_scale_int" , 0))

        block_40000.add_16bit_uint(values.get("p1_voltage_int" , 0))
        block_40000.add_16bit_uint(values.get("p2_voltage_int" , 0))
        block_40000.add_16bit_uint(values.get("p3_voltage_int" , 0))
        block_40000.add_16bit_uint(values.get("p1n_voltage_int" , 0))
        block_40000.add_16bit_uint(values.get("p2n_voltage_int" , 0))
        block_40000.add_16bit_uint(values.get("p3n_voltage_int" , 0))
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




def t_update(ctx, SE7K_CTX, stop, module, device, refresh):

    this_t = threading.currentThread()
    logger = logging.getLogger()

    while not stop.is_set():
        try:
            t_update_se7k(SE7K_CTX, stop, module, device, refresh)
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
            logger.info(meterValues['power']*10**meterValues['power_scale'])

            if logger.isEnabledFor(logging.DEBUG):
                logger.info("current:"+str(meterValues['current']))
                logger.info(str(meterValues['current']*10**meterValues['current_scale']))
                logger.info(meterValues['p1_current']*10**meterValues['current_scale'])
                logger.info(meterValues['p2_current']*10**meterValues['current_scale'])
                logger.info(meterValues['p3_current']*10**meterValues['current_scale'])
                logger.debug(meterValues['current_scale'])

                logger.debug("voltage_ln:"+str(meterValues['voltage_ln']))
                logger.debug(meterValues['voltage_ln']*10**meterValues['voltage_scale'])
                logger.debug(meterValues['p1n_voltage']*10**meterValues['voltage_scale'])
                logger.debug(meterValues['p2n_voltage']*10**meterValues['voltage_scale'])
                logger.debug(meterValues['p3n_voltage']*10**meterValues['voltage_scale'])
                logger.debug(meterValues['voltage_scale'])

                logger.debug("voltage_ll:"+str(meterValues['voltage_ll']))          
                logger.debug(meterValues['voltage_ll']*10**meterValues['voltage_scale'])
                logger.debug(meterValues['p12_voltage']*10**meterValues['voltage_scale'])
                logger.debug(meterValues['p23_voltage']*10**meterValues['voltage_scale'])
                logger.debug(meterValues['p31_voltage']*10**meterValues['voltage_scale'])
                logger.debug(meterValues['voltage_scale'])

                
                logger.info("frequency:"+str(meterValues['frequency']))          
                logger.info(meterValues['frequency']*10**meterValues['frequency_scale'])

                logger.info("power:"+str(meterValues['power']))          
                logger.info(meterValues['power']*10**meterValues['power_scale'])
                logger.info(meterValues['p1_power']*10**meterValues['power_scale'])
                logger.info(meterValues['p2_power']*10**meterValues['power_scale'])
                logger.info(meterValues['p3_power']*10**meterValues['power_scale'])
                logger.info(meterValues['power_scale'])

                logger.info("power_apparent:"+str(meterValues['power_apparent']))          
                logger.info(meterValues['power_apparent']*10**meterValues['power_apparent_scale'])
                logger.info(meterValues['p1_power_apparent']*10**meterValues['power_apparent_scale'])
                logger.info(meterValues['p2_power_apparent']*10**meterValues['power_apparent_scale'])
                logger.info(meterValues['p3_power_apparent']*10**meterValues['power_apparent_scale'])
                logger.info(meterValues['power_apparent_scale'])

                logger.info("power_reactive:"+str(meterValues['power_reactive']))          
                logger.info(meterValues['power_reactive']*10**meterValues['power_reactive_scale'])
                logger.info(meterValues['p1_power_reactive']*10**meterValues['power_reactive_scale'])
                logger.info(meterValues['p2_power_reactive']*10**meterValues['power_reactive_scale'])
                logger.info(meterValues['p3_power_reactive']*10**meterValues['power_reactive_scale'])
                logger.info(meterValues['power_reactive_scale'])

                logger.info("power_factor:"+str(meterValues['power_factor']))          
                logger.info(meterValues['power_factor']*10**meterValues['power_factor_scale'])
                logger.info(meterValues['p1_power_factor']*10**meterValues['power_factor_scale'])
                logger.info(meterValues['p2_power_factor']*10**meterValues['power_factor_scale'])
                logger.info(meterValues['p3_power_factor']*10**meterValues['power_factor_scale'])
                logger.info(meterValues['power_factor_scale'])

                logger.debug("export_energy_active:"+str(meterValues['export_energy_active']))          
                logger.debug(meterValues['export_energy_active']*10**meterValues['energy_active_scale'])
                logger.debug(meterValues['p1_export_energy_active']*10**meterValues['energy_active_scale'])
                logger.debug(meterValues['p2_export_energy_active']*10**meterValues['energy_active_scale'])
                logger.debug(meterValues['p3_export_energy_active']*10**meterValues['energy_active_scale'])
                logger.debug(meterValues['energy_active_scale'])

                logger.debug("import_energy_active:"+str(meterValues['import_energy_active']))          
                logger.debug(meterValues['import_energy_active']*10**meterValues['energy_active_scale'])
                logger.debug(meterValues['p1_import_energy_active']*10**meterValues['energy_active_scale'])
                logger.debug(meterValues['p2_import_energy_active']*10**meterValues['energy_active_scale'])
                logger.debug(meterValues['p3_import_energy_active']*10**meterValues['energy_active_scale'])
                logger.debug(meterValues['energy_active_scale'])

                logger.debug("import_energy_apparent:"+str(meterValues['import_energy_apparent']))          
                logger.debug(meterValues['import_energy_apparent']*10**meterValues['energy_apparent_scale'])
                logger.debug(meterValues['p1_import_energy_apparent']*10**meterValues['energy_apparent_scale'])
                logger.debug(meterValues['p2_import_energy_apparent']*10**meterValues['energy_apparent_scale'])
                logger.debug(meterValues['p3_import_energy_apparent']*10**meterValues['energy_apparent_scale'])
                logger.debug(meterValues['energy_apparent_scale'])


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
            block_0.add_32bit_int(meterValues['p1_power']*-10) # power l1   *10
            block_0.add_32bit_int(meterValues['p2_power']*-10) # power l2
            block_0.add_32bit_int(meterValues['p3_power']*-10) # power l3
            block_0.add_32bit_int(meterValues['p1_power_apparent']*-10) # apparent power l1   *10
            block_0.add_32bit_int(meterValues['p2_power_apparent']*-10) # apparent power l2
            block_0.add_32bit_int(meterValues['p3_power_apparent']*-10) # apparent power l3
            block_0.add_32bit_int(meterValues['p1_power_reactive']*-10) # reactive power l1   *10
            block_0.add_32bit_int(meterValues['p2_power_reactive']*-10) # reactive power l2
            block_0.add_32bit_int(meterValues['p3_power_reactive']*-10) # reactive power l3
            block_0.add_32bit_int(int(meterValues['voltage_ln']/10)) # l-n voltage                *10
            block_0.add_32bit_int(int(meterValues['voltage_ll']/10)) # l-l voltage
            block_0.add_32bit_int(meterValues['power']*-10) # total power              *10
            block_0.add_32bit_int(meterValues['power_apparent']*-10) # total apparent power
            block_0.add_32bit_int(meterValues['power_reactive']*-10) # total reactive power
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
            ctx.setValues(4, 0, block_0.to_registers())

            block_254 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
            block_254.add_32bit_int(2400) # hour    *100                                                         *100
            block_254.add_32bit_int(256)  # unused                                                       *100
            block_254.add_32bit_int(int(meterValues['voltage_ln']/10)) # l-n voltage                *10
            block_254.add_32bit_int(int(meterValues['voltage_ll']/10)) # l-l voltage
            block_254.add_32bit_int(meterValues['power']*-10) # total power              *10
            block_254.add_32bit_int(meterValues['power_apparent']*-10) # total apparent power
            block_254.add_32bit_int(meterValues['power_reactive']*-10) # total reactive power
            block_254.add_32bit_int(int(meterValues['power_factor']/10)) # power factor
            block_254.add_32bit_int(0) # Value –1 correspond to L1-L3-L2 sequence, value 0 correspond to L1-L2-L3 sequence (this value is meaningful only in case of 3-phase systems)
            block_254.add_32bit_int(int(meterValues['frequency']/10)) # line frequency           *10
            block_254.add_32bit_int(int(meterValues['import_energy_active']/100)) # imported active energy
            block_254.add_32bit_int(int(meterValues['import_energy_apparent']/100)) # imported active energy
            block_254.add_32bit_int(int(meterValues['export_energy_active']/100)) # total exported active energy non-reset   /100)
            block_254.add_32bit_int(int(meterValues['export_energy_apparent']/100)) # imported active energy non-reset
            block_254.add_32bit_int(56) # demand power
            block_254.add_32bit_int(58) # maximum demand power




            block_254.add_32bit_int(int(meterValues['p12_voltage']/10)) # l1-l2 voltage
            block_254.add_32bit_int(int(meterValues['p1n_voltage']/10)) # l1-n voltage    * 10
            block_254.add_32bit_int(meterValues['p1_current']*100) # current l1      * 1000
            block_254.add_32bit_int(meterValues['p1_power']*-10) # power l1   *10
            block_254.add_32bit_int(meterValues['p1_power_apparent']*-10) # apparent power l1   *10
            block_254.add_32bit_int(meterValues['p1_power_reactive']*-10) # reactive power l1   *10
            block_254.add_32bit_int(int(meterValues['p1_power_factor']/10)) # power factor l1       *1000

            block_254.add_32bit_int(int(meterValues['p23_voltage']/10)) # l2-l3 voltage
            block_254.add_32bit_int(int(meterValues['p2n_voltage']/10)) # l2-n voltage
            block_254.add_32bit_int(meterValues['p2_current']*100) # current l2
            block_254.add_32bit_int(meterValues['p2_power']*-10) # power l2
            block_254.add_32bit_int(meterValues['p2_power_apparent']*-10) # apparent power l2
            block_254.add_32bit_int(meterValues['p2_power_reactive']*-10) # reactive power l2
            block_254.add_32bit_int(int(meterValues['p2_power_factor']/10)) # power factor l2

            block_254.add_32bit_int(int(meterValues['p31_voltage']/10)) # l3-l1 voltage
            block_254.add_32bit_int(int(meterValues['p3n_voltage']/10)) # l3-n voltage
            block_254.add_32bit_int(meterValues['p3_current']*100) # current l3
            block_254.add_32bit_int(meterValues['p3_power']*-10) # power l3
            block_254.add_32bit_int(meterValues['p3_power_apparent']*-10) # apparent power l3
            block_254.add_32bit_int(meterValues['p3_power_reactive']*-10) # reactive power l3
            block_254.add_32bit_int(int(meterValues['p3_power_factor']/10)) # power factor l3

            block_254.add_32bit_int(0) # Value –1 correspond to L1-L3-L2 sequence, value 0 correspond to L1-L2-L3 sequence (this value is meaningful only in case of 3-phase systems)
            
            block_254.add_32bit_int(int(meterValues['import_energy_active']/100)) # imported active energy
            block_254.add_32bit_int(int(meterValues['import_energy_apparent']/100)) # imported active energy
            block_254.add_32bit_int(int(meterValues['p1_import_energy_active']/100)) # imported active energy l1
            block_254.add_32bit_int(int(meterValues['p2_import_energy_active']/100)) # imported active energy l2
            block_254.add_32bit_int(int(meterValues['p3_import_energy_active']/100)) # imported active energy l3
            block_254.add_32bit_int(10) # total active energy Tarif 1
            block_254.add_32bit_int(20) # total active energy Tarif 2
            block_254.add_32bit_int(30) # total active energy Tarif 3
            block_254.add_32bit_int(40) # total active energy Tarif 4
            block_254.add_32bit_int(346)  # unused                                                       *100
            block_254.add_32bit_int(348)  # unused                                                       *100
            block_254.add_32bit_int(350)  # unused                                                       *100
            block_254.add_32bit_int(352)  # unused                                                       *100
            block_254.add_32bit_int(11) # total apparent energy Tarif 1                                      *10
            block_254.add_32bit_int(22) # total apparent energy Tarif 2
            block_254.add_32bit_int(33) # total apparent energy Tarif 3
            block_254.add_32bit_int(44) # total apparent energy Tarif 4
            block_254.add_32bit_int(262)  # unused                                                       *100
            block_254.add_32bit_int(264)  # unused                                                       *100
            block_254.add_32bit_int(266)  # unused                                                       *100
            block_254.add_32bit_int(268)  # unused                                                       *100
            block_254.add_32bit_int(270)  # unused                                                       *100
            block_254.add_32bit_int(272)  # unused                                                       *100
            block_254.add_32bit_int(274)  # unused                                                       *100
            block_254.add_32bit_int(276)  # unused                                                       *100
            block_254.add_32bit_int(118) # apparent demand power
            block_254.add_32bit_int(120) # apparent demand power max
            block_254.add_32bit_int(122) # DMD A max                        *10
            ctx.setValues(3, 254, block_254.to_registers())
            ctx.setValues(4, 254, block_254.to_registers())

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
            time.sleep(0.6)


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

                EM24_slave_ctx = EM24SlaveContext()
                SE7K_slave_ctx = ModbusSlaveContext()

                # block_11 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                # block_11.add_16bit_int(1648)
                # EM24_slave_ctx.setValues(3, 11, block_11.to_registers())
                # EM24_slave_ctx.setValues(4, 11, block_11.to_registers())

                block_0 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_0.add_32bit_int(1234)
                EM24_slave_ctx.setValues(3, 0, block_0.to_registers())
                EM24_slave_ctx.setValues(4, 0, block_0.to_registers())

                block_770 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_770.add_16bit_int(4126) # Version and revision measurment module
                block_770.add_16bit_int(68)   # 
                block_770.add_16bit_int(4127) # Version and revision communication module
                block_770.add_16bit_int(67)   # 
                block_770.add_16bit_int(0)    # Current tariff 
                EM24_slave_ctx.setValues(3, 770, block_770.to_registers())
                EM24_slave_ctx.setValues(4, 770, block_770.to_registers())

                block_848 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_848.add_16bit_int(4128) # Measurement module’s firmware CRC
                EM24_slave_ctx.setValues(3, 848, block_848.to_registers())
                EM24_slave_ctx.setValues(4, 848, block_848.to_registers())

                block_20480 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_20480.add_string("MB24DINAV23XE1X") 
                EM24_slave_ctx.setValues(3, 20480, block_20480.to_registers())
                EM24_slave_ctx.setValues(4, 20480, block_20480.to_registers())

                block_41216 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_41216.add_16bit_int(3) # Front selector status
                EM24_slave_ctx.setValues(3, 41216, block_41216.to_registers())
                EM24_slave_ctx.setValues(4, 41216, block_41216.to_registers())

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
                EM24_slave_ctx.setValues(3, 4096, block_4096.to_registers())
                EM24_slave_ctx.setValues(4, 4096, block_4096.to_registers())

                block_4360 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_4360.add_16bit_int(2) # PASSWORD
                block_4360.add_16bit_int(2) # PASSWORD
                EM24_slave_ctx.setValues(3, 4360, block_4360.to_registers())
                EM24_slave_ctx.setValues(4, 4360, block_4360.to_registers())

                block_40960 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                block_40960.add_16bit_int(1) # Type of application
                block_40960.add_16bit_int(3) # Default page for selector position “LOCK”
                block_40960.add_16bit_int(1) # Default page for selector position “1”
                block_40960.add_16bit_int(3) # Default page for selector position “2”
                block_40960.add_16bit_int(3) # Default page for selector position “kvarh”
                block_40960.add_16bit_int(1) # ID code of user 1
                block_40960.add_16bit_int(2) # ID code of user 2
                block_40960.add_16bit_int(3) # ID code of user 3
                EM24_slave_ctx.setValues(3, 40960, block_40960.to_registers())
                EM24_slave_ctx.setValues(4, 40960, block_40960.to_registers())

                update_t_stop = threading.Event()
                update_t = threading.Thread(
                    target=t_update,
                    name=f"t_update_{address}",
                    args=(
                        EM24_slave_ctx,
                        SE7K_slave_ctx,
                        update_t_stop,
                        meter_module,
                        meter_device,
                        confparser[meter].getfloat("refresh_rate", fallback=default_config["meters"]["refresh_rate"])
                    )
                )

                threads.append(update_t)
                thread_stops.append(update_t_stop)

                slaves.update({1: EM24_slave_ctx})
                slaves.update({2: SE7K_slave_ctx})
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

        StartMyTcpServer(
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
