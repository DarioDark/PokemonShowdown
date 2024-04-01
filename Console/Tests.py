from ClientConsole import Client
from PlayerConsole import Player


player = Player("Player 1")
c = Client(player, "192.168.1.45", 12346)

result = c.start()
print(result)
