import pytoml as toml
import os
import select
import socket
import sys


# find the path of a simulation starting from the simulation name
def findSimuPath(simuName):
	with open(os.path.join(MORSECONFIGPATH, 'config'), 'r') as config:
		for line in config:
			if simuName in line:
				lineList = line.split(' = ')
				return lineList[1].strip('\n')
		return None


def receive(conn):
	data = b''
	word = b''
	while word != b'\x04':
		data += word
		word = conn.recv(1)
	message = data.decode('utf-8')
	return message


def send(robot, score, stop, socket):
	message = robot + '.' + str(score) + '.' + str(stop) + '\x04'
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
MORSECONFIGPATH = os.path.join(os.environ['HOME'], '.morse/')

if __name__ == '__main__':

	if len(sys.argv) != 2:
		raise Exception('Wrong number of parameters')

	SIMUPATH = findSimuPath(sys.argv[1])
	if SIMUPATH == None:
		raise Exception('Simulation name not found')

	# connect to collision.py
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))

		# read layer configuration file
		with open(os.path.join(SIMUPATH, "l.toml"), 'r') as lfile:
			layer = toml.loads(lfile.read())
			layer = layer.get('layer', {})

			# open a socket to talk with score.py
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketScore:
				socketScore.bind((HOST, PORTSCORE))
				socketScore.listen(1)
				conn, addr = socketScore.accept()

				#print("Press ctrl+C to stop")

				try:
					while True:
                        if layer.get('layer', None) == None:
                            time.sleep(1)
                            continue

                        while not messageInSocket(s):
                            pass

						message = receive(s)
                        parts = message.split('.')
						robot = parts[0]
                        obj = parts[1:]

                        score = 0
                        stop = False
						for s in layer['score']:
                            for o in obj:
							    if o in s['obj']:
                                    score += s['score']
                                    stop |= s['stop']
                        send(robot, str(score), str(stop), conn)
				except (KeyboardInterrupt, SystemExit):
					s.close()
					socketScore.close()
					print("layer.py is shutting down")
