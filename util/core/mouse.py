import time
import uinput
from Xlib import display

from util.core.ocr import Ocr

class Mouse():
    def __init__(self, sct, osclientbox):

        self.ocr = Ocr(sct, osclientbox)
        self.disp = display.Display().screen()

        self.device = uinput.Device([
                uinput.BTN_LEFT,
                uinput.BTN_RIGHT,
                uinput.REL_X,
                uinput.REL_Y
                ])
        self.osclientbox = osclientbox

    def move_mouse_abs(self, abs_x, abs_y):
        qp = self.disp.root.query_pointer()
        self.device.emit(uinput.REL_X, abs_x-qp.root_x)
        self.device.emit(uinput.REL_Y, abs_y-qp.root_y)


    def ocr_click(self, abs_x, abs_y, click = "left", target_text=[], textcolor = 'auto'):
        text_found = False
        self.move_mouse_abs(abs_x, abs_y)
        time.sleep(.1)
        text = self.ocr.get_toptext(textcolor = textcolor)
        print('text found from ocr click', text)
        for target in target_text:
            if target in text:
                text_found = True
                if click == "left":
                    self.device.emit_click(uinput.BTN_LEFT, 1)
                else:
                    self.device.emit_click(uinput.BTN_RIGHT, 1)
                return text_found

    def mclick_abs(self, abs_x, abs_y, click = "left"):

        qp = self.disp.root.query_pointer()
        self.device.emit(uinput.REL_X, abs_x-qp.root_x)
        self.device.emit(uinput.REL_Y, abs_y-qp.root_y)
        time.sleep(.1)
        if click == "left":
            self.device.emit_click(uinput.BTN_LEFT, 1)
        else:
            self.device.emit_click(uinput.BTN_RIGHT, 1)

    def mclick_onclient(self, abs_x, abs_y, click = "left"):
        abs_x += self.osclientbox['left']
        abs_y += self.osclientbox['top']
        qp = self.disp.root.query_pointer()
        self.device.emit(uinput.REL_X, abs_x-qp.root_x)
        self.device.emit(uinput.REL_Y, abs_y-qp.root_y)
        time.sleep(.1)
        if click == "left":
            self.device.emit_click(uinput.BTN_LEFT, 1)
        else:
            self.device.emit_click(uinput.BTN_RIGHT, 1)

    def set_north(self):
        self.mclick_onclient(560, 20)

    def move_minimap(self, mx , my):
        minimap_center_x = 75 + 562 # change this to osclient map offset to be compatible to other clients
        minimap_center_y = 75 + 4
        self.mclick_onclient(minimap_center_x+mx, minimap_center_y+my)






