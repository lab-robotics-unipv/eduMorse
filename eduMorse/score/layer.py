import pytoml as toml
import os
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
    return message


def send(robot, score, stop, socket):
    message = robot + '.' + str(score) + '.' + str(stop) + '\x04'
    socket.sendall(message.encode('utf-8'))


def messageInSocket(s):
    read_list, _, _ = select.select([s], [], [], 0)
    if read_list == []:
        return False
    else:
        return True


HOST = 'localhost'
PORT = 50000
PORTSCORE = 50001
MORSECONFIGPATH = os.path.join(os.environ['HOME'], '.morse/')
EDUMORSEPATH = os.environ.get("EDUMORSEPATH")
GAMESPATH = os.path.join(EDUMORSEPATH, "games")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Wrong number of parameters')

    SIMUPATH = findSimuPath(sys.argv[1])
    if SIMUPATH == None:
        raise Exception('Simulation name not found')

    #connect to collision.py
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # read layer configuration file
        with open(os.path.join(SIMUPATH, "simulation.toml"), 'r') as simulation_file:
            simulation = toml.loads(simulation_file.read())

            # Check if rules file exists and load it
            rules_name = simulation['simulation']['name']
            try:
                rules_name = findFileInPath(rules_name, 'toml', [SIMUPATH, GAMESPATH])
            except:
                raise

            with open(rules_name) as rules_file:
                rules = toml.loads(rules_file.read())
                layer = rules['simulation'].get('score', [])

                # open a socket to talk with score.py
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketScore:
                    socketScore.bind((HOST, PORTSCORE))
                    socketScore.listen(1)
                    conn, addr = socketScore.accept()

                    #print("Press ctrl+C to stop")

                    try:
                        while True:
                            if len(layer) == 0:
                                time.sleep(1)
                                continue

                            while not messageInSocket(s):
                                pass

                            message = receive(s)
                            parts = message.split('.')
                            robot = parts[0]
                            obj = parts[1:]

                            score = 0
                            stop = False
                            for l in layer:
                                for o in obj:
                                    if o in l['obj']:
                                        score += l['score']
                                        stop |= l['stop']
                                        send(robot, str(score), str(stop), conn)
                    except (KeyboardInterrupt, SystemExit):
                        s.close()
                        socketScore.close()
                        print("layer.py is shutting down")
