import os
import sys
import pygame
import requests
from io import BytesIO


def terminate():
    pygame.quit()
    sys.exit()


def get_image(pos, zoom):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        'll': pos,
        'z': zoom,
        'l': 'map',
        'size': "650,450"
    }
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.content)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return response.content


# Масштаб карты
zoom = input()
# Координаты (разделяются запятой)
coords = input()

# Инициализация
pygame.init()
screen = pygame.display.set_mode((650, 450))
pygame.display.set_caption("MapsAPI")
clock = pygame.time.Clock()
FPS = 60

running = True
# 4
# 29.897824,59.865449

screen.blit(pygame.image.load(BytesIO(get_image(coords, zoom))), (0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)

terminate()

# main
# # Created by Sergey Yaksanov at 08.02.2021
# Copyright © 2020 Yakser. All rights reserved.
