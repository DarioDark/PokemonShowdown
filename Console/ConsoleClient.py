import socket
import threading
import pickle
import time

from ConsolePlayerTest import *


class Client:
    def __init__(self, player: Player):
        # Player settings
        self.player = player
        self.enemy_player = None
        self.name = f"Player {self.player.name}"
        self.enemy_moves = []

        # Server settings
        host, port = input("Enter the server IP address :\n>>"), 12345
        self.host, self.port = (host, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.client.connect((self.host, self.port))
        self.send_info(self.player.name)
        self.send_info(self.player)
        print("Connected to the server !")


        thread = threading.Thread(target=self.handle)
        thread.start()

    def set_name(self, name: str) -> None:
        self.client.send(name.encode('utf-8'))    

    def handle(self) -> None:
        while True:
            data = self.client.recv(4096)
            if data:
                print("data")
                obj = pickle.loads(data)
                print("obj", obj)
                if isinstance(obj, Player):
                    if not self.enemy_player:
                        self.enemy_player = obj
                    print("player added", obj)
                else:
                    while len(self.enemy_moves) >= 1:
                        pass
                    self.enemy_moves.append(obj)
                    print("added")

    def send_info(self, info) -> None:
        print("sending")
        self.client.send(pickle.dumps(info))

    def get_enemy_player(self):
        while self.enemy_player is None:
            time.sleep(0.5)
        return self.enemy_player

    def get_last_info(self):
        while len(self.enemy_moves) == 0:
            print("waiting")
            time.sleep(1)
        print("returning")
        print("enemey moves", self.enemy_moves)
        return self.enemy_moves.pop(0)

    def reset_last_info(self):
        if len(self.enemy_moves) > 1:
            self.enemy_moves.pop(0)

    def stop(self) -> None:
        self.client.close()
