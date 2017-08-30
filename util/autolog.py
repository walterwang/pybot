import time

from util.core import mouse, keyboard
import util.core.ocr as ocr

def login(box):
    with open('account_id.txt','r') as f:
        name = f.readline()
        password = f.readline()

    if "Existing" in ocr._get_textbox(bbox=box, top=276, left=410, w=57, h=20):
        time.sleep(1)
        mouse.mclick_onclient(box, 410, 276)
        time.sleep(1)
    if "Existing" in ocr._get_textbox(bbox=box, top=276, left=410, w=57, h=20):  # if first click doenst register happens in dual screen.
        mouse.mclick_onclient(box, 410, 276)
        time.sleep(1)
    if "Continue" in ocr._get_textbox(bbox=box, top=310, left=265, w=62, h=18):
        mouse.mclick_onclient(box, 265, 312)
        time.sleep(1)
    if "Login" in ocr._get_textbox(bbox=box, top=310, left=265, w=62, h=20):
        keyboard.send_string(name.strip())
        keyboard.send_key("TAB_KEY")
        keyboard.send_string(password.strip())
        keyboard.send_key("ENTER_KEY")

def checkloginscreen(box, logbackin = True):

    if "Existing" in ocr._get_textbox(bbox=box, top=276, left=410, w=57, h=20):
        print("logged_out, attempting to log back in")
        if logbackin:
            login(box)
            return True

