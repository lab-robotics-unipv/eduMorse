import os
import socket
import socketComm

robot_sender = 'robot2'
robot_receiver = 'robot'
HOST = os.environ.get("EDUMORSE_ROBOT2_HOST")
PORT = int(os.environ.get("EDUMORSE_ROBOT2_PORT"))

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        socketComm.send(robot_sender, s)
        start = ''
        while 'Start' not in start:
            start = socketComm.receive(s)
            print(start)

        text = 'Hello from robot2!'
        message = {robot_receiver : text}
        socketComm.send(message, s)

        while not socketComm.messageInSocket(s):
            pass
        data = socketComm.receive(s)
        msg = data['robot2']
        print(msg)

        while not socketComm.messageInSocket(s):
            pass
        data = socketComm.receive(s)
        msg = data['robot2']
        print(msg)

        s.close()
