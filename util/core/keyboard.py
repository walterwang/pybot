import uinput
import time

events = {
    "a": uinput.KEY_A,
    "b": uinput.KEY_B,
    "c": uinput.KEY_C,
    "d": uinput.KEY_D,
    "e": uinput.KEY_E,
    "f": uinput.KEY_F,
    "g": uinput.KEY_G,
    "h": uinput.KEY_H,
    "i": uinput.KEY_I,
    "j": uinput.KEY_J,
    "k": uinput.KEY_K,
    "l": uinput.KEY_L,
    "m": uinput.KEY_M,
    "n": uinput.KEY_N,
    "o": uinput.KEY_O,
    "p": uinput.KEY_P,
    "q": uinput.KEY_Q,
    "r": uinput.KEY_R,
    "s": uinput.KEY_S,
    "t": uinput.KEY_T,
    "u": uinput.KEY_U,
    "v": uinput.KEY_V,
    "w": uinput.KEY_W,
    "x": uinput.KEY_X,
    "y": uinput.KEY_Y,
    "z": uinput.KEY_Z,
    "0": uinput.KEY_0,
    "1": uinput.KEY_1,
    "2": uinput.KEY_2,
    "3": uinput.KEY_3,
    "4": uinput.KEY_4,
    "5": uinput.KEY_5,
    "6": uinput.KEY_6,
    "7": uinput.KEY_7,
    "8": uinput.KEY_8,
    "9": uinput.KEY_9,
    "LEFT_KEY": uinput.KEY_LEFT,
    "RIGHT_KEY": uinput.KEY_RIGHT,
    "TAB_KEY": uinput.KEY_TAB,
    "ENTER_KEY": uinput.KEY_ENTER
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


