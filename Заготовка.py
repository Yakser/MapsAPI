import pygame
import pygame_gui


pygame.init()
screen = pygame.display.set_mode((900, 600))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()