import mss
import numpy as np
import cv2
import os
from util.core.mouse import Mouse
import time


class Template(object):

    def __init__(self, sct, osclientbox):
        self.sct = sct
        self.osclientbox = osclientbox
        self.mouse = Mouse(sct, osclientbox)
        filepath = os.path.dirname(__file__)
        self.deposittemplate = cv2.imread(os.path.join(filepath, 'templates/deposittemplate.png'), 3)
        self.pot = cv2.imread(os.path.join(filepath, 'templates/pot.png'), 3)

        self.invbox = {}
        self.invbox['top'] = self.osclientbox['top'] +206
        self.invbox['left'] = self.osclientbox['left'] +550
        self.invbox['width'] = 175
        self.invbox['height'] = 255

    def click_deposit(self):

        mainscreen = np.array(self.sct.grab(self.osclientbox))[:, :, :-1]
        mainscreen = np.array(mainscreen)

        result = cv2.matchTemplate(mainscreen, self.deposittemplate, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        print("values:", maxVal, maxLoc)

        if maxVal > 200433:
            print("location of deposit icon:", maxLoc)
            x,y=maxLoc
            self.mouse.mclick_onclient(x+8, y+8)
            time.sleep(1)
            return maxLoc
        else:
            return None

    def click_pot(self):

        mainscreen = np.array(self.sct.grab(self.invbox))[:, :, :-1]
        mainscreen = np.array(mainscreen)

        result = cv2.matchTemplate(mainscreen, self.pot, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        print("values:", maxVal, maxLoc)

        if maxVal > 500433:
            print("location of pot icon:", maxLoc)
            x,y=maxLoc
            self.mouse.mclick_abs(x+8 + self.invbox['left'], y + 8 + self.invbox['top'])
            time.sleep(1)
            return x + 8 + self.invbox['left'],  y + 8 + self.invbox['top']
        else:
            return 0, 0
if __name__ == '__main__':
    from util.core import client, mouse
    import mss, time

    osclient = client.Client()


    box = osclient.box
    sct = mss.mss()
    t = Template(sct, box)
    time.sleep(5)
    t.click_pot()