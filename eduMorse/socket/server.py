import json
import os
import pymorse
import pytoml as toml
import select
import socket
import sys
import time

# control if a file exists
def findFileInPath(filename, extension, paths):
    for path in paths:
        if os.path.exists(os.path.join(path, filename)):
            return os.path.join(path, filename)
        elif os.path.exists(os.path.join(path, filename + '.' + extension)):
            return os.path.join(path, filename + '.' + extension)
    raise FileNotFoundError('File ' + filename + ' not found')

# find the path of a simulation starting from the simulation name
def findSimuPath(simuName):
    with open(os.path.join(MORSECONFIGPATH, 'config'), 'r') as config:
        for line in config:
            if simuName in line:
                lineList = line.split(' = ')
                return lineList[1].strip('\n')
        return None

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

def checkMessage(message, robots):
    for r in message.keys():
        receiver = r
    if receiver not in robots.keys():
        return None
    msg = [receiver, message]
    return msg

def checkBandwidth(address, conn, message, frequency, length):
    # time limitation
    timestamp = time.time()
    if (timestamp - address[conn.getpeername()]['timestamp']) < (1/frequency):
        return None
    address[conn.getpeername()]['timestamp'] = timestamp
    # length limitation
    for r in message.keys():
        receiver = r
    text = message[receiver]
    if len(text) > length:
        return None
    return 0

MORSECONFIGPATH = os.path.join(os.environ['HOME'], '.morse/')
EDUMORSEPATH = os.environ.get("EDUMORSEPATH")
GAMESPATH = os.path.join(EDUMORSEPATH, "games")
HOST = os.environ.get("EDUMORSE_SERVER_HOST")
PORT = int(os.environ.get("EDUMORSE_SERVER_PORT"))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(len(sys.argv))
        raise Exception('Wrong number of parameters')

    SIMUPATH = findSimuPath(sys.argv[1])
    if SIMUPATH == None:
        raise Exception('Simulation name not found')

    # read configuration file
    with open(os.path.join(SIMUPATH, "simulation.toml"), 'r') as simulation_file:
        simulation = toml.loads(simulation_file.read())

        # Check if rules file exists and load it
        rules_name = simulation['simulation']['name']
        try:
            rules_name = findFileInPath(rules_name, 'toml', [SIMUPATH, GAMESPATH])
        except:
            raise

        with open(rules_name, 'r') as rules_file:
            rules = toml.loads(rules_file.read())
            frequency = rules['simulation']['bandwidth']['frequency']
            length = rules['simulation']['bandwidth']['length']

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
                msg = checkMessage(message, robots)
                if msg == None:
                    continue
                if checkBandwidth(address, x, message, frequency, length) == None:
                    continue
                send(msg[1], robots[msg[0]]['conn'])
    except (KeyboardInterrupt, SystemExit):
        s.close()
        for x in robots.keys():
            robots[x]['conn'].close()
        print('server.py is shutting down')
        sys.exit(0)
