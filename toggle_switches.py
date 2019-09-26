from orvibo.orvibo import Orvibo

def toggleSwitches():
    for args in Orvibo.discover().values():
        device = Orvibo(*args)
        device.on = not device.on

toggleSwitches()
