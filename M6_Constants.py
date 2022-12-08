import pygame
from os import path


W = 1920
H = 1080
FPS = 60

B = (255, 255, 255)

IMG_DIR = path.join(path.dirname(__file__), 'img')

IMG = {'p_img': pygame.image.load(path.join(IMG_DIR, 'plain.png')),
       'astr_img': pygame.image.load(path.join(IMG_DIR, 'asteroid_64x64_1.png')),
       'c_img': (pygame.image.load(path.join(IMG_DIR, 'cursor_norm.png')),
                 pygame.image.load(path.join(IMG_DIR, 'cursor_left.png')))}