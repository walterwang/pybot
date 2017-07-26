import uinput
import time
import mouse
import ocr

def login(box):
    with open('account_id.txt','r') as f:
        name = f.readline()
        password = f.readline()

    letter_index = 'abcdefghijklmnopqrstuvwxyz0123456789'
    events = (
        uinput.KEY_A,
        uinput.KEY_B,
        uinput.KEY_C,
        uinput.KEY_D,
        uinput.KEY_E,
        uinput.KEY_F,
        uinput.KEY_G,
        uinput.KEY_H,
        uinput.KEY_I,
        uinput.KEY_J,
        uinput.KEY_K,
        uinput.KEY_L,
        uinput.KEY_M,
        uinput.KEY_N,
        uinput.KEY_O,
        uinput.KEY_P,
        uinput.KEY_Q,
        uinput.KEY_R,
        uinput.KEY_S,
        uinput.KEY_T,
        uinput.KEY_U,
        uinput.KEY_V,
        uinput.KEY_W,
        uinput.KEY_X,
        uinput.KEY_Y,
        uinput.KEY_Z,
        uinput.KEY_0,
        uinput.KEY_1,
        uinput.KEY_2,
        uinput.KEY_3,
        uinput.KEY_4,
        uinput.KEY_5,
        uinput.KEY_6,
        uinput.KEY_7,
        uinput.KEY_8,
        uinput.KEY_9,
        uinput.KEY_ENTER,
        uinput.KEY_TAB
    )

    with uinput.Device(events) as device:
        if "Existing" in ocr.get_textbox(bbox=box, top=276, left=410, w=57, h=20):
            time.sleep(1)
            mouse.mclick_onclient(box, 410, 276)
            time.sleep(1)
        if "Existing" in ocr.get_textbox(bbox=box, top=276, left=410, w=57, h=20):  # if first click doenst register happens in dual screen.
            mouse.mclick_onclient(box, 410, 276)
            time.sleep(1)
        if "Continue" in ocr.get_textbox(bbox=box, top=310, left=265, w=62, h=18):
            mouse.mclick_onclient(box, 265, 312)
            time.sleep(1)
        if "Login" in ocr.get_textbox(bbox=box, top=310, left=265, w=62, h=20):
            for c in name.strip():
                n = letter_index.find(c)
                device.emit_click(events[n])
            device.emit_click(uinput.KEY_TAB)
            for p in password.strip():
                n = letter_index.find(p)
                device.emit_click(events[n])
            device.emit_click(uinput.KEY_ENTER)

def checkloginscreen(box, logbackin = True):

    if "Existing" in ocr.get_textbox(bbox=box, top=276, left=410, w=57, h=20):
        print("logged_out, attempting to log back in")
        if logbackin:
            login(box)
            return True

