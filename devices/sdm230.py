import sdm_modbus


def device(
        host=False, port=False,
        device=False, stopbits=False, parity=False, baud=False,
        timeout=False, retries=False, unit=False,
        extended=False
    ):

    if device:
        return sdm_modbus.SDM230(
            device=device,
            stopbits=stopbits,
            parity=parity,
            baud=baud,
            timeout=timeout,
            unit=unit
        )
    else:
        return sdm_modbus.SDM230(
            host=host,
            port=port,
            timeout=timeout,
            unit=unit
        )


def values(device):
    values = device.read_all()

    return {
        "energy_active": values.get("total_energy_active", 0),
        "import_energy_active": values.get("import_energy_active", 0),
        "power_active": values.get("power_active", 0),
        "p1_power_active": values.get("power_active", 0),
        # "p2_power_active"
        # "p3_power_active"
        "voltage_ln": values.get("voltage", 0),
        "p1n_voltage": values.get("voltage", 0),
        # "p2n_voltage"
        # "p3n_voltage"
        # "voltage_ll"
        # "p12_voltage"
        # "p23_voltage"
        # "p31_voltage"
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
        # "energy_apparent"
        # "p1_energy_apparent"
        # "p2_energy_apparent"
        # "p3_energy_apparent"
        "power_factor": values.get("power_factor", 0),
        "p1_power_factor": values.get("power_factor", 0),
        # "p2_power_factor"
        # "p3_power_factor"
        "power_reactive": values.get("power_reactive", 0),
        "p1_power_reactive": values.get("power_reactive", 0),
        # "p2_power_reactive"
        # "p3_power_reactive"
        "power_apparent": values.get("power_apparent", 0),
        "p1_power_apparent": values.get("power_apparent", 0),
        # "p2_power_apparent"
        # "p3_power_apparent"
        "p1_current": values.get("current", 0),
        # "p2_current"
        # "p3_current"
        "demand_power_active": values.get("total_demand_power_active", 0),
        # "minimum_demand_power_active"
        "maximum_demand_power_active": values.get("maximum_total_demand_power_active", 0),
        # "demand_power_apparent"
        "p1_demand_power_active": values.get("total_demand_power_active", 0),
        # "p2_demand_power_active"
        # "p3_demand_power_active"
    }
