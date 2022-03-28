import datetime
import json
import logging
import sys
import time

import paho.mqtt.client as mqtt

lastValues = {}
logger = logging.getLogger()


def on_connect(client, userdata, flags, rc):
    logger.info(
        f"MQTT connected to {userdata['host']}:{userdata['port']} - topic: '{userdata['meterValuesTopic']}' with result code {rc}.")
    client.subscribe(userdata["meterValuesTopic"])
    if userdata['willTopic'] is not None:
        client.publish(userdata['willTopic'], "MeterProxy Connected " +
                       str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))


def on_message(client, userdata, message):
    global lastValues
    logger.debug(F'Received message: {message.payload.decode("utf-8")}')
    decoded_message = str(message.payload.decode("utf-8"))
    lastValues = json.loads(decoded_message)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.info(F"Unexpected MQTT disconnection, with result code {rc}.")


def device(config):

    # Configuration parameters:
    #
    # host              ip or hostname of MQTT server
    # port              port of MQTT server
    # keepalive         keepalive time in seconds for MQTT server
    # meterValuesTopic  MQTT topic to subscribe to to receive meter values

    host = config.get("host", fallback="localhost")
    port = config.getint("port", fallback=1883)
    keepalive = config.getint("keepalive", fallback=60)
    meterValuesTopic = config.get("meterValuesTopic", fallback="meter")
    willTopic = config.get("willTopic", fallback=None)
    willMsg = config.get("willMsg", fallback="MeterProxy Disconnected")

    topics = {
        "host": host,
        "port": port,
        "meterValuesTopic": meterValuesTopic,
        "willTopic": willTopic
    }

    try:
        client = mqtt.Client(userdata=topics)
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        if willTopic is not None:
            client.will_set(willTopic, payload=willMsg, qos=0, retain=False)
        client.connect(host, port, keepalive)
        client.loop_start()
        logger.debug(
            f"Started MQTT connection to server - topic: {host}:{port}  - {meterValuesTopic}")
    except:
        logger.critical(
            f"MQTT connection failed: {host}:{port} - {meterValuesTopic}")

    return {
        "client": client,
        "host": host,
        "port": port,
        "keepalive": keepalive,
        "meterValuesTopic": meterValuesTopic,
        "willTopic": willTopic,
        "willMsg": willMsg
    }


def values(device):
    if not device:
        return {}
    return lastValues

    #  MQTT input is a json with one or more of the below elements
    # "energy_active"
    # "import_energy_active"
    # "power_active"
    # "l1_power_active"
    # "l2_power_active"
    # "l3_power_active"
    # "voltage_ln"
    # "l1n_voltage"
    # "l2n_voltage"
    # "l3n_voltage"
    # "voltage_ll"
    # "l12_voltage"
    # "l23_voltage"
    # "l31_voltage"
    # "frequency"
    # "l1_energy_active"
    # "l2_energy_active"
    # "l3_energy_active"
    # "l1_import_energy_active"
    # "l2_import_energy_active"
    # "l3_import_energy_active"
    # "export_energy_active"
    # "l1_export_energy_active"
    # "l2_export_energy_active"
    # "l3_export_energy_active"
    # "energy_reactive"
    # "l1_energy_reactive"
    # "l2_energy_reactive"
    # "l3_energy_reactive"
    # "energy_apparent"
    # "l1_energy_apparent"
    # "l2_energy_apparent"
    # "l3_energy_apparent"
    # "power_factor"
    # "l1_power_factor"
    # "l2_power_factor"
    # "l3_power_factor"
    # "power_reactive"
    # "l1_power_reactive"
    # "l2_power_reactive"
    # "l3_power_reactive"
    # "power_apparent"
    # "l1_power_apparent"
    # "l2_power_apparent"
    # "l3_power_apparent"
    # "l1_current"
    # "l2_current"
    # "l3_current"
    # "demand_power_active"
    # "minimum_demand_power_active"
    # "maximum_demand_power_active"
    # "demand_power_apparent"
    # "l1_demand_power_active"
    # "l2_demand_power_active"
    # "l3_demand_power_active"
