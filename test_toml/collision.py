import pymorse
import socket

period = 1/3
HOST = ''
PORT = 50000

def send(robot, obj, socket):
	message = robot + '.' + obj + '\x04'
	socket.sendall(message.encode('utf-8'))


def counter(data, x, robots, socket):

	if data["collision"]: # collision occurred
		for o in data["objects"].split(','):
			if robots[x]['obj'] == o: # robot collides again with the same object of the previous collision

				# check if robot is still colliding against the object considering the frequency of the sensor
				if (data['timestamp'] - robots[x]['timestamp']) > 1.2*period: # 1.2=factor of security for float count
					robots[x]['nb_collisions'] += 1
					#print("Collision with {}! In total, {} collisions occured, robot name '{}'".format(robots[x]['obj'], robots[x]['nb_collisions'], x))
					send(x, robots[x]['obj'], socket)

			else:
				# robot collides with a different object than the previous collision
				robots[x]['nb_collisions'] += 1
				robots[x]['obj'] = o
				#print("Collision with {}! In total, {} collisions occured, robot name '{}'".format(robots[x]['obj'], robots[x]['nb_collisions'], x))
				send(x, robots[x]['obj'], socket)

			robots[x]['timestamp'] = data["timestamp"] # timestamp is registered every time


if __name__ == '__main__':
	with pymorse.Morse() as simu:
		robots = {}
		for x in simu.robots:
			robots[x] = {}
			robots[x]['timestamp'] = 0
			robots[x]['nb_collisions'] = 0
			robots[x]['obj'] = None

		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((HOST, PORT))
			s.listen(1)
			conn, addr = s.accept()

			for x in robots.keys():
				simu.__dict__[x].collision.subscribe(lambda data: counter(data, x, robots, conn))

			print("Press ctrl+C to stop")
			while True:
				s.close()
				simu.sleep(10)
