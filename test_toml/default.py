#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <my_project> environment

Feel free to edit this template as you like!
"""

from morse.builder import *
import pytoml as toml

with open("test_toml/r.toml") as conffile:
    config = toml.loads(conffile.read())

robots = []
for rob in config['robot']:
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
        motion = eval(act['type'] + '()')
        motion.name = act['id']
        robot.append(motion)
        aes.append(act['id'])
    for sens in rob['sensors']:
        sensor = eval(sens['type'] + '()')
        sensor.name = sens['id']
        #print('#####')
        #print(sensor.__dict__)#.get_properties()
        #print('#####')
        #print(type(sensor))
        robot.append(sensor)
        #sensor.get_properties()
        #sensor.set_property('ControlType', 'Position')
        sensor.properties(**sens['properties'])
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

