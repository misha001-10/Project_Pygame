import pygame
import math
import M1_Objects
import random


class Player(M1_Objects.Object):
    def __init__(self, img, cord=[720, 480], angle=0, health=1500, weight=10, speed=[0, 0], angle_speed=0, max_angle_speed=4, speed_boost=0.1):
        self.id = '002' + '.' + str(random.randint(9999999, 100000000))
        super(Player, self).__init__(img, cord, angle, health, weight, speed, angle_speed, max_angle_speed)
        self.speed_boost = speed_boost
        self.gan = Line_Bullet_Gan_Gatling(self, [50, 60, 600, 5], 15, 700, [3, 6])

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
        self.rect.center = [720, 480]
        return position

    def update(self, *args, **kwargs) -> None:
        pass

    def action(self, *args, **kwargs):
        return self.gan.shooting()


class Line_Bullet_Gan_Standard:
    def __init__(self, parent, damage, radius_of_defeat, accuracy):
        self.parent = parent
        self.damage = damage
        self.range = radius_of_defeat
        self.accuracy = accuracy

    def shooting(self):
        if pygame.mouse.get_pressed()[0]:
            return M1_Objects.Bullet_Line(self.parent.cord, self.parent.angle, self.parent, self.accuracy, self.range, self.damage)


class Line_Bullet_Gan_Automat(Line_Bullet_Gan_Standard):
    def __init__(self, parent, rate_of_fire, queue, recharge_time, damage, radius_of_defeat, accuracy):
        super(Line_Bullet_Gan_Automat, self).__init__(parent, damage, radius_of_defeat, accuracy)
        self.rate_of_fire = rate_of_fire
        self.queue = queue
        self.recharge_time = recharge_time
        self.time = 0
        self.queue_now = [0, 0]

    def shooting(self):
        print(pygame.time.get_ticks() - self.queue_now[1])
        if self.queue_now[0] >= self.queue[0]:
            if pygame.time.get_ticks() - self.queue_now[1] > self.queue[1]:
                self.queue_now[0] = 0
            return None
        self.queue_now[1] = pygame.time.get_ticks()
        if not self.queue or self.queue_now[0] < self.queue[0]:
            if pygame.mouse.get_pressed()[0]:
                if pygame.time.get_ticks() - self.time >= self.rate_of_fire:
                    self.time = pygame.time.get_ticks()
                    self.queue_now[0] += 1
                    return M1_Objects.Bullet_Line(self.parent.cord, self.parent.angle, self.parent, self.accuracy,
                                                  self.range, self.damage)


class Line_Bullet_Gan_Gatling(Line_Bullet_Gan_Standard):
    def __init__(self, parent, rate_of_fire, damage, radius_of_defeat, accuracy):
        super(Line_Bullet_Gan_Gatling, self).__init__(parent, damage, radius_of_defeat, accuracy)
        self.rate_of_fire = rate_of_fire
        self.time = 0
        self.speed = rate_of_fire[1]

    def shooting(self):
        accuracy = self.accuracy[0] + ((self.accuracy[1] - self.accuracy[0]) * (self.speed - self.rate_of_fire[1]) / (self.rate_of_fire[2] - self.rate_of_fire[1] - self.rate_of_fire[1]))
        #print(self.accuracy[1], self.speed - self.rate_of_fire[1], self.rate_of_fire[2] - self.rate_of_fire[1] - self.rate_of_fire[1], accuracy)
        if pygame.mouse.get_pressed()[0]:
            if self.speed < self.rate_of_fire[2] - self.rate_of_fire[1]:
                self.speed += self.rate_of_fire[3]
            if self.speed >= self.rate_of_fire[0] + self.rate_of_fire[1]:
                if pygame.time.get_ticks() - self.time >= self.rate_of_fire[2] - self.speed:
                    self.time = pygame.time.get_ticks()
                    return M1_Objects.Bullet_Line(self.parent.cord, self.parent.angle, self.parent, accuracy,
                                                  self.range, self.damage)
        else:
            if self.speed > self.rate_of_fire[1]:
                self.speed -= self.rate_of_fire[3]