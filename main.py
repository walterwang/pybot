import argparse
import random
import threading
import time

import cv2
import mss
import numpy as np

from util import autolog, drop
from util.core import client, keyboard, mouse
from util.core.ssd import ssd_inference

parser = argparse.ArgumentParser(description = 'Debug')
parser.add_argument('--d', type = bool, help='debug false by default', default=False)
args = parser.parse_args()
start_debug = args.d

osclient = client.Client()

box = osclient.box


labels = {
    0: 'none',
    1:'depleted',
    2:'gold',
    3:'tin',
    4:'copper' ,
    5:'clay' ,
    6:'granite' ,
    7:'sandstone' ,
    8:'coal' ,
    9:'iron' ,
    10: 'silver'
}
sct = mss.mss()


def visualize_box(img, rclasses, rscores, rbboxes):
    for ind, box in enumerate(rbboxes):
        topleft = (int(box[1] * img.shape[1]), int(box[0] * img.shape[0]))
        botright = (int(box[3] * img.shape[1]), int(box[2] * img.shape[0]))
        area = (botright[0] - topleft[0]) * (botright[1] - topleft[1])
        if area > 3000:
            img = cv2.putText(img, str(labels[rclasses[ind]])+": "+ str(np.round(rscores[ind], decimals=2)),
                        topleft, cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1, cv2.LINE_AA)
            img = cv2.rectangle(img, topleft, botright, (0, 255, 0), 1)
    return img


def get_client_debug():
    img = np.array(sct.grab(box))[:, :, :-1]
    img = np.array(img)
    rclasses, rscores, rbboxes = ssd_inference.process_image(img)
    client_img = visualize_box(img, rclasses, rscores, rbboxes)
    return client_img

def get_objects():
    img = np.array(sct.grab(osclient.box))[:, :, :-1]
    img = np.array(img)
    rcenter = []
    rclasses, rscores, rbboxes = ssd_inference.process_image(img)
    for ind, box in enumerate(rbboxes):
        topleft = (int(box[1] * img.shape[1]), int(box[0] * img.shape[0]))
        botright = (int(box[3] * img.shape[1]), int(box[2] * img.shape[0]))
        area = (botright[0] - topleft[0]) * (botright[1] - topleft[1])

        if area > 3000:
            c = (int((botright[0] + topleft[0]) / 2), int((botright[1] + topleft[1]) / 2))
            rcenter.append(c)

    return rclasses, rbboxes, rcenter

def debug_thread():
    while 1:
        cv2.imshow('pybot', get_client_debug())

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
def distSquared(p0, p1):
    return (p0[0] - p1[0])**2 + (p0[1] - p1[1])**2


def run_script():
    box = osclient.box
    char_center = osclient.center
    inv = osclient.inv
    rock1 =(0,0)
    rock2 = (0,0)
    loop_count = 0
    while 1:
        if loop_count%100 == 0 and autolog.checkloginscreen(box=box):
            time.sleep(10)
            keyboard.hold_key("LEFT_KEY", 20)
        rclasses, _, rcenter = get_objects()
        r1 = 99999999
        r2 = 99999999
        for c in rcenter:
            d = distSquared(char_center,c)
            if d < r1:
                r2 = r1
                rock2 = rock1
                r1 = d
                rock1 = c
            elif d < r2:
                r2 = d
                rock2 = c
        time.sleep(0.1)
        text_found = mouse.ocr_click(rock1[0] + box['left'], rock1[1] + box['top'], box, target_text="Rock")

        #mouse.mclick_abs(rock1[0]+box['left'], rock1[1]+box['top'])
        time.sleep(1.4)
        drop.drop_item(1, inv)
        time.sleep(0.1)
        text_found = mouse.ocr_click(rock2[0] + box['left'], rock2[1] + box['top'], box, target_text="Rock")

        time.sleep(1.4)
        drop.drop_item(0, inv)
        if random.randint(0,15)<1:
            drop.drop_item(2, inv)
        loop_count+=1

if start_debug:
    t = threading.Thread(target=run_script)
    m = threading.Thread(target=debug_thread)

    t.start()
    m.start()
else:
    run_script()
