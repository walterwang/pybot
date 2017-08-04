import os, sys
from util.core.client import Client
import numpy as np
import cv2
import mss
import argparse

def get_game_screen(sct4, client_box):
    return np.array(sct4.grab(client_box))[:, :, :-1]

from pykeyboard import PyKeyboardEvent

class MonitorSuper(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)
        self.sct4 = mss.mss()
        self.client = Client()
        PyKeyboardEvent.i = last_id
    def tap(self, keycode, character, press):

        if character == 'w':
            if press:
                    PyKeyboardEvent.i +=1
                    print('map_saved', str(PyKeyboardEvent.i))
                    filename=os.path.join(data_path, label + "_%s.png" % format(PyKeyboardEvent.i,'04d'))
                    print(filename)
                    cv2.imwrite(filename, get_game_screen(self.sct4, self.client.box))
        if character == 'q':
            sys.exit()

if __name__ == "__main__":
    label = 'rocks'
    data_path = os.path.join(os.path.dirname(__file__), "training_data/rocks/JPEGImages/")

    parser = argparse.ArgumentParser()
    parser.add_argument('--label', type = str, default = label)
    parser.add_argument('--dir_path', type=str, default = data_path)
    args = parser.parse_args()
    label = args.label
    data_path = args.dir_path
    num = []
    for f in os.listdir(data_path):
        if label == f.split('_')[0]:
            num.append(int(f.split('_')[-1].split('.')[0]))
    if num:
        last_id = max(num)
    else:
        last_id = 0

    mon = MonitorSuper()
    mon.run()
