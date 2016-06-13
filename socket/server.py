import socket
import pymorse

robot_list = list()
HOST = ''
PORT = 50007
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen(5)
	conn, addr = s.accept()
	print('Got connection from', addr)
	simu = pymorse.Morse()
	robot_list = simu.robots
	data = conn.recv(1024)
	if not data:
		raise Exception('No data')
	#print(data.decode('utf-8'))
	stringa = data.decode('utf-8').split('/')
	print(stringa)
	if stringa[0] != stringa[1]:
		if (stringa[0] and stringa[1]) in robot_list:
			print('robots present')
			eval('simu.' + stringa[2])
		else:
			raise Exception('no robots with this name')
	else:
		raise Exception('Same robot used')
	s.close()
