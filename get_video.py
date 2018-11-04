#! /usr/bin/env python

import sys
import traceback
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import os
import time

import matplotlib.pyplot as plt
import threading

from drone_connection import DroneConnection


class GetVideo(object):
	def __init__(self, drone_conn):
		self.collecting = False
		self.current_frame = np.array([[[0,0,0]]])
		self.drone_conn = drone_conn
		self.drone = self.drone_conn.get_drone_connection()
		self.file_start_id = 0
		file_patt = self.get_file_pattern()
		while os.path.exists(file_patt.format(start_id=self.file_start_id, id=0)):
			self.file_start_id = self.file_start_id + 1
		self.file_start_id = start_id

	def frame_collect(self):
		try:
			self.collecting = True
			container = av.open(self.drone.get_video_stream())
			# # skip first 300 frames
			# frame_skip = 300
			while self.collecting:
				for frame in container.decode(video=0):
					# if 0 < frame_skip:
					#     frame_skip = frame_skip - 1
					#     continue
					# start_time = time.time()
					image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
					# cv2.imshow('Original', image)
					# cv2.imshow('Canny', cv2.Canny(image, 100, 200))
					# cv2.waitKey(1)
					self.current_frame = image
					# frame_skip = int((time.time() - start_time)/frame.time_base)

		except Exception as ex:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			traceback.print_exception(exc_type, exc_value, exc_traceback)
			print(ex)
		finally:
			self.drone.quit()
			# cv2.destroyAllWindows()
			self.collecting = False
	
	def frame_collect_async(self):
		threading.Thread(target=self.frame_collect).start()
	
	def stop_collecting(self):
		self.collecting = False

	def display(self):
		# plt.imshow(self.current_frame)
		# plt.show()
		pass
	
	def display_cont(self):
		while self.collecting:
			self.display()
	
	def display_cont_async(self):
		threading.Thread(target=self.display_cont).start()
	
	def get_file_pattern(self):
		return 'snaps/snap_{start_id}_{id}.png'
	
	def frame_save(self):
		start_id = self.file_start_id
		file_patt = self.get_file_pattern()
		ident = 0
		latest_fname = file_patt.format(start_id=start_id, id='current')
		while self.collecting:
			fname = file_patt.format(start_id=start_id, id=ident)
			self.display()
			cv2.imwrite(fname,self.current_frame)
			cv2.imwrite(latest_fname,self.current_frame)
			time.sleep(0.25)
			print("Image saved!")
			ident = ident + 1
	
	def frame_save_async(self):
		threading.Thread(target=self.frame_save).start()

if __name__ == '__main__':
	dc = DroneConnection()
	gv = GetVideo(dc)
	gv.frame_collect_async()
	gv.frame_save()
	# gv.display_cont()
