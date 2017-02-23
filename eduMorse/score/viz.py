import json
import os
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

HOST = os.environ.get("EDUMORSE_VIZ_HOST")
PORT = int(os.environ.get("EDUMORSE_VIZ_PORT"))

if __name__ == '__main__':
    # connect to controller.py
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
