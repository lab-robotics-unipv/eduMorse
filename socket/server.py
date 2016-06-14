import socket
import threading
import time
import pymorse


class threadMorse (threading.Thread):

	def __init__(self, delay, robots, element):
		threading.Thread.__init__(self)
		self.delay = delay
		self.robots = robots
		self.element = element
		self.start()

	def run(self):
		#print('Starting thread')
		print("I'll be waiting")
		robots[self.element] = True
		time.sleep(self.delay)
		#print('Thread finished')


with pymorse.Morse() as simu:
	robots = {x: True for x in simu.robots}
HOST = ''
PORT = 50007
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen(5)
	conn, addr = s.accept()
	print('Got connection from', addr)
	while (True):
		data = conn.recv(1024)
		if not data:
			continue
		#print(data.decode('utf-8'))
		stringa = data.decode('utf-8').split('/')
		#print(stringa)
		if stringa[0] != stringa[1]:
			try:
				robots[stringa[0]] = False
				thread = threadMorse(1, robots, stringa[0])
				#eval('simu.' + stringa[2])
			except:
				raise
		else:
			print('Same robot used')
	s.close()
