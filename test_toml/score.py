import pymorse
import pytoml as toml
import os
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

PWD = os.path.join(os.environ['HOME'], 'simulator/test_toml')
MORSELABPATH = os.environ.get("MORSELABPATH")
GAMESPATH = os.path.join(MORSELABPATH, "games")

if __name__ == '__main__':
	startTime = time.time()
	maxScore = 100

	with pymorse.Morse() as simu:
		robots = {}
		for x in simu.robots:
			robots[x] = {}
			robots[x]['score'] = maxScore

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
	while not ((endTime and timeSimu <= 0) or (scoreZero and max([i['score'] for i in robots.values()]) <= 0)):
		print('\033[H\033[2J')
		for x in robots.keys():
			robots[x]['score'] -= loss
			robots[x]['score'] = max(robots[x]['score'], 0)
			print("Robot '{}' score = {}".format(x, robots[x]['score']))
			#sys.stdout.write("Robot '{}' score = {}".format(x, robots[x]['score']))
			#sys.stdout.flush()
		time.sleep(0.1)
		timeSimu = timeSimu - (time.time() - startTime)
