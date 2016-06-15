import socket

robot_sender = b'robot2'
robot_destination = b'robot'
HOST = 'localhost'
PORT = 4002
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	data = s.recv(1024)
	print('Received' + data.decode('utf-8'))
	s.close()
