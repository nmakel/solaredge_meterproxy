import logging
import re
import solaredge_modbus


def device(config):

    # Configuration parameters:
    #
    # timeout   seconds to wait for a response, default: 1
    # retries   number of retries, default: 3
    # unit      modbus address, default: 1
    #
    # For Modbus TCP:
    # host      ip or hostname
    # port      modbus tcp port
    #
    # For Modbus RTU:
    # device    serial device, e.g. /dev/ttyUSB0
    # stopbits  number of stop bits
    # parity    parity setting, N, E or O
    # baud      baud rate

    timeout = config.getint("timeout", fallback=1)
    retries = config.getint("retries", fallback=3)
    unit = config.getint("src_address", fallback=1)

    host = config.get("host", fallback=False)
    port = config.getint("port", fallback=False)
    device = config.get("device", fallback=False)

    if device:
        stopbits = config.getint("stopbits", fallback=1)
        parity = config.get("parity", fallback="N")
        baud = config.getint("baud", fallback=2400)

        if (parity
                and parity.upper() in ["N", "E", "O"]):
            parity = parity.upper()
        else:
            parity = False

        return solaredge_modbus.Inverter(
            device=device,
            stopbits=stopbits,
            parity=parity,
            baud=baud,
            timeout=timeout,
            retries=retries,
            unit=unit
        )
    else:
        return solaredge_modbus.Inverter(
            host=host,
            port=port,
            timeout=timeout,
            retries=retries,
            unit=unit
        )


def values(device):
    if not device:
        return {}

    logger = logging.getLogger()
    logger.debug(f"device: {device}")

    values = {}
    inverter_values=device.read_all()
    
    # append type to key to prevent key name collision with legacy values
    values = {key+'_'+re.search('\'(.*)\'',str(type(value))).group(1):value for key, value in inverter_values.items()}  
    
    meters = device.meters()
    batteries = device.batteries()
    values["connected_meters"] = {}
    values["connected_batteries"] = {}

    for meter, params in meters.items():
        meter_values = params.read_all()
        values["connected_meters"][meter] = {key+'_'+re.search('\'(.*)\'',str(type(value))).group(1):value for key, value in meter_values.items()}

    for battery, params in batteries.items():
        battery_values = params.read_all()
        values["connected_batteries"][battery] = {key+'_'+re.search('\'(.*)\'',str(type(value))).group(1):value for key, value in battery_values.items()}

    logger.debug(f"values: {values}")

    # additional values for emulation of SE-WNC-3Y-400-MB-K1 or WattNode WNC-3Y-400-MB

    # TODO Calculate the values for the SE-WNC-3Y-400-MB-K1 meter from the SolarEdge meter provided by SE7K
    SE_WNC_3Y_400_MB_K1_values = {
        "energy_active": values.get("total_energy_active", 0),
        "import_energy_active": values.get("import_energy_active", 0),
        "power_active": values.get("total_power_active", 0),
        "p1_power_active": values.get("p1_power_active", 0),
        "p2_power_active": values.get("p2_power_active", 0),
        "p3_power_active": values.get("p3_power_active", 0),
        "voltage_ln": values.get("voltage_ln", 0),
        "p1n_voltage": values.get("p1_voltage", 0),
        "p2n_voltage": values.get("p2_voltage", 0),
        "p3n_voltage": values.get("p3_voltage", 0),
        "voltage_ll": values.get("voltage_ll", 0),
        "p12_voltage": values.get("p12_voltage", 0),
        "p23_voltage": values.get("p23_voltage", 0),
        "p31_voltage": values.get("p31_voltage", 0),
        "frequency": values.get("frequency", 0),
        "p1_energy_active": values.get("total_energy_active", 0),
        # "p2_energy_active"
        # "p3_energy_active"
        "p1_import_energy_active": values.get("import_energy_active", 0),
        # "p2_import_energy_active"
        # "p3_import_energy_active"
        "export_energy_active": values.get("export_energy_active", 0),
        "p1_export_energy_active": values.get("export_energy_active", 0),
        # "p2_export_energy_active"
        # "p3_export_energy_active"
        "energy_reactive": values.get("total_energy_reactive", 0),
        "p1_energy_reactive": values.get("total_energy_reactive", 0),
        # "p2_energy_reactive"
        # "p3_energy_reactive"
        "energy_apparent": values.get("total_energy_apparent", 0),
        "p1_energy_apparent": values.get("total_energy_apparent", 0),
        # "p2_energy_apparent"
        # "p3_energy_apparent"
        "power_factor": values.get("total_power_factor", 0),
        "p1_power_factor": values.get("p1_power_factor", 0),
        "p2_power_factor": values.get("p2_power_factor", 0),
        "p3_power_factor": values.get("p3_power_factor", 0),
        "power_reactive": values.get("total_power_reactive", 0),
        "p1_power_reactive": values.get("p1_power_reactive", 0),
        "p2_power_reactive": values.get("p2_power_reactive", 0),
        "p3_power_reactive": values.get("p3_power_reactive", 0),
        "power_apparent": values.get("total_power_apparent", 0),
        "p1_power_apparent": values.get("p1_power_apparent", 0),
        "p2_power_apparent": values.get("p2_power_apparent", 0),
        "p3_power_apparent": values.get("p3_power_apparent", 0),
        "p1_current": values.get("p1_current", 0),
        "p2_current": values.get("p2_current", 0),
        "p3_current": values.get("p3_current", 0),
        "demand_power_active": values.get("total_import_demand_power_active", 0),
        # "minimum_demand_power_active"
        "maximum_demand_power_active": values.get("maximum_import_demand_power_active", 0),
        "demand_power_apparent": values.get("total_demand_power_apparent", 0),
        "p1_demand_power_active": (values.get("p1_demand_current", 0) * values.get("p1_voltage", 0)),
        "p2_demand_power_active": (values.get("p2_demand_current", 0) * values.get("p2_voltage", 0)),
        "p3_demand_power_active": (values.get("p3_demand_current", 0) * values.get("p3_voltage", 0))
    }


    return values | SE_WNC_3Y_400_MB_K1_values  
    # append type to key