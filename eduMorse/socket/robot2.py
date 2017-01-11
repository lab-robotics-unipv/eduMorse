import select
import socket

def receive(conn):
    data = b''
    word = b''
    while word != b'\x04':
        data += word
        word = conn.recv(1)
    message = data.decode('utf-8')
    return message


def send(stringa, socket):
    message = stringa + '\x04'
    socket.sendall(message.encode('utf-8'))


def messageInSocket(s):
    read_list, _, _ = select.select([s], [], [], 0)
    if read_list == []:
        return False
    else:
        return True


robot_sender = 'robot2'
robot_receiver = 'robot'
HOST = 'localhost'
PORT = 4001

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        send(robot_sender, s)
        start = ''
        while 'Start' not in start:
            start = receive(s)
            print(start)

        message = robot_receiver + '{ciao}'
        send(message, s)

        while not messageInSocket(s):
            pass
        data = receive(s)
        print(data)

        while not messageInSocket(s):
            pass
        data = receive(s)
        print(data)

        s.close()
