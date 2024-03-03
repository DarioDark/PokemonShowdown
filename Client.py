import socket
import threading
import pickle
import Types

from PlayerTest import *


class Client:
    def __init__(self, player: Player) -> None:
        self.player = player
        self.enemy_player = None
        self.name = f"Player {self.player.name}"
        self.enemy_moves = []
        self.last_action = None
        # Server settings
        self.host, self.port = ('', 12345) 
        self.start()
        self.set_name(self.name)
        
    def set_name(self, name: str) -> None:
        self.client.send(name.encode('utf-8'))    
    
    def start(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        print("Connected to the server !")
        
        thread = threading.Thread(target=self.handle)
        thread.start()
    
    def handle(self):
        while True:
            data = self.client.recv(4096)
            if data:
                obj = pickle.loads(data)
                if isinstance(obj, Player):
                    self.enemy_player = obj
                else:
                    self.enemy_moves.append(obj)
                    self.last_action = obj  
    
    def send_player(self):
        self.client.send(pickle.dumps(self.player))
        
    def send_damage(self, damage: int):
        self.client.send(pickle.dumps(damage))
        
    def send_action(self, action: tuple):
        self.client.send(pickle.dumps(action))
        
    def send_lead(self, lead: Pokemon):
        self.client.send(pickle.dumps(lead))    
    
    def get_last_info(self):
        while len(self.enemy_moves) == 0:
            pass
        return self.enemy_moves.pop()

    def reset_last_info(self):
        self.enemy_moves = []
    
    def stop(self):
        self.client.close()
