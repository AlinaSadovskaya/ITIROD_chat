import json
import socket


class UDP:
    def __init__(self, host, port, buffer_size=1024):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.buffer_size = buffer_size

    def send(self, mess, host, port):
        msg = json.dumps(mess.__dict__)
        data = msg.encode('utf-8')
        self.sock.sendto(data, (host, port))

    def receive(self):
        data, address = self.sock.recvfrom(self.buffer_size)
        msg = data.decode('utf-8', errors='replace').strip()
        msg = json.loads(msg)
        return msg, address


class Message:
    def __init__(self, login, mess, status):
        self.login = login
        self.mess = mess
        self.status = status
