import os
import socket
import socketComm
import time

robot_sender = 'robot'
robot_receiver = 'robot2'
HOST = os.environ.get("EDUMORSE_ROBOT_HOST")
PORT = int(os.environ.get("EDUMORSE_ROBOT_PORT"))

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        socketComm.send(robot_sender, s)
        start = ''
        while 'Start' not in start:
            start = socketComm.receive(s)
            print(start)

        #socketComm.stopRobot(robot_sender, s)

        text = 'Hello from robot!'
        message = {robot_receiver : text}
        socketComm.send(message, s)

        time.sleep(0.6)
        text = 'Hello again!'
        message = {robot_receiver : text}
        socketComm.send(message, s)

        while not socketComm.messageInSocket(s):
            pass
        data = socketComm.receive(s)
        msg = data['robot']
        print(msg)

        s.close()
