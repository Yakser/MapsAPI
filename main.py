import os
import sys
import pygame
import requests
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("MapsAPI")
# Масштаб карты
zoom = float(input())
# Координаты (разделяются запятой)
coords = input()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
    pygame.display.flip()
pygame.quit()

# main
# # Created by Sergey Yaksanov at 08.02.2021
# Copyright © 2020 Yakser. All rights reserved.
