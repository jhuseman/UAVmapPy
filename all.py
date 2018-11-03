#! /usr/bin/env python

import threading
from time import sleep

from drone_connection import DroneConnection
from flying import Flying
from get_video import GetVideo

if __name__ == '__main__':
	dc = DroneConnection()
	gv = GetVideo(dc)
	fl = Flying(dc)
	gv.frame_collect_async()
	gv.display_cont_async()
	fl.fly()
