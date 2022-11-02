import logging
import json
import sys
import zmq


class ZmqDevice:

    def __init__(self, host, port, topic):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.topic = topic
        print("Collecting updates from meter...")
        self.socket.connect(f"tcp://{host}:{port}")
    
    def read_all(self):
        topicfilter = str(self.topic)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
        recv_string = self.socket.recv()
        topic, message_data = recv_string.split()
        parsed_message_data = json.loads(message_data)
        return parsed_message_data


def device(config):

    # Configuration parameters:
    #
    # host      ip or hostname
    # port      modbus tcp port
    # topic     zeromq topic to listen on
    #

    host = config.get("host", fallback=False)
    port = config.getint("port", fallback=False)
    topic = config.get("topic", fallback=1)

    return ZmqDevice(
        host=host,
        port=port,
        topic=topic,
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
        "power_active": values.get("power_active", 0),
        "l1_power_active": values.get("power_active", 0),
        # "l2_power_active"
        # "l3_power_active"
        "voltage_ln": values.get("voltage", 0),
        "l1n_voltage": values.get("voltage", 0),
        # "l2n_voltage"
        # "l3n_voltage"
        # "voltage_ll"
        # "l12_voltage"
        # "l23_voltage"
        # "l31_voltage"
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
        # "energy_apparent"
        # "l1_energy_apparent"
        # "l2_energy_apparent"
        # "l3_energy_apparent"
        "power_factor": values.get("power_factor", 0),
        "l1_power_factor": values.get("power_factor", 0),
        # "l2_power_factor"
        # "l3_power_factor"
        "power_reactive": values.get("power_reactive", 0),
        "l1_power_reactive": values.get("power_reactive", 0),
        # "l2_power_reactive"
        # "l3_power_reactive"
        "power_apparent": values.get("power_apparent", 0),
        "l1_power_apparent": values.get("power_apparent", 0),
        # "l2_power_apparent"
        # "l3_power_apparent"
        "l1_current": values.get("current", 0),
        # "l2_current"
        # "l3_current"
        "demand_power_active": values.get("total_demand_power_active", 0),
        # "minimum_demand_power_active"
        "maximum_demand_power_active": values.get("maximum_total_demand_power_active", 0),
        # "demand_power_apparent"
        "l1_demand_power_active": values.get("total_demand_power_active", 0),
        # "l2_demand_power_active"
        # "l3_demand_power_active"
    }
