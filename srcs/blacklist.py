import os
import sys
import cv2
import numpy as np

def error(img1, img2):
	h, w, _= img1.shape
	h2, w2, _ = img2.shape
	print(h, w)
	print(h2, w2)
	if h == h2 and w == w2:
		try:
			diff = cv2.subtract(img1, img2)
		except:
			print('Subtract failed')
			try:
				diff = abs(img1-img2)
			except:
				return -1, -1
		err = np.sum(diff**2)
		mse = err/(float(h*w))
		#    msre = np.sqrt(mse)
		return mse, diff
	else:
		return -1, -1

x = sys.argv[1]
dir = "D:\\manga\\Solo_leveling-"
images = os.listdir(dir + x)
blacklist = os.listdir("D:\\manga\\blacklist")
for image in images:
	print(dir + x + "\\" + image)
	f1 = cv2.imread(dir + x + "\\" + image)
	# cv2.imshow('f1', f1)
	# cv2.waitKey(0)
	for black in blacklist:
		print("D:\\manga\\blacklist\\" + black)
		f2 = cv2.imread("D:\\manga\\blacklist\\" + black)
		# cv2.imshow('f2', f2)
		# cv2.waitKey(0)
		match_error, diff = error(f1, f2)
		print('answer:')
		print(match_error)
