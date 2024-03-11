
class obj:
    def __init__(self):
        self.x = 1
        self.y = 2


a = obj()

b = a

b.x = 3

print(a.x)  # 3
