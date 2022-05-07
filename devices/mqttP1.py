#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""P1 meter device for solaredge_meterproxy

   This file is indended to be used with https://github.com/nmakel/solaredge_meterproxy by nmakel
   and is to be stored in the devices folder

   It consumes MQTT messages with meterdata from the P1 meter created with https://github.com/marcelrv/p1-reader

"""

from __future__ import division
from collections import deque

import logging
import sys
import time
import json
import paho.mqtt.client as mqtt
from datetime import datetime

__author__ = ["Marcel Verpaalen"]
__version__ = "1.0"
__copyright__ = "Copyright 2022, Marcel Verpaalen"
__license__ = "GPL"
__credits__ = ["NMakel"]

class MovingAverage(object):
    def __init__(self, size):
        """
        Initialize your data structure here.
        :type size: int
        """
        self.queue = deque(maxlen=size)

    def next(self, val):
        """
        :type val: int
        :rtype: float
        """
        self.queue.append(val)
        return sum(self.queue) / len(self.queue)


lastValues = {}
logger = logging.getLogger()

# 1 measurement/message every 5 sec -> 15min demand average
demandAvg = MovingAverage(180)
demandL1Avg = MovingAverage(180)
demandL2Avg = MovingAverage(180)
demandL3Avg = MovingAverage(180)

def on_connect(client, userdata, flags, rc):
    logger.info(
        f"MQTT connected to {userdata['host']}:{userdata['port']} - topic: '{userdata['meterValuesTopic']}' with result code {rc}.")
    client.subscribe(userdata["meterValuesTopic"])
    if userdata['willTopic'] is not None:
        client.publish(userdata['willTopic'], "MeterProxy Connected " +
                       str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))


def on_message(client, userdata, message):
    global lastValues
#   logger.debug("Dump variable %s " %  json.dumps( userdata, indent=4, sort_keys=True))
    decoded_message = str(message.payload.decode("utf-8"))
    lastValues = json.loads(decoded_message)
    # Calc net power average
    lastValues ['demand_power_active'] = demandAvg.next ( lastValues['powerImportedActual'] - lastValues['powerExportedActual'] )
    lastValues ['l1_demand_power_active'] = demandL1Avg.next( lastValues['instantaneousActivePowerL1Plus'] - lastValues['instantaneousActivePowerL1Min'] )
    lastValues ['l2_demand_power_active'] = demandL2Avg.next( lastValues['instantaneousActivePowerL2Plus'] - lastValues['instantaneousActivePowerL2Min'] )
    lastValues ['l3_demand_power_active'] = demandL3Avg.next( lastValues['instantaneousActivePowerL3Plus'] - lastValues['instantaneousActivePowerL3Min'] )
    logger.debug(F'Received message in {message.topic}, avg demand: {lastValues ["demand_power_active"]}')

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
    global lastValues
    submitValues = {}

    submitValues['l1n_voltage'] = lastValues['instantaneousVoltageL1']
    submitValues['l2n_voltage'] = lastValues['instantaneousVoltageL2']
    submitValues['l3n_voltage'] = lastValues['instantaneousVoltageL3']
    submitValues['voltage_ln']  = lastValues['instantaneousVoltageL1']
    submitValues['frequency'] = 50

    submitValues ['power_active'] = lastValues['powerImportedActual'] - lastValues['powerExportedActual']
    submitValues ['l1_power_active']= lastValues['instantaneousActivePowerL1Plus'] - lastValues['instantaneousActivePowerL1Min']
    submitValues ['l2_power_active']= lastValues['instantaneousActivePowerL2Plus'] - lastValues['instantaneousActivePowerL2Min']
    submitValues ['l3_power_active']= lastValues['instantaneousActivePowerL3Plus'] - lastValues['instantaneousActivePowerL3Min']

    P1Current=False
    if (P1Current):
        submitValues['l1_current'] = lastValues[ 'instantaneousCurrentL1'] 
        submitValues['l2_current'] = lastValues[ 'instantaneousCurrentL2'] 
        submitValues['l3_current'] = lastValues[ 'instantaneousCurrentL3'] 
    else:
        #calculate current as P1 provided current is rounded to integers
        submitValues['l1_current'] = abs ( submitValues ['l1_power_active'] ) / lastValues['instantaneousVoltageL1']
        submitValues['l2_current'] = abs ( submitValues ['l2_power_active'] ) / lastValues['instantaneousVoltageL2']
        submitValues['l3_current'] = abs ( submitValues ['l3_power_active'] ) / lastValues['instantaneousVoltageL3']

    submitValues ['demand_power_active'] = lastValues ['demand_power_active'] 
    submitValues ['l1_demand_power_active'] = lastValues ['l1_demand_power_active']
    submitValues ['l2_demand_power_active'] = lastValues ['l2_demand_power_active']
    submitValues ['l3_demand_power_active'] = lastValues ['l3_demand_power_active']

    submitEnergy=True
    if (submitEnergy):
        submitValues['import_energy_active'] = lastValues['electricityImported'] / 1000.0
        submitValues ["l1_import_energy_active"] = lastValues['electricityImported'] / 1000.0
        submitValues['export_energy_active'] = lastValues['electricityExported'] / 1000.0
        submitValues ["l1_export_energy_active"] = lastValues["electricityExported"] / 1000.0
        submitValues['energy_active'] =  submitValues['import_energy_active'] - submitValues['export_energy_active'] 
    submitValues["_input"] = lastValues

    logger.debug("Dump values %s " %  json.dumps( submitValues, indent=4, sort_keys=True))

    return submitValues

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
