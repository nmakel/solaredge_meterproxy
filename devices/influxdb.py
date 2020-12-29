import logging
import requests
import sys

import influxdb


def device(config):

    # Configuration parameters:
    #
    # host          ip or hostname
    # port          influxdb port
    # database      database name
    # bucket        bucket name
    # where_key     tag name identifying the meter
    # where_value   tag value identifying the meter

    logger = logging.getLogger()

    host = config.get("host", fallback="localhost")
    port = config.getint("port", fallback=8086)
    database = config.get("database", fallback="measurements")
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

    logger = logging.getLogger()
    logger.debug(f"device: {device}")
    
    if device["where_key"] and device["where_value"]:
        values = list(device["client"].query(
            f'SELECT last(*) FROM "{device["bucket"]}" WHERE ("{device["where_key"]}" = \'{device["where_value"]}\')'
        ).get_points())[0]
    else:
        values = list(device["client"].query(
            f'SELECT last(*) FROM "{device["bucket"]}"'
        ).get_points())[0]

    logger.debug(f"values: {values}")

    return {
        "energy_active": values.get("last_total_energy_active", 0),
        "import_energy_active": values.get("last_import_energy_active", 0),
        "power_active": values.get("last_power_active", 0),
        "p1_power_active": values.get("last_power_active", 0),
        # "p2_power_active"
        # "p3_power_active"
        "voltage_ln": values.get("last_voltage", 0),
        "p1n_voltage": values.get("last_voltage", 0),
        # "p2n_voltage"
        # "p3n_voltage"
        # "voltage_ll"
        # "p12_voltage"
        # "p23_voltage"
        # "p31_voltage"
        "frequency": values.get("last_frequency", 0),
        "p1_energy_active": values.get("last_total_energy_active", 0),
        # "p2_energy_active"
        # "p3_energy_active"
        "p1_import_energy_active": values.get("last_import_energy_active", 0),
        # "p2_import_energy_active"
        # "p3_import_energy_active"
        "export_energy_active": values.get("last_export_energy_active", 0),
        "p1_export_energy_active": values.get("last_export_energy_active", 0),
        # "p2_export_energy_active"
        # "p3_export_energy_active"
        "energy_reactive": values.get("last_total_energy_reactive", 0),
        "p1_energy_reactive": values.get("last_total_energy_reactive", 0),
        # "p2_energy_reactive"
        # "p3_energy_reactive"
        # "energy_apparent"
        # "p1_energy_apparent"
        # "p2_energy_apparent"
        # "p3_energy_apparent"
        "power_factor": values.get("last_power_factor", 0),
        "p1_power_factor": values.get("last_power_factor", 0),
        # "p2_power_factor"
        # "p3_power_factor"
        "power_reactive": values.get("last_power_reactive", 0),
        "p1_power_reactive": values.get("last_power_reactive", 0),
        # "p2_power_reactive"
        # "p3_power_reactive"
        "power_apparent": values.get("last_power_apparent", 0),
        "p1_power_apparent": values.get("last_power_apparent", 0),
        # "p2_power_apparent"
        # "p3_power_apparent"
        "p1_current": values.get("last_current", 0),
        # "p2_current"
        # "p3_current"
        "demand_power_active": values.get("last_total_demand_power_active", 0),
        # "minimum_demand_power_active"
        "maximum_demand_power_active": values.get("last_maximum_total_demand_power_active", 0),
        # "demand_power_apparent"
        "p1_demand_power_active": values.get("last_total_demand_power_active", 0),
        # "p2_demand_power_active"
        # "p3_demand_power_active"
    }
