import os
import sys
import pygame
import requests


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("MapsAPI")
clock = pygame.time.Clock()
FPS = 60
# Масштаб карты
zoom = float(input())
# Координаты (разделяются запятой)
coords = input()

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)

terminate()

# main
# # Created by Sergey Yaksanov at 08.02.2021
# Copyright © 2020 Yakser. All rights reserved.
