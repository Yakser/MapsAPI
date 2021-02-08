import os
import sys
import pygame
import requests
from io import BytesIO
import pygame_gui

def terminate():
    pygame.quit()
    sys.exit()


def get_image(pos, zoom, format=0):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        'll': pos,
        'z': zoom,
        'l': ['map', 'sat', 'sat,skl'][format]
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
coords = input()
# Масштаб карты
zoom = int(input())

width, height = 600, 450
# Инициализация
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("MapsAPI")
clock = pygame.time.Clock()
FPS = 60
manager = pygame_gui.UIManager((width, height))

running = True
# 4
# 29.897824,59.865449
type_map = 0
screen.blit(pygame.image.load(BytesIO(get_image(coords, zoom))), (0, 0))
rules = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width - 105, height - 90), (100, 50)),
                                     text='Вид карты',
                                     manager=manager)
while running:
    timedelta = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
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

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element.text == 'Вид карты':
                    type_map = (type_map + 1) % 3
                    screen.blit(pygame.image.load(BytesIO(get_image(coords, zoom, type_map))), (0, 0))
        manager.process_events(event)
    manager.update(timedelta)
    manager.draw_ui(screen)
    pygame.display.flip()
    clock.tick(FPS)

terminate()

# main
# # Created by Sergey Yaksanov at 08.02.2021
# Copyright © 2020 Yakser. All rights reserved.
