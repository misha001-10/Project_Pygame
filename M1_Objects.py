import pygame
import math
import random


class Object(pygame.sprite.Sprite):
    def __init__(self, img: pygame.Surface, cord, angle=0, health=1500, speed=[0, 0], angle_speed=0,
                 max_angle_speed=0):
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.angle = angle
        self.speed = speed
        self.angle_speed = angle_speed
        self.cord = cord
        self.max_angle_speed = max_angle_speed
        self.type = 0
        #print(self.img)
        self.width, self.height = self.img.get_width(), self.img.get_height()
        self.image = pygame.transform.rotate(self.img, self.angle)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.cord
        self.health = health

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
    def __init__(self, id, cord, end_cord):
        super(Bullet_Line, self).__init__()
        self.cord = cord.copy()
        self.end_cord = end_cord.copy()
        self.rect_cord = cord.copy()
        self.end_rect_cord = self.end_cord.copy()
        self.color = (255, 255, 255)
        self.color_end = self.color
        self.life = 0

    def update(self):
        self.life += 1
        if self.life == 25:
            self.kill()
        self.color_end = self.color[0] - 10 * self.life, self.color[1] - 10 * self.life, self.color[2] - 10 * self.life

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


class Cursor(pygame.sprite.Sprite):
    def __init__(self, img):
        super(Cursor, self).__init__()
        self.type = 'cursor'
        self.img = img
        self.image = self.img[0]
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.button_event = [0, 0, 0]

    def update(self):
        if pygame.mouse.get_focused():
            self.rect.center = pygame.mouse.get_pos()
            if self.button_event != pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[0]:
                    self.image = self.img[1]
                    self.image.set_colorkey((255, 255, 255))
                else:
                    self.image = self.img[0]
                    self.image.set_colorkey((255, 255, 255))
            self.button_event = pygame.mouse.get_pressed()
        else:
            self.rect.center = (-20, -20)
