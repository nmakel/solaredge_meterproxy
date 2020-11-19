import sdm_modbus


def device(
        host=False, port=False,
        device=False, stopbits=False, parity=False, baud=False,
        timeout=False, retries=False, unit=False,
        extended=False
    ):

    if device:
        return sdm_modbus.SDM630(
            device=device,
            stopbits=stopbits,
            parity=parity,
            baud=baud,
            timeout=timeout,
            unit=unit
        )
    else:
        return sdm_modbus.SDM630(
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
