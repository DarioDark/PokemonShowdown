import pygame

pygame.init()
screen = pygame.display.set_mode((960, 540))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        print(event)
    pygame.display.update()