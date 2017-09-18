import cv2
import numpy as np
from PIL import Image
import pytesseract

class Ocr(object):

    def __init__(self, sct3, osclientbox):
        self.osclientbox = osclientbox
        self.sct3 = sct3

    def _get_textbox(self, top, left, w, h, textcolor = 'auto'):
        text_bbox = {}
        text_bbox['top'] = self.osclientbox['top'] + top
        text_bbox['left'] = self.osclientbox['left'] + left
        text_bbox['width'] = w
        text_bbox['height'] = h

        img_text = np.array(self.sct3.grab(text_bbox))[:, :, :-1]
        img_text = cv2.cvtColor(img_text, cv2.COLOR_BGR2GRAY)
        if textcolor == 'auto':
            img_text = cv2.threshold(img_text, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            img_text = cv2.medianBlur(img_text, 1)
            img_text = cv2.resize(img_text, (0, 0), fx=4, fy=4)
        else:
            img_text = cv2.threshold(img_text, textcolor, 255, cv2.THRESH_BINARY)[1]
            img_text = cv2.resize(img_text, (0,0), fx= 4, fy =4)
            img_text = cv2.threshold(img_text, 100, 255, cv2.THRESH_BINARY)[1]
        # img_text = cv2.copyMakeBorder(img_text, 10, 10, 10, 10, cv2.BORDER_CONSTANT,value=[0,0,0])
        pil_im = Image.fromarray(img_text)

        # cv2.imshow('img', img_text)
        # cv2.waitKey(1)

        text = pytesseract.image_to_string(pil_im)
        return(text)

    def get_lastchat(self):
        top = 439
        left = 1
        w = 200
        h = 15
        return self._get_textbox(top, left, w, h)

    def get_toptext(self, textcolor = 'auto'):
        top = 0
        left = 0
        w = 226
        h = 19
        return self._get_textbox(top, left, w, h, textcolor)

    def get_dialogue(self):
        top = 386
        left = 76
        w = 200
        h = 24
        return self._get_textbox(top, left, w, h)

    def get_run_energy(self, textcolor= 100):
        top = 129
        left = 540
        w = 23
        h = 15
        run_energy = self._get_textbox(top, left, w, h, textcolor=textcolor)
        try:
            run_energy = int(run_energy)
            return run_energy
        except ValueError:
            return 0

if __name__ == '__main__':
    from util.core.client import Client
    import mss
    import time

    sct = mss.mss()
    osclient = Client()
    testocr = Ocr(sct, osclient.box)
    while 1:
        print(testocr.get_toptext(textcolor=200))
        time.sleep(1)