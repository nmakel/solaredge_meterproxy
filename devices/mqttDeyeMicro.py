""" Deye Microinverter for solaredge_meterproxy

    This file is intended to be used with https://github.com/nmakel/solaredge_meterproxy
    and is to be stored in the devices folder.

    It consumes MQTT messages which are provided via Deye solar inverter MQTT bridge,
    see https://github.com/kbialek/deye-inverter-mqtt
    Only for microinverter so far. Feel free to extend it.
"""

import logging

import paho.mqtt.client as mqtt

lastValues = {}
logger = logging.getLogger()


def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to MQTT: {userdata['host']}:{userdata['port']}/{userdata['topic']}")
    client.subscribe(userdata["topic"]+"/#")

def on_message(client, userdata, message):
    global lastValues

    logger.debug(f"MQTT message received: {message.topic}:{message.payload.decode('utf-8')}")

    topicmap = userdata['topicmap']
    if message.topic == f"userdata['topic']/status":
        if message.payload.decode("utf-8") == "online":
            logger.debug(f"Status is online")
        else:
            logger.debug(f"Status is not online, setting power vlaues to 0")
            lastValues["power_active"] = 0
            lastValues["l1_power_active"] = 0
            lastValues["l1_current"] = 0
    elif message.topic in topicmap:
        logger.debug(f"message {message.topic} is in map")
        for entry in topicmap[message.topic]:
            lastValues[entry[0]] = float(message.payload) * entry[1]
    else:
        logger.debug(f"MQTT ignored unknown topic {message.topic}")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning(f"MQTT disconnected unexpectedly: {rc}, trying to reconnect")
    reconnect_delay = 10
    while true:
        time.sleep(reconnect_delay)
        try:
            client.reconnect()
            logger.info(f"MQTT reconnected")
            return
        except Exception as err:
            logger.warning("MQTT reconnect failed (%s), retrying...", err)


def device(config):

    # Configuration parameters:
    #
    # host              ip or hostname of MQTT server
    # port              port of MQTT server
    # keepalive         keepalive time in seconds for MQTT server
    # topic             MQTT topic to subscribe to to receive meter values
    #                   the string is extended by '/#' to receive all sub topics

    host = config.get("host", fallback="localhost")
    port = config.getint("port", fallback=1883)
    keepalive = config.getint("keepalive", fallback=60)
    topic = config.get("topic", fallback="deye")

    """ The topicmap is used for mapping the Deye names to the one within the proxy.
        Per MQTT topic an array of proxy keys has to be given. The array entries are arrays again.
        The first value of the array is the name within the proxy, the second vlaue is a scaling
        factor. Set it to -1 to invert something. Currently not really needed, but who knows.
    """
    userdata = {
        "host": host,
        "port": port,
        "topic": topic,
        "topicmap":  {
            f"{topic}/total_energy": [ ["energy_active", 1] ],
            f"{topic}/ac/l1/power": [ ["l1_power_active", 1], ["active_power", 1] ],
            f"{topic}/ac/l1/voltage": [ ["voltage_ln", 1], ["l1n_voltage", 1] ],
            f"{topic}/ac/freq": [ ["frequency", 1] ],
            f"{topic}/total_energy": [ ["l1_energy_active", 1], ["l1_export_energy_active", 1] ],
            f"{topic}/ac/l1/current": [ ["l1_current", 1] ],
        }
    }

    try:
        client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1, userdata=userdata)
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        client.connect(host, port, keepalive)
        client.loop_start()
    except Exception as err:
        logger.error(f"MQTT connection failed: {host}:{port}/{topic} ({err=})")

    return {
        "client": client,
        "host": host,
        "port": port,
        "keepalive": keepalive,
        "topic": topic,
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
