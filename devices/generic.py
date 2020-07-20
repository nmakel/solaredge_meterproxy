def device(
        host=False, port=False,
        device=False, stopbits=False, parity=False, baud=False,
        timeout=False, retries=False, unit=False
    ):
    return False


def values(device):
    if not device:
        return {}

    return {
        # "energy_active"
        # "import_energy_active"
        # "power_active"
        # "p1_power_active"
        # "p2_power_active"
        # "p3_power_active"
        # "voltage_ln"
        # "p1n_voltage"
        # "p2n_voltage"
        # "p3n_voltage"
        # "voltage_ll"
        # "p12_voltage"
        # "p23_voltage"
        # "p31_voltage"
        # "frequency"
        # "p1_energy_active"
        # "p2_energy_active"
        # "p3_energy_active"
        # "p1_import_energy_active"
        # "p2_import_energy_active"
        # "p3_import_energy_active"
        # "export_energy_active"
        # "p1_export_energy_active"
        # "p2_export_energy_active"
        # "p3_export_energy_active"
        # "energy_reactive"
        # "p1_energy_reactive"
        # "p2_energy_reactive"
        # "p3_energy_reactive"
        # "energy_apparent"
        # "p1_energy_apparent"
        # "p2_energy_apparent"
        # "p3_energy_apparent"
        # "power_factor"
        # "p1_power_factor"
        # "p2_power_factor"
        # "p3_power_factor"
        # "power_reactive"
        # "p1_power_reactive"
        # "p2_power_reactive"
        # "p3_power_reactive"
        # "power_apparent"
        # "p1_power_apparent"
        # "p2_power_apparent"
        # "p3_power_apparent"
        # "p1_current"
        # "p2_current"
        # "p3_current"
        # "demand_power_active"
        # "minimum_demand_power_active"
        # "maximum_demand_power_active"
        # "demand_power_apparent"
        # "p1_demand_power_active"
        # "p2_demand_power_active"
        # "p3_demand_power_active"
    }
