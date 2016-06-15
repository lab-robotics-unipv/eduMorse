import socket
import threading
import time
import pymorse


class threadDelay (threading.Thread):

	def __init__(self, delay, robots, robot):
		threading.Thread.__init__(self)
		self.delay = delay
		self.robots = robots
		self.robot = robot

	def run(self):
		print("I'll be waiting")
		self.robots[self.robot] = True
		time.sleep(self.delay)


class threadMessage (threading.Thread):

	def __init__(self, robots, robot):
		threading.Thread.__init__(self)
		self.robots = robots
		self.robot = robot

	def run(self):
		while (True):
			data = self.robots[self.robot]['socket'].recv(1024)
			stringa = data.decode('utf-8').split('/')
			receiver = robots[stringa[1]]
			receiver['mutex'].acquire() # mutex of receiver
			try:
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
thread_list = []
with pymorse.Morse() as simu:
	robots = {}
	for x in simu.robots:
		robots[x] = {}
		robots[x]['flag'] = True
		robots[x]['mutex'] = threading.Lock()
try:
	for x in robots.keys():
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((HOST, PORT))
		s.listen(1)
		t = threadSocket(robots, x, s)
		thread_list.append(t)
		t.start()
		PORT = PORT + 1
	for t in thread_list:
		t.join()
except:
	raise

thread_list2 = []
for x in robots.keys():
	t = threadMessage(robots, x)
	t.append(thread_list2)
	t.start()

for t in thread_list2:
	t.join()

PORT = 50007
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen(1)
	conn, addr = s.accept()
	print('Got connection from', addr)
	while (True):
		data = conn.recv(1024)
		if not data:
			continue
		stringa = data.decode('utf-8').split('/')
		if stringa[0] != stringa[1]:
			try:
				robots[stringa[1]]['socket'].sendall(stringa[2].encode('utf-8'))
				robots[stringa[0]] = False
				t = threadDelay(1, robots, stringa[0])
				t.start()
			except:
				raise
		else:
			print('Same robot used')
	s.close()
