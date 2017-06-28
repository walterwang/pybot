import numpy as np
import cv2
import os

# Load an color image in grayscale


path = '/home/walter/Desktop/varrock_map.jpg'

output_dir ='/media/walter/565EBE215EBDF9B7/Users/Walter/Documents/map_output_dir/'
file_list = os.listdir(output_dir)
img = cv2.imread(path,1)
height, width, channels = img.shape
for x in range(width-140):
    for y in range(height - 140):

        file_name = str(x+70)+'_'+str(y+70)+'.jpg'
        if file_name not in file_list:
            crop_img = img[x:x + 140, y:y + 140]
            cv2.imwrite(output_dir+file_name, crop_img)
