import pygame
import M1_Objects
import M2_Player
import M3_Groups
from os import path
import M6_Constants

# создание окна игры
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((M6_Constants.W, M6_Constants.H))
pygame.display.set_caption('me game')
clock = pygame.time.Clock()

# создание груп спрайтов
all_sprits = M3_Groups.Large_Sprite_Group()
cur = M1_Objects.Cursor(M6_Constants.IMG['c_img'])
all_sprits.add(cur)

pygame.mouse.set_visible(False)

# запуск игрового цикла
r = True
while r:
    clock.tick(M6_Constants.FPS)
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                all_sprits.respawn()

    # обновление спрайтов и прорисовка
    all_sprits.update()
    all_sprits.action()
    all_sprits.calculation_relative_coordinates()

    screen.fill((0, 0, 35))

    all_sprits.draw(screen)
    pygame.display.flip()

pygame.quit()
