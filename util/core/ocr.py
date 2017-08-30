import cv2
import mss
import numpy as np
from PIL import Image
import pytesseract

# def get_toptext(bbox):
#     toptext={}
#     toptext['top'] = bbox['top']
#     toptext['left'] = bbox['left']
#     toptext['width'] = 226
#     toptext['height'] = 19
#     sct2 = mss.mss()
#     img_text = np.array(sct2.grab(toptext))[:,:,:-1]
#     img_text = cv2.cvtColor(img_text, cv2.COLOR_BGR2GRAY)
#     img_text = cv2.threshold(img_text, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#     #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
#     img_text = cv2.medianBlur(img_text, 1)
#     img_text = cv2.resize(img_text, (0,0), fx= 3, fy =3)
#
#     pil_im = Image.fromarray(img_text)
#
#     text = pytesseract.image_to_string(pil_im)
#     return (text)

def _get_textbox(bbox, top, left, w, h):

    text_bbox = {}
    text_bbox['top'] = bbox['top'] + top
    text_bbox['left'] = bbox['left'] + left
    text_bbox['width'] = w
    text_bbox['height'] = h
    sct3 = mss.mss()
    img_text = np.array(sct3.grab(text_bbox))[:, :, :-1]
    img_text = cv2.cvtColor(img_text, cv2.COLOR_BGR2GRAY)
    img_text = cv2.threshold(img_text, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    img_text = cv2.medianBlur(img_text, 1)
    img_text = cv2.resize(img_text, (0,0), fx= 3, fy =3)

    pil_im = Image.fromarray(img_text)

    text = pytesseract.image_to_string(pil_im)
    return(text)

def get_lastchat(bbox):
    top = 439
    left = 1
    w = 200
    h = 15
    return _get_textbox(bbox, top, left, w, h)

def get_toptext(bbox):
    top = 0
    left = 0
    w = 226
    h = 19
    return _get_textbox(bbox, top, left, w, h)

def get_dialogue(bbox):
    top = 386
    left = 76
    w = 200
    h = 24
    return _get_textbox(bbox, top, left, w, h)