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

all_sprits = M3_Groups.Large_Sprite_Group()
objekt = M1_Objects.Object(0, astr_img, [0, 0], 0)
all_sprits.add(objekt)
player = M2_Player.Player(0, p_img)
all_sprits.add(player)
position = [0, 0]
r = True
while r:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False

    position = player.update_player(position)
    all_sprits.update(position)
    all_sprits.action(position)
    all_sprits.collide()
    #print(position)

    screen.fill((0, 0, 35))

    all_sprits.draw(screen)
    pygame.display.flip()

pygame.quit()
