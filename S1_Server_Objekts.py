import pygame
import random
import math


class Server_colide_objekt(pygame.sprite.Sprite):
    def __init__(self, id, rect, angle):
        super(Server_colide_objekt, self).__init__()
        self.id = id
        self.updating = 0
        self.receiving(rect, angle)
        self.health = 150

    def receiving(self, rect, angle):
        self.rect = pygame.Rect(int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3]))
        self.cord = [int(rect[0]), int(rect[1])]
        self.rects = [int(rect[2]), int(rect[3])]
        self.width = self.rects[0]
        self.height = self.rects[1]
        self.angle = angle


class Server_Objekt(Server_colide_objekt):
    def __init__(self, rect, angle=0, speed=[0, 0], angle_speed=random.randint(-2, 2), max_angle_speed=0, health=1500):
        id = '0101' + '.' + str(random.randint(9999999, 100000000))
        super(Server_Objekt, self).__init__(id, rect, angle)
        self.updating = 1
        #self.angle = angle
        self.speed = speed
        self.angle_speed = angle_speed
        self.max_angle_speed = max_angle_speed
        self.type = 0
        self.health = health

    def update(self):
        if self.health <= 0:
            self.kill()
        #print(self.health, end=' ')
        self.angle += self.angle_speed
        if self.angle < 0:
            self.angle = 360 - self.angle
        elif self.angle > 360:
            self.angle = 0 + (self.angle - 360)
        self.cord[0] += self.speed[0]
        self.cord[1] += self.speed[1]


class Player(Server_colide_objekt):
    def __init__(self, id, rect, angle=0, health=1500):
        super(Player, self).__init__(id, rect, angle)
        self.health = health


class Server_line_bullet(pygame.sprite.Sprite):
    def __init__(self, id, parent, cord, angle, accuracy, radius_of_defeat, damage):
        super(Server_line_bullet, self).__init__()
        self.life = 0
        self.time = pygame.time.get_ticks()
        self.id = id
        self.type = 1
        self.cord = cord.split('.')
        self.cord = int(self.cord[0]), int(self.cord[1])
        accuracy = int(accuracy)
        radius_of_defeat = int(radius_of_defeat)
        damage = int(damage)
        self.cord = random.randint(int(self.cord[0] - accuracy), int(self.cord[0] + accuracy)), random.randint(
            int(self.cord[1]) - 5,
            int(self.cord[1]) + 5)
        angle = float(angle)
        self.angle = random.randint(int(angle - accuracy), int(angle + accuracy))
        self.end_cord = [self.cord[0] + radius_of_defeat * math.cos(self.angle * math.pi / 180),
                         self.cord[1] + radius_of_defeat * math.sin(-self.angle * math.pi / 180)]
        self.parent = parent
        self.damage = damage
        self.strike = '0'