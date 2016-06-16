import pymorse
import socket
import threading
import time
import sys

class threadDelay (threading.Thread):

	def __init__(self, delay, robots, robot):
		threading.Thread.__init__(self)
		self.delay = delay
		self.robots = robots
		self.robot = robot

	def run(self):
		print("I'll be waiting: " + self.robot)
		time.sleep(self.delay)
		self.robots[self.robot]['flag'] = True


class threadMessage (threading.Thread):

	def __init__(self, robots, robot):
		threading.Thread.__init__(self)
		self.robots = robots
		self.robot = robot
		self.mustRun = True

	def run(self):
		while (self.mustRun):
			data = self.robots[self.robot]['socket'].recv(1024)
			stringa = data.decode('utf-8').split('/')
			print('######')
			print(stringa)
			print(self.robot)
			print('######')
			#import pdb; pdb.set_trace()
			if len(stringa)!=3 or stringa[1] not in self.robots.keys():
				continue
			receiver = robots[stringa[1]]
			receiver['mutex'].acquire() # mutex of receiver
			try:
				robots[self.robot]['flag'] = False
				t = threadDelay(1, robots, self.robot)
				t.start()
				receiver['socket'].sendall(stringa[2].encode('utf-8'))
			finally:
				receiver['mutex'].release() # mutex of receiver


class threadSocket (threading.Thread):

	def __init__(self, robots, robot, socket):
		threading.Thread.__init__(self)
		self.robots = robots
		self.robot = robot
		self.socket = socket

	def run(self):
		conn, addr = self.socket.accept()
		robots[self.robot]['socket'] = conn


HOST = ''
PORT = 4001
with pymorse.Morse() as simu:
	robots = {}
	for x in simu.robots:
		robots[x] = {}
		robots[x]['timestamp'] = 0
try:
	i = 0
	while i < len(robots.keys):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((HOST, PORT))
		s.listen(1)
		conn, addr = socket.accept()
		data = conn.recv(1024)
		robot = data.decode('utf-8')
		if robot in robots.keys():
			robots[robot]['socket'] = conn
			i = i + 1
except:
	raise

try:
	while True:
		time.delay(1)
except (KeyboardInterrupt, SystemExit):
	for x in robots.keys():
		robots[x]['socket'].close()

	sys.exit(0)
