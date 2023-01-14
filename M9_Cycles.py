import pygame
import sys
import M1_Objects
import M3_Groups
from M5_Network import Network
import M6_Constants


def terminate():
    pygame.quit()
    sys.exit()


def Game_body(net):
    # создание груп спрайтов
    all_sprits = M3_Groups.Large_Sprite_Group(net)

    pygame.mouse.set_visible(False)

    # запуск игрового цикла
    r = True
    while r:
        M6_Constants.CLOCK.tick(M6_Constants.FPS)
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RSHIFT:
                    all_sprits.respawn()

        # обновление спрайтов и прорисовка
        all_sprits.update()
        all_sprits.action()
        all_sprits.calculation_relative_coordinates()

        M6_Constants.SCREEN.fill((0, 0, 35))

        all_sprits.draw(M6_Constants.SCREEN)
        pygame.display.flip()


def Start_window():
    # создание груп спрайтов
    all_sprits = M3_Groups.Start_Sprite_Group()
    all_sprits.add(M1_Objects.Button(M6_Constants.BUTTON_IMG['button_corner'], (1600, 952)))

    pygame.mouse.set_visible(False)

    # запуск игрового цикла
    r = True
    while r:
        M6_Constants.CLOCK.tick(M6_Constants.FPS)
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYUP:
                return Network()

        # обновление спрайтов и прорисовка
        all_sprits.update()

        M6_Constants.SCREEN.fill((0, 0, 35))

        all_sprits.draw(M6_Constants.SCREEN)
        pygame.display.flip()