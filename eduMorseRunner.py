#!/usr/bin/python3

import os
import subprocess
import sys
import time

MORSELABPATH = os.environ.get("MORSELABPATH")
SERVERPATH = os.path.join(MORSELABPATH, "socket")
TESTPATH = os.path.join(MORSELABPATH, "test_toml")

if len(sys.argv) != 2:
	print("Wrong number of parameters")
	sys.exit(1)

server = subprocess.Popen("python3 {}".format(os.path.join(SERVERPATH, "server.py")).split(" "))
print("server.py is running")
time.sleep(1)

collision = subprocess.Popen("python3 {}".format(os.path.join(TESTPATH, "collision.py")).split(" "))
print("collision.py is running")
time.sleep(1)

layer = subprocess.Popen("python3 {} {}".format(os.path.join(TESTPATH, "layer.py"), sys.argv[1]).split(" "))
print("layer.py is running")
time.sleep(1)

start = input("Type 'start' to count the score and to begin game: ")
if start == 'start':
	score = subprocess.Popen("python3 {} {}".format(os.path.join(TESTPATH, "score.py"), sys.argv[1]).split(" "))
	print("score.py is running")
	time.sleep(1)
	try:
		while True:
			pass
	except (KeyboardInterrupt, SystemExit):
		score.terminate()
		time.sleep(0.3)

		layer.terminate()
		time.sleep(0.3)

		collision.terminate()
		time.sleep(0.3)
		print("collision.py is shutting down")

		server.terminate()
		time.sleep(0.3)
else:
	print('Wrong command')
	layer.terminate()
	time.sleep(0.3)

	collision.terminate()
	time.sleep(0.3)

	server.terminate()
	time.sleep(0.3)
