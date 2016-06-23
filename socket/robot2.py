import socket

robot_sender = b'robot2'
robot_receiver = b'robot'
HOST = 'localhost'
PORT = 4001
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.sendall(robot_sender)
	start = ''
	while 'Start' not in start:
		start = s.recv(1024).decode('utf-8')
	print(start)

	s.sendall(robot_receiver + b'{ciao}')
	data = s.recv(1024)
	print(data.decode('utf-8'))

	s.close()
