#! /usr/bin/env python

import threading
from time import sleep

from drone_connection import DroneConnection
from flying import Flying
from get_video import GetVideo
from object_detect import ObjectDetector
from uploader import upload_file

if __name__ == '__main__':
	dc = DroneConnection()
	gv = GetVideo(dc)
	fl = Flying(dc)
	od = ObjectDetector(gv=gv)
	gv.frame_collect_async()
	gv.frame_save_async()
	od.detect_and_save_async('snaps/crop_'+str(gv.file_start_id)+'_{id}.png', additional_cb=upload_file)

	# gv.display_cont_async()
	fl.fly()
