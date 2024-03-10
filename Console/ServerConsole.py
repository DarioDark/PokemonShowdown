import socket
import threading
import time
import pickle

from random import randint


class Server:
    def __init__(self):
        # Server settings
        self.host, self.port = ('0.0.0.0', 12345)
        self.clients: dict = {}
        self.players: list = []
        self.speed_tie_resolved: bool = False
        self.start()

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        print("Server started !")
        while True:
            client, addr = s.accept()
            print(f"Connection from {addr} has been established !")

            name = client.recv(4096)
            self.clients[name] = client

            player = client.recv(4096)
            self.players.append(player)

            if len(self.players) == 2:
                for client_index, client_name in enumerate(self.clients):
                    self.clients[client_name].send(self.players[client_index - 1])

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def handle(self, client):
        while True:
            data = client.recv(4096)
            if data:
                obj = pickle.loads(data)
                if obj == 'Speed tie':
                    if self.speed_tie_resolved:
                        self.speed_tie_resolved = False
                    else:
                        randomizer = randint(0, 1)
                        for index, name in enumerate(self.clients):
                            self.clients[name].send(pickle.dumps((randomizer - index)))
                        self.speed_tie_resolved = True
                else:
                    self.broadcast(data, client)

    def broadcast(self, data, client):
        print("Broadcasting data...")
        while len(self.clients) < 2:
            print("on attend", self.clients)
            time.sleep(1)
        for name in self.clients:
            if self.clients[name] != client:
                self.clients[name].send(data)
                print("Sent data to", name)

S = Server()
