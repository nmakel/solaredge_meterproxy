import influxdb
import logging
import requests
import sys


def device(config):

    # Configuration parameters:
    # 
    # host          ip or hostname of influxdb server
    # port          influxdb port
    # database      database name
    # bucket        bucket name
    # where_key     tag name identifying the meter values
    # where_value   tag value identifying the meter values

    logger = logging.getLogger()

    host = config.get("host", fallback=False)
    port = config.getint("port", fallback=False)
    database = config.get("database", fallback=False)
    bucket = config.get("bucket", fallback=False)
    where_key = config.get("where_key", fallback=False)
    where_value = config.get("where_value", fallback=False)

    try:
        client = influxdb.InfluxDBClient(host=host, port=port)
        client.switch_database(database)
        client.ping()

        logger.debug(f"connected to database: {host}:{port}/{database}")
    except (ConnectionRefusedError, requests.exceptions.ConnectionError):
        logger.critical(f"database connection failed: {host}:{port}/{database}")
        sys.exit()

    return {
        "client": client,
        "bucket": bucket,
        "where_key": where_key,
        "where_value": where_value
    }


def values(device):

    if not device:
        return {}

    values = list(device["client"].query(
        f'SELECT last(*) FROM "{device["bucket"]}" WHERE ("{device["where_key"]}" = \'{device["where_value"]}\')'
    ).get_points())[0]

    return {
        "energy_active": values.get("last_total_energy_active", 0),
        "import_energy_active": values.get("last_import_energy_active", 0),
        "power_active": values.get("last_power_active", 0),
        "p1_power_active": values.get("last_p1_power_active", 0),
        "p2_power_active": values.get("last_p2_power_active", 0),
        "p3_power_active": values.get("last_p3_power_active", 0),
        "voltage_ln": values.get("last_voltage", 0),
        "p1n_voltage": values.get("last_p1n_voltage", 0),
        "p2n_voltage": values.get("last_p2n_voltage", 0),
        "p3n_voltage": values.get("last_p3n_voltage", 0),
        "voltage_ll": values.get("last_voltage_ll", 0),
        "p12_voltage": values.get("last_p12_voltage", 0),
        "p23_voltage": values.get("last_p23_voltage", 0),
        "p31_voltage": values.get("last_p31_voltage", 0),
        "frequency": values.get("last_frequency", 0),
        "p1_energy_active": values.get("last_p1_energy_active", 0),
        "p2_energy_active": values.get("last_p2_energy_active", 0),
        "p3_energy_active": values.get("last_p3_energy_active", 0),
        "p1_import_energy_active": values.get("last_p1_import_energy_active", 0),
        "p2_import_energy_active": values.get("last_p2_import_energy_active", 0),
        "p3_import_energy_active": values.get("last_p3_import_energy_active", 0),
        "export_energy_active": values.get("last_export_energy_active", 0),
        "p1_export_energy_active": values.get("last_p1_export_energy_active", 0),
        "p2_export_energy_active": values.get("last_p2_export_energy_active", 0),
        "p3_export_energy_active": values.get("last_p3_export_energy_active", 0),
        "energy_reactive": values.get("last_total_energy_reactive", 0),
        "p1_energy_reactive": values.get("last_p1_energy_reactive", 0),
        "p2_energy_reactive": values.get("last_p2_energy_reactive", 0),
        "p3_energy_reactive": values.get("last_p3_energy_reactive", 0),
        "energy_apparent": values.get("last_energy_apparent", 0),
        "p1_energy_apparent": values.get("last_p1_energy_apparent", 0),
        "p2_energy_apparent": values.get("last_p2_energy_apparent", 0),
        "p3_energy_apparent": values.get("last_p3_energy_apparent", 0),
        "power_factor": values.get("last_power_factor", 0),
        "p1_power_factor": values.get("last_p1_power_factor", 0),
        "p2_power_factor": values.get("last_p2_power_factor", 0),
        "p3_power_factor": values.get("last_p3_power_factor", 0),
        "power_reactive": values.get("last_power_reactive", 0),
        "p1_power_reactive": values.get("last_p1_power_reactive", 0),
        "p2_power_reactive": values.get("last_p2_power_reactive", 0),
        "p3_power_reactive": values.get("last_p3_power_reactive", 0),
        "power_apparent": values.get("last_power_apparent", 0),
        "p1_power_apparent": values.get("last_p1_power_apparent", 0),
        "p2_power_apparent": values.get("last_p2_power_apparent", 0),
        "p3_power_apparent": values.get("last_p3_power_apparent", 0),
        "p1_current": values.get("last_p1_current", 0),
        "p2_current": values.get("last_p2_current", 0),
        "p3_current": values.get("last_p3_current", 0),
        "demand_power_active": values.get("last_total_demand_power_active", 0),
        "minimum_demand_power_active": values.get("last_minimum_demand_power_active", 0),
        "maximum_demand_power_active": values.get("last_maximum_total_demand_power_active", 0),
        "demand_power_apparent": values.get("last_demand_power_apparent", 0),
        "p1_demand_power_active": values.get("last_total_demand_power_active", 0),
        "p2_demand_power_active": values.get("last_p2_demand_power_active", 0),
        "p3_demand_power_active": values.get("last_p3_demand_power_active", 0),
    }
