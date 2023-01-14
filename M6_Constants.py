import pygame
from os import path


W = 1920
H = 1080
FPS = 60

B = (255, 255, 255)

# создание окна игры
pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption('me game')
CLOCK = pygame.time.Clock()

IMG_DIR = path.join(path.dirname(__file__), 'img')
DATE_DIR = path.join(path.dirname(__file__), 'date')

IMG = {'p_img': pygame.image.load(path.join(IMG_DIR, 'plain1.png')),
       'astr_img': pygame.image.load(path.join(IMG_DIR, 'asteroid_64x64_1.png')),
       'c_img': ((pygame.image.load(path.join(IMG_DIR, 'cursor_norm.png')), pygame.image.load(path.join(IMG_DIR, 'cursor_norm_hit.png'))),
                 (pygame.image.load(path.join(IMG_DIR, 'cursor_left.png')), pygame.image.load(path.join(IMG_DIR, 'cursor_left_hit.png'))))}

BUTTON_IMG_DIR = path.join(IMG_DIR, 'buttons')
BUTTON_IMG = {'button_corner': pygame.image.load(path.join(BUTTON_IMG_DIR, 'button_corner.png'))}

SHIPS_IMG_DIR = path.join(IMG_DIR, 'ships')
file = open(path.join(DATE_DIR, 'date_ships.txt'), 'rt')
SHIPS = file.read().split()
for i in SHIPS:
    ship = i.split(';')
    IMG[ship[0]] = pygame.image.load(path.join(SHIPS_IMG_DIR, ship[1].split(':')[0])).convert_alpha(SCREEN)

file = open(path.join(DATE_DIR, 'date_weapon.txt'), 'rt')
WEAPON = file.read().split()

file = open(path.join(DATE_DIR, 'date_animations.txt'), 'rt')
ANIM = file.read().split()
ANIMATIONS = {}
for i in ANIM:
    i_splited = i.split(';')
    if i_splited[0].split('.')[1] == '02':
        img_list = []
        direkt = path.join(IMG_DIR, i_splited[1].split(':')[0])
        for j in range(int(i_splited[1].split(':')[1])):
            j += 1
            img_list += [pygame.image.load(path.join(direkt, i_splited[1].split(':')[0] + '_' + str(j) + '.png')).convert_alpha(SCREEN)]
        ANIMATIONS[i_splited[0]] = img_list