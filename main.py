import sys
import pygame
import requests
from io import BytesIO
import pygame_gui


def terminate():
    pygame.quit()
    sys.exit()


def get_bounds(coords):
    pass


def get_image(pos, zoom):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        'll': ','.join(map(str, pos)),
        'spn': ','.join(map(str, zoom)),
        'l': ['map', 'sat', 'sat,skl'][type_map],
        'size': "450,450",
    }
    if pt:
        map_params['pt'] = pt + ',flag'
    response = requests.get(map_api_server, params=map_params)

    if not response:
        return
    return response.content


# 29.897824,59.865449
# 71.653772,-84.912755
# 4
try:
    # Координаты (разделяются запятой)
    print("Введите координаты через запятую:")
    coords = list(map(float, input().split(',')))
    # Масштаб карты
    print("Введите масштаб карты (область показа в градусах, через запятую)")
    zoom = list(map(float, input().split(',')))
except Exception:
    print("Некорректные координаты!")
    terminate()

width, height = 450, 450
# Инициализация
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("MapsAPI")
clock = pygame.time.Clock()
FPS = 60
manager = pygame_gui.UIManager((width, height))
pt = None
running = True

type_map = 0
map_img = get_image(coords, zoom)
if not map_img:
    print("Некорректные координаты!")
    terminate()
screen.blit(pygame.image.load(BytesIO(map_img)), (0, 0))
view = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width - 115, 10), (100, 30)),
                                    text='Вид карты',
                                    manager=manager)
name_obj = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((width // 2 - 140, height - 50), (250, 200)),
                                               manager=manager)
search = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width // 2 + 115, height - 50), (55, 30)),
                                      text='Искать',
                                      manager=manager)
reset_search = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width // 2 - 160 - 55, height - 50), (70, 30)),
                                            text='Сбросить',
                                            manager=manager)
address_text = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((5, 10), (width - 125, 30)),
                                                   manager=manager)
address_text.disable()

while running:
    timedelta = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            # scaling

            if keys[pygame.K_PAGEUP]:
                zoom[0] /= 2
                zoom[1] /= 2
            if keys[pygame.K_PAGEDOWN]:
                zoom[0] *= 2
                zoom[1] *= 2
            # if scale_value:
            #     zoom += scale_value
            #     if zoom < 0:
            #         zoom = 0
            #     elif zoom > 17:
            #         zoom = 17

            screen.blit(pygame.image.load(BytesIO(get_image(coords, zoom))), (0, 0))

            dx, dy = 2 * zoom[0], 2 * zoom[1]
            # move
            dlat = dlon = 0
            if keys[pygame.K_LEFT]:
                dlon = -dx
            if keys[pygame.K_RIGHT]:
                dlon = dx
            if keys[pygame.K_DOWN]:
                dlat = -dy
            if keys[pygame.K_UP]:
                dlat = dy
            coords[0] += dlon
            coords[1] += dlat
            if dlon or dlat:
                map_img = get_image(coords, zoom)
                if not map_img:
                    coords[0] -= dlon
                    coords[1] -= dlat
                    map_img = get_image(coords, zoom)
                screen.blit(pygame.image.load(BytesIO(map_img)), (0, 0))

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element.text == 'Вид карты':
                    type_map = (type_map + 1) % 3
                    screen.blit(pygame.image.load(BytesIO(get_image(coords, zoom))), (0, 0))
                if event.ui_element.text == 'Искать':
                    geocoder = "http://geocode-maps.yandex.ru/1.x/"
                    name = name_obj.get_text()
                    geocoder_params = {
                        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                        "geocode": name,
                        "format": "json"
                    }

                    response = requests.get(geocoder, params=geocoder_params)
                    json_response = response.json()
                    if json_response['response']['GeoObjectCollection']['metaDataProperty'][
                        'GeocoderResponseMetaData']['found'] != '0':
                        toponym = json_response["response"]["GeoObjectCollection"][
                            "featureMember"][0]["GeoObject"]

                        address_text.set_text(toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted'])

                        coords = list(map(float, toponym["Point"]["pos"].split()))
                        pt = ','.join(map(str, coords))
                        screen.blit(pygame.image.load(BytesIO(get_image(coords, zoom))), (0, 0))

                if event.ui_element.text == 'Сбросить':
                    pt = ''
                    address_text.set_text('')
                    screen.blit(pygame.image.load(BytesIO(get_image(coords, zoom))), (0, 0))
                    name_obj.set_text("")

        manager.process_events(event)
    manager.update(timedelta)
    manager.draw_ui(screen)
    pygame.display.flip()
    clock.tick(FPS)

terminate()

# main
# # Created by Sergey Yaksanov at 08.02.2021
# Copyright © 2020 Yakser. All rights reserved
