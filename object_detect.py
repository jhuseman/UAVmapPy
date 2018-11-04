#! /usr/bin/env python

import cv2.cv2 as cv2  # for avoidance of pylint error
import time
from imutils import paths
import numpy as np
import imutils
from scipy import misc
import os

import threading

class ObjectDetector(object):
	def __init__(self, gv=None, file_pattern=None):
		self.gv = gv
		self.file_pattern = file_pattern

	def object_detect(self, image, alg="big_contour"):
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
				return ((0,0),(0,0),0)
			c = max(cnts, key = cv2.contourArea)

			# compute the bounding box of the of the paper region and return it
			return cv2.minAreaRect(c)
		return {
			"big_contour":big_contour,
			}[alg](image)
	
	def crop(self, image, rect):
		return image[int(rect[1][0]):int(rect[0][0]), int(rect[1][1]):int(rect[0][1])]
	
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
		cv2.imwrite(filename, image)
	
	def detect_and_save(self, out_file_pattern, time_step=0.25, additional_cb = None):
		self.detect_and_save____cur_id_val = 0
		def cb(cropped, rect):
			if len(cropped) > 0:
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

if __name__ == '__main__':
	od = ObjectDetector(file_pattern='snaps/snap_31_{id}.png')
	od.detect_and_save('snaps/crop_31_{id}.png', time_step=0)
