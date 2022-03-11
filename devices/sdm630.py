import logging

import sdm_modbus


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
        baud = config.getint("baud", fallback=9600)

        if (parity
                and parity.upper() in ["N", "E", "O"]):
            parity = parity.upper()
        else:
            parity = False

        return sdm_modbus.SDM630(
            device=device,
            stopbits=stopbits,
            parity=parity,
            baud=baud,
            timeout=timeout,
            retries=retries,
            unit=unit
        )
    else:
        return sdm_modbus.SDM630(
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

    values = device.read_all()

    logger.debug(f"values: {values}")

    return {
        "energy_active": values.get("total_energy_active", 0),
        "import_energy_active": values.get("import_energy_active", 0),
        "power_active": values.get("total_power_active", 0),
        "l1_power_active": values.get("l1_power_active", 0),
        "l2_power_active": values.get("l2_power_active", 0),
        "l3_power_active": values.get("l3_power_active", 0),
        "voltage_ln": values.get("voltage_ln", 0),
        "l1n_voltage": values.get("l1_voltage", 0),
        "l2n_voltage": values.get("l2_voltage", 0),
        "l3n_voltage": values.get("l3_voltage", 0),
        "voltage_ll": values.get("voltage_ll", 0),
        "l12_voltage": values.get("l12_voltage", 0),
        "l23_voltage": values.get("l23_voltage", 0),
        "l31_voltage": values.get("l31_voltage", 0),
        "frequency": values.get("frequency", 0),
        "l1_energy_active": values.get("total_energy_active", 0),
        # "l2_energy_active"
        # "l3_energy_active"
        "l1_import_energy_active": values.get("import_energy_active", 0),
        # "l2_import_energy_active"
        # "l3_import_energy_active"
        "export_energy_active": values.get("export_energy_active", 0),
        "l1_export_energy_active": values.get("export_energy_active", 0),
        # "l2_export_energy_active"
        # "l3_export_energy_active"
        "energy_reactive": values.get("total_energy_reactive", 0),
        "l1_energy_reactive": values.get("total_energy_reactive", 0),
        # "l2_energy_reactive"
        # "l3_energy_reactive"
        "energy_apparent": values.get("total_energy_apparent", 0),
        "l1_energy_apparent": values.get("total_energy_apparent", 0),
        # "l2_energy_apparent"
        # "l3_energy_apparent"
        "power_factor": values.get("total_power_factor", 0),
        "l1_power_factor": values.get("l1_power_factor", 0),
        "l2_power_factor": values.get("l2_power_factor", 0),
        "l3_power_factor": values.get("l3_power_factor", 0),
        "power_reactive": values.get("total_power_reactive", 0),
        "l1_power_reactive": values.get("l1_power_reactive", 0),
        "l2_power_reactive": values.get("l2_power_reactive", 0),
        "l3_power_reactive": values.get("l3_power_reactive", 0),
        "power_apparent": values.get("total_power_apparent", 0),
        "l1_power_apparent": values.get("l1_power_apparent", 0),
        "l2_power_apparent": values.get("l2_power_apparent", 0),
        "l3_power_apparent": values.get("l3_power_apparent", 0),
        "l1_current": values.get("l1_current", 0),
        "l2_current": values.get("l2_current", 0),
        "l3_current": values.get("l3_current", 0),
        "demand_power_active": values.get("total_import_demand_power_active", 0),
        # "minimum_demand_power_active"
        "maximum_demand_power_active": values.get("maximum_import_demand_power_active", 0),
        "demand_power_apparent": values.get("total_demand_power_apparent", 0),
        "l1_demand_power_active": (values.get("l1_demand_current", 0) * values.get("l1_voltage", 0)),
        "l2_demand_power_active": (values.get("l2_demand_current", 0) * values.get("l2_voltage", 0)),
        "l3_demand_power_active": (values.get("l3_demand_current", 0) * values.get("l3_voltage", 0))
    }
