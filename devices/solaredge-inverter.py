import logging

import solaredge_modbus


def device(config):

    # Configuration parameters:
    #
    # timeout   seconds to wait for a response, default: 1
    # retries   number of retries, default: 3
    # unit      modbus address, default: 1
    #
    # For Modbus TCP:
    # host      ip or hostname
    # port      modbus tcp port
    #
    # For Modbus RTU:
    # device    serial device, e.g. /dev/ttyUSB0
    # stopbits  number of stop bits
    # parity    parity setting, N, E or O
    # baud      baud rate

    timeout = config.getint("timeout", fallback=1)
    retries = config.getint("retries", fallback=3)
    unit = config.getint("src_address", fallback=1)

    host = config.get("host", fallback=False)
    port = config.getint("port", fallback=False)
    device = config.get("device", fallback=False)

    if device:
        stopbits = config.getint("stopbits", fallback=1)
        parity = config.get("parity", fallback="N")
        baud = config.getint("baud", fallback=2400)

        if (parity
                and parity.upper() in ["N", "E", "O"]):
            parity = parity.upper()
        else:
            parity = False

        return solaredge_modbus.Inverter(
            device=device,
            stopbits=stopbits,
            parity=parity,
            baud=baud,
            timeout=timeout,
            retries=retries,
            unit=unit
        )
    else:
        return solaredge_modbus.Inverter(
            host=host,
            port=port,
            timeout=timeout,
            retries=retries,
            unit=unit
        )


def values(device):
    if not device:
        return {}

    logger = logging.getLogger()
    logger.debug(f"device: {device}")

    values = {}
    values = device.read_all()
    meters = device.meters()
    batteries = device.batteries()
    values["meters"] = {}
    values["batteries"] = {}

    for meter, params in meters.items():
        meter_values = params.read_all()
        values["meters"][meter] = meter_values

    for battery, params in batteries.items():
        battery_values = params.read_all()
        values["batteries"][battery] = battery_values

    logger.debug(f"values: {values}")

    
    for battery, params in batteries.items():
        battery_values = params.read_all()
        values["batteries"][battery] = battery_values
    
    return values        
    
