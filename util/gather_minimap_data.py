import cv2
import mss
import numpy as np
import util.core.client as client
import os, sys
import argparse

maskpath = os.path.join(os.path.dirname(__file__), 'mask.jpg')
mask = cv2.imread(maskpath, 0)


def get_map(sct4, client_box, square = False):
    thresh = 250
    ret, m = cv2.threshold(mask, thresh, 255, cv2.THRESH_BINARY)  # to be done: load the mask directry into memory
    offset_top = 4
    offset_left = 562
    minimap_box = {'top': client_box['top'] + offset_top,
                   'left': client_box['left'] + offset_left,
                   'width': 151,
                   'height': 151}
    img = np.array(sct4.grab(minimap_box))[:, :, :-1]

    img_masked = cv2.bitwise_and(img, img, mask= m )
    white_mask = cv2.bitwise_not(m, m)
    white_mask = cv2.cvtColor(white_mask, cv2.COLOR_GRAY2BGR)

    uncroppedmap = cv2.add(white_mask, img_masked)
    if square:
        croppedmap = uncroppedmap[33:118,33:118]
        return croppedmap, uncroppedmap
    else:
        return uncroppedmap



from pykeyboard import PyKeyboardEvent

class MonitorSuper(PyKeyboardEvent):
    sct4 = mss.mss()
    client = client.Client()
    PyKeyboardEvent.i = 0

    def tap(self, keycode, character, press):
        if character == 'q':
            if press:
                if PyKeyboardEvent.i < 75:
                    PyKeyboardEvent.i +=1
                    print('map_saved', str(PyKeyboardEvent.i))
                    filename=os.path.join(data_path, label + "%s.png" % str(PyKeyboardEvent.i))
                    print(filename)
                    cv2.imwrite(filename, get_map(self.sct4, self.client.box, square =True)[0])
                else:
                    sys.exit()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Debug')
    parser.add_argument('-l', type=str, help='debug false by default', default="miningguild")
    args = parser.parse_args()
    label = args.l

    data_path = os.path.join(os.path.dirname(__file__), "training_data/minimaps/miningguild")

    mon = MonitorSuper()
    mon.run()