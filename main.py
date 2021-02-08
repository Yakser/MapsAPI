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
        'll': ','.join(map(str, pos)),
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


# Координаты (разделяются запятой)
coords = list(map(float, input().split(',')))
# Масштаб карты
zoom = int(input())

# Инициализация
pygame.init()
screen = pygame.display.set_mode((650, 450))
pygame.display.set_caption("MapsAPI")
clock = pygame.time.Clock()
FPS = 60

running = True
# 29.897824,59.865449
# 4

screen.blit(pygame.image.load(BytesIO(get_image(coords, zoom))), (0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            # scaling
            scale_value = 0
            if keys[pygame.K_PAGEUP]:
                scale_value = 1
            if keys[pygame.K_PAGEDOWN]:
                scale_value = -1
            if scale_value:
                zoom += scale_value
                if zoom < 0:
                    zoom = 0
                elif zoom > 17:
                    zoom = 17
                screen.blit(pygame.image.load(BytesIO(get_image(coords, zoom))), (0, 0))
            if zoom <= 5:
                d = 1
            elif zoom <= 12:
                d = .1
            elif zoom <= 15:
                d = .01
            else:
                d = .001
            # move
            dlat = dlon = 0
            if keys[pygame.K_LEFT]:
                dlon = -d
            if keys[pygame.K_RIGHT]:
                dlon = d
            if keys[pygame.K_DOWN]:
                dlat = -d
            if keys[pygame.K_UP]:
                dlat = d
            coords[0] += dlon
            coords[1] += dlat
            if dlon or dlat:
                screen.blit(pygame.image.load(BytesIO(get_image(coords, zoom))), (0, 0))

    pygame.display.flip()
    clock.tick(FPS)

terminate()

# main
# # Created by Sergey Yaksanov at 08.02.2021
# Copyright © 2020 Yakser. All rights reserved.
