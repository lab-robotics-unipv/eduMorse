import socket

robot_sender = b'robot'
robot_destination = b'robot2'
robot_message = b'ciao'
HOST = 'localhost'
PORT = 4001
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.sendall(robot_sender + b'/' + robot_destination + b'/' + robot_message)
	s.close()
