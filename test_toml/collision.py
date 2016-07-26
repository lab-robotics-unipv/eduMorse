import pymorse

nb_collisions = 0

def counter(data):
	global nb_collisions

	if data["collision"]:
		nb_collisions += 1
		print("Collision with %s! In total, %d collisions occured" % (data["objects"], nb_collisions))


with pymorse.Morse() as morse:

	morse.robot.collision.subscribe(counter)

	print("Press ctrl+C to stop")
	while True:
		morse.sleep(10)
