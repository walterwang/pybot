import os

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
img_dir = "/media/walter/565EBE215EBDF9B7/Users/Walter/Desktop/rs_train2/"

if not os.path.exists(img_dir):
    os.makedirs(img_dir)

files = os.listdir(img_dir)
print(files)
id = 93
# for f in files:
#     if int(f.split('.')[0])>id:
#         id=int(f.split('.')[0])
#         print(id)

for i in range(1000):
    time.sleep(2)
    sct.get_pixels(box)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


    cv2.imshow('client', img)

    id+=1
    file_name=img_dir+str(id)+'.jpg'
    cv2.imwrite(file_name, img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break