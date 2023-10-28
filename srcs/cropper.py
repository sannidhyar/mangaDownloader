from PIL import Image
import os
from scipy import misc
import sys

# chapter = sys.argv[1]
image = sys.argv[1]
# x = str(chapter)
# image = 'images05.jpg'

import cv2   
# Read the image
img = cv2.imread(image)
try:
    print(img.shape)
except:
    print('\n' + image + '\n')
height = img.shape[0]
width = img.shape[1]

# Cut the image in half
height_cutoff = height // 4
if height_cutoff > 2500:
    print(image)
    s1 = img[:height_cutoff, :]
    s2 = img[height_cutoff:height_cutoff+height_cutoff, :]
    s3 = img[height_cutoff+height_cutoff:height_cutoff+height_cutoff+height_cutoff, :]
    s4 = img[height_cutoff+height_cutoff+height_cutoff:, :]
    cv2.imwrite(image[:-4] + "_1.jpg", s1)
    cv2.imwrite(image[:-4] + "_2.jpg", s2)
    cv2.imwrite(image[:-4] + "_3.jpg", s3)
    cv2.imwrite(image[:-4] + "_4.jpg", s4)
    os.remove(image)