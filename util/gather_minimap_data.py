import cv2
import mss
import numpy as np
import util.core.client as client

client = client.Client()

offset_top = 78 - 74
offset_left = 636 - 74
minimap_box = {'top': client.box['top'] + offset_top,
               'left': client.box['left'] + offset_left,
               'width': 151,
               'height': 151}

sct4 = mss.mss()
img = np.array(sct4.grab(minimap_box))[:, :, :-1]



mask = cv2.imread('mask.jpg', 0)



# ret, mask = cv2.threshold(mask, 125, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

thresh = 250
ret, mask = cv2.threshold(mask, thresh, 255, cv2.THRESH_BINARY)


img_masked = cv2.bitwise_and(img, img, mask= mask )
white_mask = cv2.bitwise_not(mask, mask)
white_mask = cv2.cvtColor(white_mask, cv2.COLOR_GRAY2BGR)
combined_img = cv2.add(white_mask, img_masked)
cv2.imshow("minimap", combined_img)
cv2.waitKey(0)
cv2.imwrite("test_minimap.jpg", combined_img, [cv2.IMWRITE_JPEG_QUALITY, 100])

