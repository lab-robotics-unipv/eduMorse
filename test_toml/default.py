#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <my_project> environment

Feel free to edit this template as you like!
"""

from morse.builder import *
import pytoml as toml
import os

PWD = os.path.join(os.environ['HOME'], 'simulator/test_toml')
GAMESPATH = os.environ.get("GAMESPATH")
MAPSPATH = os.path.join(GAMESPATH, "maps")

# Control if a file exists
def findFile(filename, extension, paths):
	for path in paths:
		if os.path.exists(os.path.join(path, filename)):
			return os.path.join(path, filename)
		elif os.path.exists(os.path.join(path, filename + '.' + extension)):
			return os.path.join(path, filename + '.' + extension)
	raise FileNotFoundError('File ' + filename + ' not found')

# Load the game configuration file
with open(os.path.join(PWD, "g.toml")) as gfile:
	g = toml.loads(gfile.read())

# Check if game file exists and load it
game_name = g['game']['game']
try:
	game_file = findFile(game_name, 'toml', [PWD, GAMESPATH])
except:
	raise

with open(game_file) as gamefile:
	game = toml.loads(gamefile.read())

# Check if map file exists
map_name = game['game']['map']
try:
    map_file = findFile(map_name, 'blend', [PWD, MAPSPATH])
except:
    raise

# TODO se più file si chiamano uguale


# Check if any robot file exists and if we have the right number of robots
num_robot = game['game']['numrobot']
config = []
num = 0
for r in g['game']['robot_file']:
	try:
		robot_file = findFile(r, 'toml', [PWD])
	except:
		raise

	with open(robot_file) as rfile:
		config.append(toml.loads(rfile.read()))
	for i in config:
		num += len(i['robot'])

	if num > num_robot:
		raise Exception('Too many robots')

# robot configuration files
for robot_config in config:
	robots = []
	for rob in robot_config['robot']:
		if rob['id'] in robots:
			raise Exception('Robot id is not unique')

		robot = eval(rob['type'] + '()')
		robot.name = rob['id']
		x = rob['x']
		y = rob['y']
		z = rob['z']
		p = rob['p']
		q = rob['q']
		r = rob['r']
		robot.translate(x, y, z)
		robot.rotate(p, q, r)
		aes = []  #actuators and sensors

		for act in rob['actuators']:
			if act['id'] in aes:
				raise Exception('Actuator id is not unique')
			actuator = eval(act['type'] + '()')
			actuator.name = act['id']
			robot.append(actuator)
			aes.append(act['id'])

		for sens in rob['sensors']:
			sensor = eval(sens['type'] + '()')
			sensor.name = sens['id']
			sensor.properties(**sens['properties'])
			robot.append(sensor)
			aes.append(sens['id'])

		for interf in rob['interface']:
			robot.add_default_interface(interf['type'])

		robots.append(rob['id'])


# TODO tirare dentro gli oggetti
num_object = game['game']['numobject']

# TODO add fastmode to config file
env = Environment('indoors-1/indoor-1', fastmode = False)
#env = Environment(map_file, fastmode = False)

# TODO add camera to config and/or game config file
env.set_camera_location([-18.0, -6.7, 10.8])
env.set_camera_rotation([1.09, 0, -1.14])

# Add the MORSE mascott, MORSY.
# Out-the-box available robots are listed here:
# http://www.openrobots.org/morse/doc/stable/components_library.html
#
# 'morse add robot <name> my_project' can help you to build custom robots.
# robot = Morsy()

# The list of the main methods to manipulate your components
# is here: http://www.openrobots.org/morse/doc/stable/user/builder_overview.html
# robot.translate(1.0, 0.0, 0.0)
# robot.rotate(0.0, 0.0, 3.5)

# Add a motion controller
# Check here the other available actuators:
# http://www.openrobots.org/morse/doc/stable/components_library.html#actuators
#
# 'morse add actuator <name> my_project' can help you with the creation of a custom
# actuator.
# motion = MotionVW()
# robot.append(motion)


# Add a keyboard controller to move the robot with arrow keys.
#keyboard = Keyboard()
# robot.append(keyboard)
# keyboard.properties(ControlType = 'Position')


# Add a pose sensor that exports the current location and orientation
# of the robot in the world frame
# Check here the other available actuators:
# http://www.openrobots.org/morse/doc/stable/components_library.html#sensors
#
# 'morse add sensor <name> my_project' can help you with the creation of a custom
# sensor.
# pose = Pose()
# robot.append(pose)

# To ease development and debugging, we add a socket interface to our robot.
#
# Check here: http://www.openrobots.org/morse/doc/stable/user/integration.html
# the other available interfaces (like ROS, YARP...)
# robot.add_default_interface('socket')


# set 'fastmode' to True to switch to wireframe mode
#env = Environment('indoors-1/indoor-1', fastmode = False)
#env.set_camera_location([-18.0, -6.7, 10.8])
#env.set_camera_rotation([1.09, 0, -1.14])

