import socket
import threading
import pickle
import Types

from PlayerTest import *


class Client:
    def __init__(self, player: Player):
        # Player settings
        self.player = player
        self.enemy_player = None
        self.name = f"Player {self.player.name}"
        self.enemy_moves = []
        self.last_action = None

        # Server settings
        host, port = input("Enter the server IP address :\n>>"), 12345
        self.host, self.port = (host, port)

        # Socket / Thread settings
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        print("Connected to the server !")

        thread = threading.Thread(target=self.handle)
        thread.start()
        
    def set_name(self, name: str) -> None:
        self.client.send(name.encode('utf-8'))    

    def handle(self) -> None:
        while True:
            data = self.client.recv(4096)
            if data:
                obj = pickle.loads(data)
                if isinstance(obj, Player):
                    self.enemy_player = obj
                else:
                    self.enemy_moves.append(obj)
                    self.last_action = obj  

    def is_there_info(self) -> bool:
        return True if len(self.enemy_moves) > 0 else False

    def send_info(self, info) -> None:
        self.client.send(pickle.dumps(info))
    
    def get_last_info(self):
        while len(self.enemy_moves) == 0:
            pass
        return self.enemy_moves.pop()

    def reset_last_info(self) -> None:
        self.enemy_moves = []
    
    def stop(self) -> None:
        self.client.close()
