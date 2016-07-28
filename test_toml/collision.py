import pymorse

period = 1/3

def counter(data, x, robots):

	if data["collision"]: # collision occured
		if robots[x]['obj'] == data["objects"]: # robot collides again with the same object of the previous collision

			# check if robot is still colliding against the object considering the frequency of the sensor
			if (data['timestamp'] - robots[x]['timestamp']) > 1.2*period: # 1.2=factor of security for float count
				robots[x]['nb_collisions'] += 1
				print("Collision with {}! In total, {} collisions occured, robot name '{}'".format(robots[x]['obj'], robots[x]['nb_collisions'], x))

		else:
			# robot collides with a different object than the previous collision
			robots[x]['nb_collisions'] += 1
			robots[x]['obj'] = data["objects"]
			print("Collision with {}! In total, {} collisions occured, robot name '{}'".format(robots[x]['obj'], robots[x]['nb_collisions'], x))

		robots[x]['timestamp'] = data["timestamp"] # timestamp is registered every time


with pymorse.Morse() as simu:
	robots = {}
	for x in simu.robots:
		robots[x] = {}
		robots[x]['timestamp'] = 0
		robots[x]['nb_collisions'] = 0
		robots[x]['obj'] = None

	for x in robots.keys():
		simu.__dict__[x].collision.subscribe(lambda data: counter(data, x, robots))

	print("Press ctrl+C to stop")
	while True:
		simu.sleep(10)
