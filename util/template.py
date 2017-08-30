import mss
import numpy as np
import cv2
import os
import util.core.mouse as mouse
import time

filepath = os.path.dirname(__file__)
deposittemplate = cv2.imread(os.path.join(filepath,'deposittemplate.png'),3)
def click_deposit(sct, osclientbox):

    mainscreen = np.array(sct.grab(osclientbox))[:, :, :-1]
    mainscreen = np.array(mainscreen)

    result = cv2.matchTemplate(mainscreen, deposittemplate, cv2.TM_CCOEFF)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    print("values:", maxVal, maxLoc)

    if maxVal >2000433:
        print("location of deposit icon:", maxLoc)
        x,y=maxLoc
        mouse.mclick_onclient(osclientbox, x+8, y+8)
        time.sleep(1)
        return maxLoc
    else:
        return None