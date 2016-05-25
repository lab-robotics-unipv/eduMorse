#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <sim> environment

Feel free to edit this template as you like!
"""

from morse.builder import *
import pytoml as toml
import os

# control if a file exists
def findFileInPath(filename, extension, paths):
	for path in paths:
		if os.path.exists(os.path.join(path, filename)):
			return os.path.join(path, filename)
		elif os.path.exists(os.path.join(path, filename + '.' + extension)):
			return os.path.join(path, filename + '.' + extension)
	raise FileNotFoundError('File ' + filename + ' not found')

def main():

	############################################################
	# IMPORTANT PATHS
	############################################################

	PWD = os.path.join(os.environ['HOME'], 'simulator/test_toml')
	GAMESPATH = os.environ.get("GAMESPATH")
	MAPSPATH = os.path.join(GAMESPATH, "maps")
	OBJECTSPATH = os.path.join(GAMESPATH, "objects")
	ROBOTSPATH = os.path.join(GAMESPATH, "robots")

	############################################################
	# GAME CONFIGURATION
	############################################################

	# Open and load the local file containing the configuration of the simulation
	with open(os.path.join(PWD, "g.toml"), 'r') as gfile:
		simulation = toml.loads(gfile.read())

		# Check if game file exists and load it
		game_name = simulation['game']['name']
		try:
			game_name = findFileInPath(game_name, 'toml', [PWD, GAMESPATH])
		except:
			raise

		with open(game_name) as gamefile:
			game = toml.loads(gamefile.read())


			# Control if any robot file exists and collect them in a list
			num_robot = game['game']['numrobot']
			robot_file_list = []
			num = 0
			for robot_file in simulation['game']['robot_file']:
				try:
					rf = findFileInPath(robot_file, 'toml', [PWD, ROBOTSPATH])
				except:
					raise
				robot_file_list.append(rf)

			# Open and load any robot file and collect them in a list
			config = []
			for robot_file in robot_file_list:
				with open(os.path.join(PWD, robot_file)) as conffile:
					config.append(toml.loads(conffile.read()))

			# Check if the number of robots is higher than the admitted one
			for c in config:
				num += len(c['robot'])
				if num > num_robot:
					raise Exception('Too many robots')

			# Check if the files are used once
			if len(set(robot_file_list)) < len(robot_file_list):
				raise Exception('Robot files with the same name')


			############################################################
			# ROBOT CONFIGURATION
			############################################################

			for robot_config in config:
				robots = []
				for rob in robot_config['robot']:
					if rob['id'] in robots:
						raise Exception('Robot id is not unique')

					robot = eval(rob['type'] + '()')
					robot.name = rob['id']
					aes = []  #actuators and sensors

					for act in rob['actuators']:
						if act['id'] in aes:
							raise Exception('Error: actuator id is not unique')
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

			for pos in game['game']['robot_position']:
				robot.translate(pos['x'], pos['y'])


			############################################################
			# OBJECT CONFIGURATION
			############################################################

			num_object = game['game']['numobject']
			objects = []
			for o in game['game']['objects']:
				try:
					object_file = findFileInPath(o['file'], 'blend', [PWD, OBJECTSPATH])
				except:
					raise
				objects.append(o['file'])

			if len(objects) > num_object:
				raise Exception('Too many objects')

			for o in game['game']['objects']:
				obj = PassiveObject(object_file, o['type'])
				obj.translate(o['x'], o['y'], o['z'])
				for prop in o['properties']:
					obj.properties(Label = prop['label'], GOAL = prop['goal'])


			############################################################
			# ENVIRONMENT CONFIGURATION
			############################################################

			# Check if map file exists
			game_map = game['game']['map']
			try:
				game_map = findFileInPath(game_map, 'blend', [PWD, MAPSPATH])
			except:
				raise

			fmode = simulation['game']['fastmode']

			env = Environment(game_map, fastmode = fmode)

			for cam in game['game']['camera_position']:
				env.set_camera_location([cam['x_cam'], cam['y_cam'], cam['z_cam']])
				env.set_camera_rotation([cam['p_cam'], cam['q_cam'], cam['r_cam']])

			camera = VideoCamera()
			for cam in simulation['game']['camera_position']:
				camera.translate(cam['x_cam'], cam['y_cam'], cam['z_cam'])
				camera.rotate(cam['p_cam'], cam['q_cam'], cam['r_cam'])
			camera.properties(Vertical_Flip=False)
			robot.append(camera)
			env.select_display_camera(camera)

if __name__ == "__main__":
	main()

