import cv2
import mss
import numpy as np
import core.client as client
import os, sys
import argparse

parser = argparse.ArgumentParser(description = 'Debug')
parser.add_argument('-l', type=str, help='debug false by default', default="")
args = parser.parse_args()
label = args.l

data_path = os.path.join(os.path.dirname(__file__),"training_data/minimap_data/")

client = client.Client()

offset_top = 78 - 74
offset_left = 636 - 74
minimap_box = {'top': client.box['top'] + offset_top,
               'left': client.box['left'] + offset_left,
               'width': 151,
               'height': 151}
def get_map():
    sct4 = mss.mss()
    img = np.array(sct4.grab(minimap_box))[:, :, :-1]


    mask = cv2.imread('mask.jpg', 0)

    # ret, mask = cv2.threshold(mask, 125, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    thresh = 250
    ret, mask = cv2.threshold(mask, thresh, 255, cv2.THRESH_BINARY)


    img_masked = cv2.bitwise_and(img, img, mask= mask )
    white_mask = cv2.bitwise_not(mask, mask)
    white_mask = cv2.cvtColor(white_mask, cv2.COLOR_GRAY2BGR)
    return cv2.add(white_mask, img_masked)


from pykeyboard import PyKeyboardEvent

class MonitorSuper(PyKeyboardEvent):
    PyKeyboardEvent.i = 0
    def tap(self, keycode, character, press):

        '''Monitor Right key.'''
        if character == 'Right':
            if press:
                if PyKeyboardEvent.i < 75:
                    PyKeyboardEvent.i +=1
                    print('map_saved', str(PyKeyboardEvent.i))
                    cv2.imwrite(os.path.join(data_path, label + "_%s.jpg" % str(PyKeyboardEvent.i)), get_map(),
                                [cv2.IMWRITE_JPEG_QUALITY, 100])
                else:
                    sys.exit()

mon = MonitorSuper()
mon.run()






