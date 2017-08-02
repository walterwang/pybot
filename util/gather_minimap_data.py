import cv2
import mss
import numpy as np
import core.client as client
import os, sys
import argparse


def get_map(sct4, client_box, square = False):

    offset_top = 78 - 74
    offset_left = 636 - 74
    minimap_box = {'top': client_box['top'] + offset_top,
                   'left': client_box['left'] + offset_left,
                   'width': 151,
                   'height': 151}
    img = np.array(sct4.grab(minimap_box))[:, :, :-1]


    mask = cv2.imread('mask.jpg', 0)

    # ret, mask = cv2.threshold(mask, 125, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    thresh = 250
    ret, mask = cv2.threshold(mask, thresh, 255, cv2.THRESH_BINARY)


    img_masked = cv2.bitwise_and(img, img, mask= mask )
    white_mask = cv2.bitwise_not(mask, mask)
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

        '''Monitor Right key.'''
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
#


# cv2.imwrite("map6.jpg", get_map(square =True), [cv2.IMWRITE_JPEG_QUALITY, 100])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Debug')
    parser.add_argument('-l', type=str, help='debug false by default', default="miningguild")
    args = parser.parse_args()
    label = args.l

    data_path = os.path.join(os.path.dirname(__file__), "training_data/minimaps/miningguild")



    mon = MonitorSuper()
    mon.run()