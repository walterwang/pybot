# Not working

import numpy as np
import cv2
im = cv2.imread('test.jpg')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 10, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnt = contours[0]
# cv2.drawContours(im, contours, -1, (0,255,0), 1)

epsilon = 0.1*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)


cv2.drawContours(im, contours,3, (0,255,0), 3)

cv2.imshow("test", im)
cv2.waitKey(0)
cv2.destroyAllWindows()