def device(
        host=False, port=False,
        device=False, stopbits=False, parity=False, baud=False,
        timeout=False, retries=False, unit=False
    ):
    return False


def values(device):
    if not device:
        return {}

    return device.read_all()
