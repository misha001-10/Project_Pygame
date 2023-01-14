import pygame
import math


class Animation(pygame.sprite.Sprite):
    def __init__(self, img, cord):
        super(Animation, self).__init__()
        self.img = img
        self.image = self.img[0]
        self.cord = cord
        self.rect = self.image.get_rect(center=self.cord)
        self.anim_poz = 0

    def update(self):
        try:
            self.anim_poz += 1
            self.image = self.img[int(self.anim_poz / 2)]
        except Exception:
            self.kill()

    def calculation_relative_coordinates(self, position):
        self.rect.center = position[0] + self.cord[0], position[1] + self.cord[1]


class Animation_angle(Animation):
    def __init__(self, img, cord, angle):
        self.img = []
        for i in img:
            self.img += [pygame.transform.rotate(i, angle)]
        super(Animation_angle, self).__init__(self.img, cord)

    def update(self):
        try:
            self.anim_poz += 1
            self.image = self.img[int(self.anim_poz / 2)]
        except Exception:
            self.kill()

    def calculation_relative_coordinates(self, position):
        self.rect.center = position[0] + self.cord[0], position[1] + self.cord[1]


class Animation_angle_connection(Animation):
    def __init__(self, img, id, angle):
        self.id = id
        self.img = []
        for i in img:
            self.img += [pygame.transform.rotate(i, angle)]
        super(Animation_angle_connection, self).__init__(self.img, (0, 0))

    def update(self, all_pap):
        for i in all_pap:
            if hasattr(i, 'id'):
                if i.id == self.id:
                    perent = i
                    break
        else:
            self.kill()
        try:
            self.anim_poz += 1
            self.image = self.img[int(self.anim_poz / 2)]
            cord = [perent.cord[0] + perent.width * math.cos(perent.angle * math.pi / 180),
                    perent.cord[1] + perent.width * math.sin(-perent.angle * math.pi / 180)]
            self.cord = cord
        except Exception:
            self.kill()

    def calculation_relative_coordinates(self, position):
        self.rect.center = position[0] + self.cord[0], position[1] + self.cord[1]