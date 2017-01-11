import pymorse
import select
import socket
import sys
import time

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

def checkString(message, robots):
    bracket = message.find('{')
    if bracket <= 0 or bracket == len(message) - 1 or message[-1] != '}':
        return None
    stringa = [message[:bracket], message[bracket:]]
    if stringa[0] not in robots.keys():
        return None
    return stringa


def checkTimestamp(address, conn):
    timestamp = time.time()
    if timestamp <= address[conn.getpeername()]['timestamp']:
        return None
    address[conn.getpeername()]['timestamp'] = timestamp
    return 0


HOST = ''
PORT = 4001
if __name__ == '__main__':
    with pymorse.Morse() as simu:
        robots = {}
        robots['SCORE'] = {}
        robots['SCORE']['flag'] = False
        for x in simu.robots:
            robots[x] = {}
            robots[x]['flag'] = False

    try:
        address = {}
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        i = 0
        while i < len(robots.keys()):
            conn, addr = s.accept()
            robot = receive(conn)

            if robots[robot]['flag']:
                raise ValueError

            robots[robot]['conn'] = conn
            robots[robot]['flag'] = True
            address[addr] = {}
            address[addr]['robot'] = robot
            address[addr]['timestamp'] = 0
            i = i + 1

    except KeyError:
        print('Wrong robot name')
        s.close()
        for x in robots.keys():
            if robots[x]['flag']:
                robots[x]['conn'].close()
        sys.exit(1)
    except ValueError:
        print("Robot '{}' already connected".format(robot))
        s.close()
        for x in robots.keys():
            if robots[x]['flag']:
                robots[x]['conn'].close()
        sys.exit(1)

    for x in robots.keys():
        send('Start', robots[x]['conn'])
    print('Start send')

    try:
        while True:
            read_list, _, _ = select.select([robots[x]['conn'] for x in robots.keys()], [], [])
            for x in read_list:
                message = receive(x)
                stringa = checkString(message, robots)
                if stringa == None:
                    continue
                if checkTimestamp(address, x) == None:
                    continue
                send(stringa[1], robots[stringa[0]]['conn'])
    except (KeyboardInterrupt, SystemExit):
        s.close()
        for x in robots.keys():
            robots[x]['conn'].close()
        print('server.py is shutting down')
        sys.exit(0)
