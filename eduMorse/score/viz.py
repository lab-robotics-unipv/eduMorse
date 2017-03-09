import json
import os
import select
import socket
import time

def receive(conn):
    data = b''
    word = b''
    while word != b'\x04':
        data += word
        word = conn.recv(1)
    message = data.decode('utf-8')
    message = json.loads(message)
    return message

def send(msg, socket):
    message = json.dumps(msg)
    message = message + '\x04'
    socket.sendall(message.encode('utf-8'))

def messageInSocket(s):
    read_list, _, _ = select.select([s], [], [], 0)
    if read_list == []:
        return False
    else:
        return True

def outputPrint(robots, t):
    print('\033[H\033[2J')
    print('{}| {}'.format('Robot'.center(20), 'Score'.center(20)))
    print('----------------------------------------------')
    for x in robots.keys():
        print('{}| {}'.format(x.center(20), str(round(robots[x]['score'], 1)).center(20)))
    print('----------------------------------------------')
    print('{}:{}'.format('Time'.center(5), str(int(t)).center(5)))

HOST = os.environ.get("EDUMORSE_VIZ_HOST")
PORT = int(os.environ.get("EDUMORSE_VIZ_PORT"))

if __name__ == '__main__':
    # connect to controller.py
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        request = "VIZ_REQUEST"
        end = True
        try:
            while end:
                send(request, s)
                while messageInSocket(s):
                    message = receive(s)
                    if message[0] == "END_SIMULATION":
                        robots = message[1]
                        t = message[2]
                        outputPrint(robots, t)
                        end = False
                    else:
                        robots = message[0]
                        t = message[1]
                        outputPrint(robots, t)
                time.sleep(0.2)
        except (KeyboardInterrupt, SystemExit):
            print("viz.py is shutting down")
