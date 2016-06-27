import pymorse
import select
import socket
import sys
import time

HOST = ''
PORT = 4001
with pymorse.Morse() as simu:
	robots = {}
	for x in simu.robots:
		robots[x] = {}
		robots[x]['flag'] = False

try:
	address = {}
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1)
	i = 0
	while i < len(robots.keys()):
		conn, addr = s.accept()
		data = conn.recv(1024)
		robot = data.decode('utf-8')

		if robots[robot]['flag']:
			raise ValueError

		robots[robot]['conn'] = conn
		robots[robot]['flag'] = True
		address[addr] = {}
		address[addr]['robot'] = robot
		address[addr]['timestamp'] = 0
		i = i + 1

except KeyError:
	print('Wrong robot name')
	s.close()
	for x in robots.keys():
		if robots[x]['flag']:
			robots[x]['conn'].close()
	sys.exit(1)
except ValueError:
	print("Robot '{}' already connected".format(robot))
	s.close()
	for x in robots.keys():
		if robots[x]['flag']:
			robots[x]['conn'].close()
	sys.exit(1)

for x in robots.keys():
	conn = robots[x]['conn']
	conn.sendall(b'Start\x04')
print('Start send')

try:
	while True:
		read_list, _, _ = select.select([robots[x]['conn'] for x in robots.keys()], [], [])
		for x in read_list:
			data = x.recv(1024)
			timestamp = time.time()
			message = data.decode('utf-8')
			bracket = message.find('{')
			if bracket <= 0 or bracket == len(message) - 1 or message[-1] != '}':
				continue
			stringa = [message[:bracket], message[bracket:]]
			if stringa[0] not in robots.keys():
				continue
			if timestamp <= address[x.getpeername()]['timestamp']:
				continue
			print(stringa)
			address[x.getpeername()]['timestamp'] = timestamp
			robots[stringa[0]]['conn'].sendall(stringa[1].encode('utf-8'))
except (KeyboardInterrupt, SystemExit):
	for x in robots.keys():
		robots[x]['conn'].close()
	print('Server is shutting down')
	sys.exit(0)
