import pymorse
import pytoml as toml
import os
import select
import socket
import sys
import time


# control if a file exists
def findFileInPath(filename, extension, paths):
	for path in paths:
		if os.path.exists(os.path.join(path, filename)):
			return os.path.join(path, filename)
		elif os.path.exists(os.path.join(path, filename + '.' + extension)):
			return os.path.join(path, filename + '.' + extension)
	raise FileNotFoundError('File ' + filename + ' not found')


# find the path of a simulation starting from the simulation name
def findSimuPath(simuName):
	with open(os.path.join(MORSECONFIGPATH, 'config'), 'r') as config:
		for line in config:
			if simuName in line:
				lineList = line.split(' = ')
				return lineList[1].strip('\n')
		return None


def strToBool(s):
	if s == 'True':
		return True
	if s == 'False':
		return False
	raise ValueError('Wrong input')


def strToInt(s):
	try:
		i = int(s)
	except ValueError:
		print('Wrong input')
		raise
	return i


def receive(conn):
	data = b''
	word = b''
	while word != b'\x04':
		data += word
		word = conn.recv(1)
	message = data.decode('utf-8')
	return message


def send(stringa, socket):
	message = stringa + '\x04'
	socket.sendall(message.encode('utf-8'))


def messageInSocket(s):
	read_list, _, _ = select.select([s], [], [], 0)
	if read_list == []:
		return False
	else:
		return True


def stopRobot(simu, robot):
	components = simu.__dict__[robot]
	for c in components:
		deact = robot + "." + c
		try:
			simu.deactivate(deact)
		except pymorse.MorseServiceFailed:
			pass


HOST = 'localhost'
PORT = 50001
HOSTSERVER = 'localhost'
PORTSERVER = 4001
MORSECONFIGPATH = os.path.join(os.environ['HOME'], '.morse/')
MORSELABPATH = os.environ.get("MORSELABPATH")
GAMESPATH = os.path.join(MORSELABPATH, "games")

if __name__ == '__main__':

	if len(sys.argv) != 2 and len(sys.argv) != 5:
		raise Exception('Wrong number of parameters')

	SIMUPATH = findSimuPath(sys.argv[1])
	if SIMUPATH == None:
		raise Exception('Simulation name not found')

	with pymorse.Morse() as simu:

		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((HOST, PORT)) # connect to layer.py

			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketServer:
				socketServer.connect((HOSTSERVER, PORTSERVER)) # connect to server.py
				send('SCORE', socketServer)

				start = ''
				while 'Start' not in start:
					start = receive(socketServer)
					print(start)

				startTime = time.time()
				maxScore = 100

				robots = {}
				for x in simu.robots:
					robots[x] = {}
					robots[x]['score'] = maxScore
					robots[x]['collision'] = 0
					robots[x]['stop'] = False

				# Open and load the local file containing the configuration of the simulation
				with open(os.path.join(SIMUPATH, "g.toml"), 'r') as gfile:
					simulation = toml.loads(gfile.read())

					#Check if game file exists and load it
					game_name = simulation['game']['name']
					try:
						game_name = findFileInPath(game_name, 'toml', [SIMUPATH, GAMESPATH])
					except:
						raise

				with open(game_name, 'r') as gamefile:
					game = toml.loads(gamefile.read())

					timeSimu = game['game']['time']['timeSimu']
					scoreZero = game['game']['time']['scoreZero']
					endTime = game['game']['time']['endTime']

					init = game['game'].get('initScore', {})
					k = init.get('k', 0)
					initialScore = init.get('initialScore', 0)
					stopFlag = init.get('stopFlag', False)

				if len(sys.argv) == 5:
					timeSimu = strToInt(sys.argv[2])
					endTime = strToBool(sys.argv[3])
					scoreZero = strToBool(sys.argv[4])

				timeLeft = 1
				try:
					while not ((endTime and timeLeft <= 0) or (scoreZero and max([i['score'] for i in robots.values()]) <= 0)):
						print('\033[H\033[2J')
						diffStartTime = time.time() - startTime
						timeLeft = timeSimu - diffStartTime
						while messageInSocket(s):
							message = receive(s)
							point = message.split('.')
							robot = point[0]
							score = point[1]
							stop = point[2]
							for x in robots.keys():
								if x == robot:
									robots[x]['collision'] += float(score)
									if stop == 'True':
										stopRobot(simu, x)
										robots[x]['stop'] = True
										robots[x]['score'] = initialScore + k*diffStartTime + robots[x]['collision']
						print('{}| {}'.format('Robot'.center(20), 'Score'.center(20)))
						print('----------------------------------------------')
						for x in robots.keys():
							if not robots[x]['stop']:
								robots[x]['score'] = initialScore + k*diffStartTime + robots[x]['collision']
							if stopFlag:
								robots[x]['score'] = max(robots[x]['score'], 0)
							if robots[x]['score'] == 0 and stopFlag:
								stopRobot(simu, x)
							print('{}| {}'.format(x.center(20), str(round(robots[x]['score'], 1)).center(20)))
						print('----------------------------------------------')
						print('{}:{}'.format('Time'.center(5), str(int(diffStartTime)).center(5)))
						time.sleep(0.2)
				except (KeyboardInterrupt, SystemExit):
					print("score.py is shutting down")
