import uinput
import time


events = {
    "a": uinput.KEY_A,
    "b": uinput.KEY_B,
    "c": uinput.KEY_C,
    "LEFT_KEY": uinput.KEY_LEFT,
    "RIGHT_KEY": uinput.KEY_RIGHT,
}

def send_key(key):
    with uinput.Device(set(events.values())) as device:
        time.sleep(.1)
        device.emit_click(events[key])

def send_string(string):
    with uinput.Device(set(events.values())) as device:
        time.sleep(.1)
        for c in string:
            device.emit_click(events[c])

def hold_key(key, t):
    with uinput.Device(set(events.values())) as device:
        time.sleep(.1)
        for i in range(t):
            time.sleep(.1)
            device.emit(events[key], 100)


