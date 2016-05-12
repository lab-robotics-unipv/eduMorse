#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <my_project> environment

Feel free to edit this template as you like!
"""

from morse.builder import *
import pytoml as toml
import os

PWD = '/home/robitca/simulator/test_toml'

GAMESPATH = os.environ.get("GAMESPATH")
MAPSPATH = os.path.join(GAMESPATH, "maps")

# control if a file exists
def findFile(filename, extension, paths):
	for path in paths:
		if os.path.exists(os.path.join(path, filename)):
			return os.path.join(path, filename)
		elif os.path.join(path, filename + '.' + extension):
			return os.path.join(path, filename + '.' + extension)
	raise FileNotFoundError('File ' + filename + ' not found')

# g.toml game configuration
with open(os.path.join(PWD, "g.toml")) as gfile:
	g = toml.loads(gfile.read())

game_name = g['game']['game']
try:
	findFile(game_name, 'toml', [PWD, GAMESPATH])
except:
	raise

with open(game_name) as gamefile:
	game = toml.loads(gamefile.read())

num_robot = game['game']['numrobot']
num_object = game['game']['numobject']
map_name = game['game']['map']

# TODO use findFile for maps and robots

# control if any robot file exists
for r in g['game']['robot_file']:
	robot_file = r + '.toml'
	if os.path.exists(os.path.join(PWD, robot_file)):
		pass
	else:
		print("Error: robot file doesn't exist")
		print('#############################')
		exit()
		config = []
		with open(os.path.join(PWD, robot_file)) as conffile:
			config.append(toml.loads(conffile.read()))
			#        for j in config:
			#           for i in config['robot']:

		if len(config) > num_robot:
			print("error: too many robots!")
			print('#############################')
			exit()

# robot configuration files
for robot_config in config:
	robots = []
	for rob in robot_config['robot']:
		if rob['id'] in robots:
			print('#############################')
			print('Error: robot id is not unique')
			print('#############################')
			exit()
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
					print('################################')
					print('Error: actuator id is not unique')
					print('################################')
					exit()
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
env = Environment('indoors-1/indoor-1', fastmode = False)
env.set_camera_location([-18.0, -6.7, 10.8])
env.set_camera_rotation([1.09, 0, -1.14])

