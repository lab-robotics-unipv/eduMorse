import json
import select
import socket

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

if __name__ == '__main__':
    robot_sender = 'robot'
    robot_receiver = 'robot2'
    HOST = 'localhost'
    PORT = 4001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        send(robot_sender, s)
        start = ''
        while 'Start' not in start:
            start = receive(s)
            print(start)

        text = 'Hello from robot!'
        message = {robot_receiver : text}
        send(message, s)

        text = 'Hello again!'
        message = {robot_receiver : text}
        send(message, s)

        while not messageInSocket(s):
            pass
        data = receive(s)
        msg = data['robot']
        print(msg)

        s.close()
