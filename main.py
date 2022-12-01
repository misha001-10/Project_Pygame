import pygame
import M1_Objects
import M2_Player
import M3_Groups
from os import path

W = 1440
H = 960
FPS = 60

B = (255, 255, 255)

img_dir = path.join(path.dirname(__file__), 'img')

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('me game')
clock = pygame.time.Clock()

p_img = pygame.image.load(path.join(img_dir, 'plain.png')).convert(screen)
astr_img = pygame.image.load(path.join(img_dir, 'asteroid_64x64_1.png')).convert(screen)
c_img = [pygame.image.load(path.join(img_dir, 'cursor_norm.png')).convert(screen),
         pygame.image.load(path.join(img_dir, 'cursor_left.png')).convert(screen)]

all_sprits = M3_Groups.Large_Sprite_Group(p_img)
#for i in range(15):
objekt = M1_Objects.Object(astr_img, [0, 210], 0)
all_sprits.add(objekt)
objekt = M1_Objects.Object(astr_img, [210, 0], 0)
all_sprits.add(objekt)
objekt = M1_Objects.Object(astr_img, [0, 0], 0)
all_sprits.add(objekt)
cur = M1_Objects.Cursor(c_img)
all_sprits.add(cur)

pygame.mouse.set_visible(False)

position = [0, 0]
r = True
while r:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False

    position = all_sprits.player.update_player(position)
    all_sprits.update()
    all_sprits.action()
    all_sprits.collide()
    all_sprits.calculation_relative_coordinates(position)
    #print(position)

    screen.fill((0, 0, 35))

    all_sprits.draw(screen)
    pygame.display.flip()

pygame.quit()
