import pytoml as toml
import os
import select
import socket


def receive(conn):
	data = b''
	word = b''
	while word != b'\x04':
		data += word
		word = conn.recv(1)
	message = data.decode('utf-8')
	return message


def send(robot, score, socket):
	message = robot + '.' + str(score) + '\x04'
	socket.sendall(message.encode('utf-8'))


def messageInSocket(s):
	read_list, _, _ = select.select([s], [], [], 0)
	if read_list == []:
		return False
	else:
		return True


HOST = 'localhost'
PORT = 50000
PORTSCORE = 50001
PWD = os.path.join(os.environ['HOME'], 'simulator/test_toml')
#MORSELABPATH = os.environ.get("MORSELABPATH")
#TOMLPATH = os.path.join(MORSELABPATH, "test_toml")

if __name__ == '__main__':
	# connect to collision.py
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))

		# read layer configuration file
		with open(os.path.join(PWD, "l.toml"), 'r') as lfile:
			layer = toml.loads(lfile.read())
			layer = layer.get('layer', {})

			# open a socket to talk with score.py
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketScore:
				socketScore.bind((HOST, PORTSCORE))
				socketScore.listen(1)
				conn, addr = socketScore.accept()

				try:
					while True:
						while not messageInSocket(s):
							pass
						message = receive(s)
						point = message.find('.')
						robot = message[:point]
						obj = message[point + 1:]
						for o in layer['score']:
							if obj in o['obj']:
								print(robot)
								print(obj)
								send(robot, str(['score']), conn)
				except (KeyboardInterrupt, SystemExit):
					s.close()
