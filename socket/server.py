import pymorse
import select
import socket
import sys

HOST = ''
PORT = 4001
with pymorse.Morse() as simu:
	robots = {}
	for x in simu.robots:
		robots[x] = {}
		robots[x]['timestamp'] = 0
		robots[x]['flag'] = False
try:
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
	conn.sendall(b'Start')
print('Start send')

try:
	while True:
		read_list, _, _ = select.select([robots[x]['conn'] for x in robots.keys()], [], [])
		for x in read_list:
			data = x.recv(1024)
			messaggio = data.decode('utf-8')
			receiver = messaggio.find('{')
			if receiver <= 0 or receiver == len(messaggio) - 1 or messaggio[-1] != '}':
				continue
			stringa = [messaggio[:receiver], messaggio[receiver:]]
			if stringa[0] not in robots.keys():
				continue
			print(stringa)
			robots[stringa[0]]['conn'].sendall(stringa[1].encode('utf-8'))
except (KeyboardInterrupt, SystemExit):
	for x in robots.keys():
		robots[x]['conn'].close()
	print('Server is shutting down')
	sys.exit(0)
