import argparse
import random
import threading
import time
from yattag import Doc
import cv2
import mss
import numpy as np
import os

from util import autolog, drop
from util.core import client, keyboard, mouse
from util.core.ssd import ssd_inference

parser = argparse.ArgumentParser(description = 'Debug')

parser.add_argument('--r', type = bool, help='record', default=False)
args = parser.parse_args()
record_debug = args.r

osclient = client.Client()
box = osclient.box


labels = {
    0: 'none',
    1:'depleted',
    2:'bankchest',
    3:'depositbox',
    4:'amethyst' ,
    5:'mithril' ,
    6:'adamantite' ,
    8:'coal' ,
    9:'iron' ,
    15: 'spooky_ghost'

}
sct = mss.mss()


def visualize_box(img, rclasses, rscores, rbboxes):
    for ind, box in enumerate(rbboxes):
        topleft = (int(box[1] * img.shape[1]), int(box[0] * img.shape[0]))
        botright = (int(box[3] * img.shape[1]), int(box[2] * img.shape[0]))
        area = (botright[0] - topleft[0]) * (botright[1] - topleft[1])
        if area> 0: #area > 3000:
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

def generate_xml(filename, img_path, annotation_path=os.path.join(os.path.dirname(__file__), "training_data/rocks/Annotations/")):
    img = np.array(sct.grab(osclient.box))[:, :, :-1]
    img = np.array(img)
    rcenter = []
    rclasses, rscores, rbboxes = ssd_inference.process_image(img)


    doc, tag, text = Doc().tagtext()
    with tag('annotation'):
        with tag('folder'):
            text('JPEGImages')
        with tag('filename'):
            text(filename+'.png')
        with tag('path'):
            text(img_path)
        with tag('source'):
            with tag('database'):
                text('Unknown')
        with tag('size'):
            with tag('width'):
                text(img.shape[1])
            with tag('height'):
                text(img.shape[0])
            with tag('depth'):
                text('3')
        with tag('segmented'):
            text('0')
        for ind, box in enumerate(rbboxes):
            with tag('object'):
                with tag('name'):
                    text(labels[rclasses[ind]])
                with tag('pose'):
                    text('Unspecified')
                with tag('truncated'):
                    text('0')
                with tag('difficult'):
                    text('0')
                with tag('bndbox'):
                    with tag('xmin'):
                        text(str(int(box[1] * img.shape[1])))
                    with tag('ymin'):
                        text(str(int(box[0] * img.shape[0])))
                    with tag('xmax'):
                        text(str(int(box[3] * img.shape[1])))
                    with tag('ymax'):
                        text(str(int(box[2] * img.shape[0])))

    xml_path = os.path.join(annotation_path, filename + '.xml')
    with open(xml_path, 'w') as f:
        f.write(doc.getvalue())
    return rclasses, rbboxes, rcenter

def debug_thread():
    if record_debug:
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter('rocks_debug.mp4', fourcc, 15.0, (osclient.box['width'], osclient.box['height']))
    while 1:
        frame = get_client_debug()
        cv2.imshow('pybot', frame)
        if record_debug:
            out.write(frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    debug_thread()

