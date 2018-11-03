#! /usr/bin/env python

import threading
from time import sleep

from drone_connection import DroneConnection

class Flying(object):
	def __init__(self, drone_conn):
		self.drone_conn = drone_conn
		self.drone = self.drone_conn.get_drone_connection()
		self.drone.subscribe(self.drone.EVENT_FLIGHT_DATA, self.log_handler)

	def log_handler(self, event, sender, data, **args):
		drn = sender
		if event is drn.EVENT_FLIGHT_DATA:
			print(data)
	
	def takeoff(self):
		self.drone.takeoff()
	
	def land(self):
		self.drone.down(50)
		sleep(5)
		self.drone.land()
	
	def turn_right(self,angle):
		self.drone.clockwise(angle)

	def takeoff_land(self):
		self.takeoff()
		sleep(20)
		self.land()
		sleep(5)
		self.drone_conn.quit()
	
	def fly(self):
		self.takeoff()
		sleep(5)
		self.turn_right(10)
		sleep(5)
		self.land()
		sleep(5)
		self.drone_conn.quit()
	
	def fly_async(self):
		threading.Thread(target=self.fly).start()

if __name__ == '__main__':
	dc = DroneConnection()
	fl = Flying(dc)
	fl.fly()
