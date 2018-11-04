#! /usr/bin/env python

import tellopy

class DroneConnection(object):
	def __init__(self):
		self.drone = tellopy.Tello()
		self.drone.connect()
		self.drone.wait_for_connection(60.0)
		
		self.drone.subscribe(self.drone.EVENT_DISCONNECTED, self.disconnect_handler)
	
	def disconnect_handler(self):
		self.drone.connect()

	def get_drone_connection(self):
		return self.drone
	
	def quit(self):
		self.drone.quit()
