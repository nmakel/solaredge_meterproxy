import sdm_modbus

def device(
        host=False, port=False,
        device=False, stopbits=False, parity=False, baud=False,
        timeout=False, retries=False, unit=False
    ):

    if device:
        return sdm_modbus.SDM120(
            device=device,
            stopbits=stopbits,
            parity=parity,
            baudrate=baud,
            timeout=timeout,
            unit=unit
        )
    else:
        return sdm_modbus.SDM120(
            host=host,
            port=port,
            timeout=timeout,
            unit=unit
        )

def values(device):
    new = device.read_all()
    
    return {
        "energy_active": new.get("total_energy_active", 0),
        "p1_energy_active": new.get("total_energy_active", 0),
        "import_energy_active": new.get("import_energy_active", 0),
        "p1_import_energy_active": new.get("import_energy_active", 0),
        "power_active": new.get("power_active", 0),
        "p1_power_active": new.get("power_active", 0),
        "voltage_ln": new.get("voltage", 0),
        "p1n_voltage": new.get("voltage", 0),
        "frequency": new.get("frequency", 0),
        "export_energy_active": new.get("export_energy_active", 0),
        "p1_export_energy_active": new.get("export_energy_active", 0),
        "energy_reactive": new.get("total_energy_reactive", 0),
        "p1_energy_reactive": new.get("total_energy_reactive", 0),
        "power_factor": new.get("power_factor", 0),
        "p1_power_factor": new.get("power_factor", 0),
        "power_reactive": new.get("power_reactive", 0),
        "p1_power_reactive": new.get("power_reactive", 0),
        "power_apparent": new.get("power_apparent", 0),
        "p1_power_apparent": new.get("power_apparent", 0),
        "current": new.get("current", 0),
        "p1_current": new.get("current", 0),
        "demand_power_active": new.get("total_demand_power_active", 0),
        "p1_demand_power_active": new.get("total_demand_power_active", 0),
        "maximum_demand_power_active": new.get("maximum_total_demand_power_active", 0)
    }