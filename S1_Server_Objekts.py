import M1_Objects
import pygame
import random


class Server_colide_objekt(pygame.sprite.Sprite):
    def __init__(self, id, rect):
        super(Server_colide_objekt, self).__init__()
        self.id = id
        self.updating = 0
        self.receiving(rect)

    def receiving(self, rect):
        self.cord = [rect[0], rect[1]]
        self.rects = [rect[2], rect[3]]


class Server_Objekt(Server_colide_objekt):
    def __init__(self, rect, angle=0, speed=[0, 0], angle_speed=random.randint(-2, 2), max_angle_speed=0, health=1500):
        id = '0101' + '.' + str(random.randint(9999999, 100000000))
        super(Server_Objekt, self).__init__(id, rect)
        self.updating = 1
        self.angle = angle
        self.speed = speed
        self.angle_speed = angle_speed
        self.max_angle_speed = max_angle_speed
        self.type = 0
        self.health = health

    def update(self):
        if self.health <= 0:
            self.kill()
        self.angle += self.angle_speed
        if self.angle < 0:
            self.angle = 360 - self.angle
        elif self.angle > 360:
            self.angle = 0 + (self.angle - 360)
        self.cord[0] += self.speed[0]
        self.cord[1] += self.speed[1]