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

def addCollisionToRobot(robot):
	collision = Collision()
	collision.translate(0, 0, 0)
	collision.properties(only_objects_with_property="Object")
	collision.scale = (0.8, 0.6, 0.8)
	collision.frequency(3)
	collision._make_transparent(collision._bpy_object, 0)
	collision._bpy_object.game.physics_type = 'RIGID_BODY'
	collision.add_interface("socket")
	robot.append(collision)

def main():

	############################################################
	# IMPORTANT PATHS
	############################################################

	PWD = os.path.join(os.environ['HOME'], 'simulator/test_toml')
	MORSELABPATH = os.environ.get("MORSELABPATH")
	GAMESPATH = os.path.join(MORSELABPATH, "games")
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
			for robot_file in simulation['game']['robot']:
				try:
					rf = findFileInPath(robot_file['file'], 'toml', [PWD, ROBOTSPATH])
				except:
					raise
				robot_file_list.append((robot_file['name'], rf))

			# Open and load any robot file and collect them in a list
			config = []
			for robot_file in robot_file_list:
				with open(robot_file[1]) as conffile:
					config.append((robot_file[0], toml.loads(conffile.read())))

			# Check if the number of robots is higher than the admitted one
			if len(config) > num_robot:
				raise Exception('Too many robots')

			# Check if the robots are used once
			if len(set([name[0] for name in robot_file_list])) < len([name[0] for name in robot_file_list]):
				raise Exception('Robots with the same name')


			############################################################
			# ROBOT CONFIGURATION
			############################################################

			positions = list(game['game']['robot_position'])

			for robot_config in config:
				rob = robot_config[1]['robot']
				robot = eval(rob['type'] + '()')
				robot.name = robot_config[0]
				aes = []  #actuators and sensors

				for act in rob['actuators']:
					if act['id'] in aes:
						raise Exception('Error: actuator id is not unique')
					if act['type'] in game['game']['actuators']:
						actuator = eval(act['type'] + '()')
						actuator.name = act['id']
						p = act.get('properties', None)
						if p:
							actuator.properties(**p)
						i = act.get('interface', None)
						if i:
							iprop = i.get('properties', None)
							itype = i['type']
							if iprop:
								actuator.add_interface(itype, **iprop)
							actuator.add_interface(itype)
						robot.append(actuator)
						aes.append(act['id'])
					else:
						raise Exception('Actuator type not allowed in this game')

				for sens in rob['sensors']:
					if sens['type'] in game['game']['sensors']:
						sensor = eval(sens['type'] + '()')
						sensor.name = sens['id']
						p = sens.get('properties', None)
						if p:
							sensor.properties(**p)
						i = sens.get('interface', None)
						if i:
							iprop = i.get('properties', None)
							itype = i['type']
							if iprop:
								sensor.add_interface(itype, **iprop)
							sensor.add_interface(itype)
						robot.append(sensor)
						aes.append(sens['id'])
					else:
						raise Exception('Sensor type not allowed in this game')

				addCollisionToRobot(robot)

				pos = positions.pop()
				robot.translate(pos['x'], pos['y'])
				robot.rotate()


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
				objects.append((object_file, o))

			if len(objects) > num_object:
				raise Exception('Too many objects')

			object_name = []
			for i in objects:
				if i[1]['name'] in object_name:
					raise Exception('Object name is not unique')
				obj = PassiveObject(i[0])
				obj.name = i[1]['name']
				obj.translate(i[1]['x'], i[1]['y'], i[1]['z'])
				p = i[1].get('properties', None)
				if p:
					obj.properties(**p)
				object_name.append(i[1]['name'])


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

