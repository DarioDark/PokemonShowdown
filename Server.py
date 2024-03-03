import socket
import threading

from PlayerTest import *
from os import system


class Server:
    def __init__(self) -> None:
        
        # Server settings
        self.host, self.port = ('0.0.0.0', 12345)
        self.clients = {}
        self.start()

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        print("Server started !")
        while True:
            client, addr = s.accept()
            print(f"Connection from {addr} has been established !")

            name = client.recv(1024).decode('utf-8')
            self.clients[name] = client
            print(self.clients.keys())
            
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def handle(self, client):
        while True:
            data = client.recv(4096)
            if data:
                self.broadcast(data, client)

    
    def broadcast(self, data, client):
        print("Broadcasting data...")
        for name in self.clients:
            if self.clients[name] != client:
                self.clients[name].send(data)
                print("Sent data to", name)
        
S = Server()
