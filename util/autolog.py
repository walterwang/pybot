import time
from util.core import keyboard
from util.core.mouse import Mouse
from util.core.ocr import Ocr

class Autolog(object):
    def __init__(self, sct, osclientbox):
        self.ocr = Ocr(sct, osclientbox)
        self.mouse = Mouse(sct, osclientbox)
        self.osclientbox= osclientbox
        self.sct = sct
    def login(self):

        with open('account_id.txt','r') as f:
            name = f.readline()
            password = f.readline()

        if "Existing" in self.ocr._get_textbox(top=276, left=410, w=57, h=20):
            time.sleep(1)
            self.mouse.mclick_onclient(410, 276)
            time.sleep(1)
        if "Existing" in self.ocr._get_textbox(top=276, left=410, w=57, h=20):  # if first click doenst register happens in dual screen.
            self.mouse.mclick_onclient(410, 276)
            time.sleep(1)
        if "Continue" in self.ocr._get_textbox(top=310, left=265, w=62, h=18):
            self.mouse.mclick_onclient(265, 312)
            time.sleep(1)
        if "Login" in self.ocr._get_textbox(top=310, left=265, w=62, h=20):
            keyboard.send_string(name.strip())
            keyboard.send_key("TAB_KEY")
            keyboard.send_string(password.strip())
            keyboard.send_key("ENTER_KEY")

    def checkloginscreen(self, logbackin = True):

        if "Existing" in self.ocr._get_textbox(top=276, left=410, w=57, h=20):
            print("logged_out, attempting to log back in")
            if logbackin:
                self.login()
                return True

