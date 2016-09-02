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


def messageInSocket(s):
	read_list, _, _ = select.select([s], [], [], 0)
	if read_list == []:
		return False
	else:
		return True


HOST = 'localhost'
PORT = 50001
PWD = os.path.join(os.environ['HOME'], 'simulator/test_toml')
MORSELABPATH = os.environ.get("MORSELABPATH")
GAMESPATH = os.path.join(MORSELABPATH, "games")
TOMLPATH = os.path.join(MORSELABPATH, "test_toml")

if __name__ == '__main__':
	with pymorse.Morse() as simu:

		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((HOST, PORT))

			startTime = time.time()
			maxScore = 100

			robots = {}
			for x in simu.robots:
				robots[x] = {}
				robots[x]['score'] = maxScore
				robots[x]['collision'] = 0

			# Open and load the local file containing the configuration of the simulation
			with open(os.path.join(PWD, "g.toml"), 'r') as gfile:
				simulation = toml.loads(gfile.read())

				#Check if game file exists and load it
				game_name = simulation['game']['name']
				try:
					game_name = findFileInPath(game_name, 'toml', [PWD, GAMESPATH])
				except:
					raise

			with open(game_name) as gamefile:
				game = toml.loads(gamefile.read())

			for timeGame in game['game']['time']:
				timeSimu = timeGame['timeSimu']
				scoreZero = timeGame['scoreZero']
				endTime = timeGame['endTime']

			if len(sys.argv) == 4:
				timeSimu = strToInt(sys.argv[1])
				endTime = strToBool(sys.argv[2])
				scoreZero = strToBool(sys.argv[3])
			if len(sys.argv) != 1 and len(sys.argv) != 4:
				raise Exception('Wrong number of parameters')

			loss = maxScore/timeSimu
			timeLeft = 1
			while not ((endTime and timeLeft <= 0) or (scoreZero and max([i['score'] for i in robots.values()]) <= 0)):
				print('\033[H\033[2J')
				diffStartTime = time.time() - startTime
				timeLeft = timeSimu - diffStartTime
				while messageInSocket(s):
					message = receive(s)
					point = message.find('.')
					robot = message[:point]
					score = message[point + 1:]
					for x in robots.keys():
						if x == robot:
							robots[x]['collision'] += float(score)
				print('{}| {}'.format('Robot'.center(20), 'Score'.center(20)))
				print('----------------------------------------------')
				for x in robots.keys():
					robots[x]['score'] = maxScore - loss*diffStartTime + robots[x]['collision']
					robots[x]['score'] = max(robots[x]['score'], 0)
					if robots[x]['score'] == 0:
						components = simu.__dict__[x]
						for c in components:
							s = x + "." + c
							try:
								simu.deactivate(s)
							except pymorse.MorseServiceFailed:
								pass
					print('{}| {}'.format(x.center(20), str(round(robots[x]['score'], 1)).center(20)))
				print('----------------------------------------------')
				print('{}:{}'.format('Time'.center(5), str(int(diffStartTime)).center(5)))
				time.sleep(0.2)
