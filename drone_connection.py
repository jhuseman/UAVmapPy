#! /usr/bin/env python

import tellopy

class DroneConnection(object):
	def __init__(self):
		self.drone = tellopy.Tello()
		self.drone.connect()
		self.drone.wait_for_connection(60.0)
	
	def get_drone_connection(self):
		return self.drone
	
	def quit(self):
		self.drone.quit()
