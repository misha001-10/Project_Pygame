import pygame
import math
import M1_Objects
import M8_Weapons
import M6_Constants
import random


# класс плеера
class Player(M1_Objects.Object):
    def __init__(self, img, cord=[M6_Constants.W // 2, M6_Constants.H // 2], angle=0, health=1500, speed=[0, 0], angle_speed=0, max_angle_speed=4, speed_boost=0.1):
        self.id = '0201' + '.' + str(random.randint(9999999, 100000000))
        super(Player, self).__init__(img, cord, angle, health, speed, angle_speed, max_angle_speed)
        self.speed_boost = speed_boost
        self.gan = M8_Weapons.weapon_forming(self, M6_Constants.WEAPON[2])

    # апдат плеера (его движение и поворот)
    def update_player(self, position):
        keystate = pygame.key.get_pressed()
        new_angle = None
        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            x_sr = x - self.rect.centerx
            y_sr = y - self.rect.centery
            new_angle = 180 + math.atan2(x_sr, y_sr) * 180 / math.pi + 90
            if new_angle < 0:
                new_angle = 360 - new_angle
            elif new_angle > 360:
                # print(self.angle)
                new_angle = 0 + (new_angle - 360)
            #print(new_angle)
        if keystate[pygame.K_d]:
            new_angle = 0
        if keystate[pygame.K_a]:
            new_angle = 180
        if keystate[pygame.K_w]:
            new_angle = 90
        if keystate[pygame.K_s]:
            new_angle = 270
        if keystate[pygame.K_w] and keystate[pygame.K_d]:
            new_angle = 45
        if keystate[pygame.K_w] and keystate[pygame.K_a]:
            new_angle = 135
        if keystate[pygame.K_a] and keystate[pygame.K_s]:
            new_angle = 225
        if keystate[pygame.K_s] and keystate[pygame.K_d]:
            new_angle = 315
        if keystate[pygame.K_SPACE]:
            self.speed = [self.speed[0] + self.speed_boost * math.cos(self.angle * math.pi / 180),
                          self.speed[1] + self.speed_boost * math.sin(-self.angle * math.pi / 180)]
        self.speed = [self.speed[0] - (self.speed[0] / 150),
                      self.speed[1] - (self.speed[1] / 150)]
        if keystate[pygame.K_LSHIFT]:
            self.speed = [0, 0]
            #print(self.speed)
        if not (new_angle is None):
            if abs(self.angle - new_angle) > self.max_angle_speed:
                if abs(self.angle - new_angle) <= 180:
                    if self.angle < new_angle:
                        self.angle_speed = self.max_angle_speed
                    else:
                        self.angle_speed = -self.max_angle_speed
                elif abs(self.angle - new_angle) > 180:
                    if self.angle > new_angle:
                        self.angle_speed = self.max_angle_speed
                    else:
                        self.angle_speed = -self.max_angle_speed
            else:
                self.angle_speed = 0
                self.angle = new_angle
        else:
            pass

        if self.health <= 0:
            self.kill()
        self.angle += self.angle_speed
        if self.angle < 0:
            self.angle = 360 - self.angle
        elif self.angle > 360:
            self.angle = 0 + (self.angle - 360)
        self.image = pygame.transform.rotate(self.img, self.angle)
        self.image.set_colorkey((255, 255, 255))
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.cord[0] += self.speed[0]
        self.cord[1] += self.speed[1]
        position[0] -= self.speed[0]
        position[1] -= self.speed[1]
        #self.rect.center = [M6_Constants.W // 2, M6_Constants.H // 2]
        #print(self.rect.center)
        return position

    def update(self, *args, **kwargs) -> None:
        pass

    def action(self, *args, **kwargs):
        return self.gan.shooting()