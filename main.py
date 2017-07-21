import ssd_inference
import numpy as np
import cv2
import mss
import Client
import mouse
import threading
import time
import random

osclient = Client.Client()

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
            cv2.putText(img, str(labels[rclasses[ind]])+": "+ str(np.round(rscores[ind], decimals=2)),
                        topleft, cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.rectangle(img, topleft, botright, (0, 255, 0), 1)
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

inv = osclient.inv
def drop(inv_id, inv =inv):

    ix, iy =inv[inv_id]
    mouse.mclick_abs(ix, iy, click='right', e=2)
    time.sleep(0.3)
    mouse.mclick_abs(ix, iy+42)


def run_script():
    box = osclient.box
    # inv = get_client.get_inventory()
    # char_center = get_client.get_center()
    char_center = osclient.center

    rock1 =(0,0)
    rock2 = (0,0)

    while 1:
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

        mouse.mclick_abs(rock1[0]+box['left'], rock1[1]+box['top'])
        time.sleep(1.4)
        drop(1)
        time.sleep(0.1)

        mouse.mclick_abs(rock2[0]+box['left'], rock2[1]+box['top'])
        time.sleep(1.4)
        drop(0)
        #if 1 > random.randint(0,15):
        #    drop(2)

t = threading.Thread(target = run_script)
#m = threading.Thread(target = debug_thread)
#
t.start()
#m.start()

# run_script()