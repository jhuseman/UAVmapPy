#! /usr/bin/env python

import cv2.cv2 as cv2  # for avoidance of pylint error
import time
from imutils import paths
import numpy as np
import imutils
from scipy import misc
import os

import matplotlib.pyplot as plt

import threading

class ObjectDetector(object):
	def __init__(self, gv=None, file_pattern=None):
		self.gv = gv
		self.file_pattern = file_pattern

	def object_detect(self, image, alg="closing_color"):
		def big_contour(image):
			# convert the image to grayscale, blur it, and detect edges
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (5, 5), 0)
			edged = cv2.Canny(gray, 35, 125)

			# find the contours in the edged image and keep the largest one;
			# we'll assume that this is our piece of paper in the image
			cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			cnts = cnts[0] if imutils.is_cv2() else cnts[1]
			if len(cnts) == 0:
				return [0,0,0,0]
			c = max(cnts, key = cv2.contourArea)


			ret = cv2.boundingRect(c)
			box_overlay = cv2.rectangle(image,(ret[0],ret[1]),(ret[0]+ret[2],ret[1]+ret[3]),(0,255,0),2)
			# plt.imshow(edged)
			# plt.show()
			# plt.imshow(box_overlay)
			# plt.show()
			return ret

			# # compute the bounding box of the of the paper region and return it
			# return cv2.minAreaRect(c)
		def color_detect(image):
			# define the list of boundaries
			boundaries = [
				([17, 15, 100], [50, 56, 200]),
				([86, 31, 4], [220, 88, 50]),
				([25, 146, 190], [62, 174, 250]),
				([103, 86, 65], [145, 133, 128]),
				([125, 25, 0], [255, 250, 100]),
			]
			# loop over the boundaries
			(lower, upper) = boundaries[4]
			# create NumPy arrays from the boundaries
			lower = np.array(lower, dtype = "uint8")
			upper = np.array(upper, dtype = "uint8")
		
			# find the colors within the specified boundaries and apply
			# the mask
			mask = cv2.inRange(image, lower, upper)
			output = cv2.bitwise_and(image, image, mask = mask)
		
			# # show the images
			# cv2.imshow("images", np.hstack([image, output]))
			# cv2.waitKey(0)


			# output = (np.array(output) / 64) * 64
			# plt.imshow(output)
			# plt.show()

			# print(output)


			return big_contour(output)
		def closing_color(image):
			return color_detect(cv2.morphologyEx(image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(200,200))))
		return {
			"big_contour":big_contour,
			"color_detect":color_detect,
			"closing_color":closing_color,
			}[alg](image)
	
	def crop(self, image, rect):
		# return image[int(rect[1][1]):int(rect[0][1]), int(rect[1][0]):int(rect[0][0])]
		# return image[int(rect[1][0]):int(rect[0][0]), int(rect[1][1]):int(rect[0][1])]
		if len(rect) < 4:
			rect = [rect[0][0],rect[0][1],rect[1][0],rect[1][1]]
		rect = np.array(rect).flatten()
		print(rect)
		top_left = [rect[0],rect[1]]
		top_left = [int(top_left[0]), int(top_left[1])]
		w_h = [rect[2],rect[3]]
		w_h = [int(w_h[0]), int(w_h[1])]
		bottom_right = [top_left[0]+w_h[0],top_left[1]+w_h[1]]
		# return image[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]
		return image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
	
	def detect_continuously(self, callback=None, time_step=0.25):
		cur_id = 0
		continuing = True
		while continuing:
			if self.file_pattern is None:
				image = self.gv.current_frame
			else:
				fname = self.file_pattern.format(id=cur_id)
				if os.path.exists(fname):
					image = misc.imread(fname)
				else:
					continuing = False
			rect = self.object_detect(image)
			cropped = self.crop(image,rect)
			if not callback is None:
				callback(cropped, rect)
			time.sleep(time_step)
			cur_id = cur_id + 1
	
	def save_image(self, image, filename):
		misc.imsave(filename, image)
	
	def detect_and_save(self, out_file_pattern, time_step=0.25, additional_cb = None):
		self.detect_and_save____cur_id_val = 0
		def cb(cropped, rect):
			if len(cropped) > 0:
				if len(cropped[0]) > 0:
					fname = out_file_pattern.format(id=self.detect_and_save____cur_id_val)
					self.save_image(cropped, fname)
					if not additional_cb is None:
						additional_cb({
							'filename':fname,
							'rect':rect,
							'cropped':cropped,
						})
			self.detect_and_save____cur_id_val = self.detect_and_save____cur_id_val + 1
		self.detect_continuously(callback=cb, time_step=time_step)
	
	def detect_and_save_async(self, *args, **kwargs):
		def temp_func():
			self.detect_and_save(*args, **kwargs)
		threading.Thread(target=temp_func).start()

if __name__ == '__main__':
	for i in range(0,35):
		if not i in range(0,3)+[4]:
			od = ObjectDetector(file_pattern='snaps/snap_'+str(i)+'_{id}.png')
			od.detect_and_save('snaps/crop_'+str(i)+'_{id}.png', time_step=0)
