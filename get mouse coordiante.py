from Xlib import display
import ssd_inference

import time
print (time.strftime("%Y-%m-%d %H:%M"))

# for i in range(1000):
#     time.sleep(3)
#     data = display.Display().screen().root.query_pointer()._data
#     print(data["root_x"], data["root_y"])


import numpy as np
import cv2
from mss import mss
from PIL import Image
id = 25
box = {'top': 72, 'left': 18, 'width': 510, 'height': 332}

sct = mss()
img_dir = "/media/walter/565EBE215EBDF9B7/Users/Walter/Desktop/rs_train"

def visualize_box(img, rclasses, rscores, rbboxes):
    id = 0
    for box in rbboxes:
        id += 1


        topleft = ( int(box[1]*510), int(box[0]*332))
        botright = (int(box[3]*510), int(box[2]*332))
        img = cv2.rectangle(img, topleft, botright, (0, 255, 0), 2)
    return img

while 1:
#for i in range(1000):
    #time.sleep(2)
    sct.get_pixels(box)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    rclasses, rscores, rbboxes = ssd_inference.process_image(img)


    img = visualize_box(img, rclasses, rscores, rbboxes)

    cv2.imshow('client', img)

    id+=1
    file_name=img_dir+str(id)+'.jpg'
    #cv2.imwrite(file_name, img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break