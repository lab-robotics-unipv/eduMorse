import pymorse
import socket
import time


class count:

    def __init__(self, x, socket):
        self.x = x
        self.period = 1/3
        self.socket = socket
        self.nb_collisions = 0
        self.obj = {}

    def send(self, robot, obj, socket):
        if len(obj) > 0:
            message = robot + '.' + '.'.join(obj) + '\x04'
            socket.sendall(message.encode('utf-8'))

    def counter(self, data):
        if data["collision"]: # collision occurred
            objs = []

            for o in data["objects"].split(','):
                if o in self.obj.keys(): # robot collides again with the same object of the previous collision

                    # check if robot is still colliding against the object considering the frequency of the sensor
                    if (data['timestamp'] - self.obj[o]['timestamp']) > 1.2*self.period: # 1.2=factor of security for float count
                        self.nb_collisions += 1
                        #print("Collision with {}! In total, {} collisions occurred, robot name '{}'".format(self.obj, self.nb_collisions, self.x))
                        objs.append(o)

                else:
                    # robot collides with a different object than the previous collision
                    self.nb_collisions += 1
                    self.obj[o] = {}
                    #print("Collision with {}! In total, {} collisions occurred, robot name '{}'".format(self.obj, self.nb_collisions, self.x))
                    objs.append(o)


                self.obj[o]['timestamp'] = data["timestamp"] # timestamp is registered every time
            self.send(self.x, objs, self.socket)

HOST = ''
PORT = 50000

if __name__ == '__main__':
    with pymorse.Morse() as simu:
        robots = {}
        for x in simu.robots:
            robots[x] = {}

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(1)
            conn, addr = s.accept()

            l = {}
            for x in robots.keys():
                l[x] = count(x, conn)

            for x in robots.keys():
                simu.__dict__[x].eduMorse_default_collision_sensor.subscribe(l[x].counter)

            #print("Press ctrl+C to stop")
            while True:
                time.sleep(10)
