from PIL import Image
import os
# from datetime import date
import sys

x = sys.argv[1]
dir = ("D:\\manga\\Solo_leveling-" + x)
l = []
i = 0
image_1 = Image.open(dir + "\\" + os.listdir(dir)[0])
im_1 = image_1.convert('RGB')
for image in os.listdir(dir):
    if i < 1:
        i += 1
        continue
    print(image)
    # print(dir + "\\" + os.listdir(dir)[2])
    image_2 = Image.open(dir + "\\" + image)
    im_2 = image_2.convert('RGB')
    l.append(im_2)
# image_2 = Image.open(dir + "\\" + os.listdir(dir)[0])
# im_2 = image_2.convert('RGB')
# l.append(im_2)
im_1.save('D:\\manga\\SL_Chapter' + x +'.pdf', save_all=True, append_images=l)
# today = date.today()
# today.month