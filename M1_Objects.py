import pygame
import math
import random


class Object(pygame.sprite.Sprite):
    def __init__(self, type, img: pygame.Surface, cord, angle=0, health=1500, weight=10, speed=[0, 0], angle_speed=-1,
                 max_angle_speed=0):
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.angle = angle
        self.speed = speed
        self.angle_speed = angle_speed
        self.cord = cord
        self.max_angle_speed = max_angle_speed
        self.type = type
        print(self.img)
        self.width, self.height = self.img.get_width(), self.img.get_height()
        self.image = pygame.transform.rotate(self.img, self.angle)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.cord
        self.health = health
        self.weight = weight

    def update(self) -> None:
        if self.health <= 0:
            self.kill()
        self.angle += self.angle_speed
        if self.angle < 0:
            self.angle = 360 - self.angle
        elif self.angle > 360:
            # print(self.angle)
            self.angle = 0 + (self.angle - 360)
        # print(self.angle)
        self.image = pygame.transform.rotate(self.img, self.angle)
        self.image.set_colorkey((255, 255, 255))
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.cord[0] += self.speed[0]
        self.cord[1] += self.speed[1]

    def calculation_relative_coordinates(self, position):
        self.rect.center = position[0] + self.cord[0], position[1] + self.cord[1]

    def action(self, *args, **kwargs) -> None:
        pass


class Bullet_Line(pygame.sprite.Sprite):
    def __init__(self, position, cord, angle, parent):
        super(Bullet_Line, self).__init__()
        self.cord = cord.copy()
        self.cord = random.randint(int(self.cord[0]) - 5, int(self.cord[0]) + 5), random.randint(int(self.cord[1]) - 5,
                                                                                                 int(self.cord[1]) + 5)
        self.angle = random.randint(angle - 10, angle + 10)
        self.end_cord = [self.cord[0] + 700 * math.cos(self.angle * math.pi / 180),
                         self.cord[1] + 700 * math.sin(-self.angle * math.pi / 180)]
        self.rect_cord = cord.copy()
        self.end_rect_cord = self.end_cord.copy()
        self.parent = parent
        self.color = (255, 255, 255)
        self.color_end = self.color
        self.life = 0

    def update(self):
        self.life += 1
        if self.life == 8:
            self.kill()
        self.color_end = self.color[0] - 28 * self.life, self.color[1] - 28 * self.life, self.color[2] - 28 * self.life

    def calculation_relative_coordinates(self, position):
        self.rect_cord = self.cord[0] + position[0], self.cord[1] + position[1]
        self.end_rect_cord = self.end_cord[0] + position[0], self.end_cord[1] + position[1]

    def draw(self, surface: pygame.Surface):
        pygame.draw.aaline(surface, self.color_end,
                           self.rect_cord,
                           self.end_rect_cord)

        #k1 = ((self.end_cord[1] - self.cord[1]) / (
        #        self.end_cord[0] - self.cord[0])) if self.end_cord[0] != self.cord[0] else 1000000000
        #b1 = self.cord[1] - (k1 * self.cord[0])
#
        #k2 = 0
        #b2 = 200
        ## print(k1, b1 ,k2, b2)
#
        #x = ((b2 - b1) / (k1 - k2)) if k1 != k2 else False
        #if x:
        #    y = k2 * x + b2
        #    pygame.draw.circle(surface, (255, 255, 255), (x, y), 5)


class Animation(pygame.sprite.Sprite):
    def __init__(self, cord):
        super(Animation, self).__init__()
        self.cord = cord
        self.rect_cord = cord

    def update(self, position):
        self.rect_cord = self.cord[0] + position[0], self.cord[1] + position[1]

    def draw(self, surface):
        #print(self.rect_cord)
        pygame.draw.circle(surface, (255, 255, 255), self.rect_cord, 5)