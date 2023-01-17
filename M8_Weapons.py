import pygame
import M4_Functions


# основной класс пушек стриляющих моментальнымми снорядами и его наследники
class Line_Bullet_Gan_Standard:
    def __init__(self, parent, id, damage, radius_of_defeat, accuracy):
        self.id = id
        self.parent = parent
        self.damage = damage
        self.range = radius_of_defeat
        self.accuracy = accuracy

    def shooting(self):
        if pygame.mouse.get_pressed()[0]:
            return self.shoot()

    def shoot(self):
        #return M1_Objects.Bullet_Line(self.parent.cord, self.parent.angle, self.parent, self.accuracy, self.range,
        #                              self.damage)
        return M4_Functions.line_bullet_shoot(self.parent, self.accuracy, self.range, self.damage)


class Line_Bullet_Gan_Autocannon(Line_Bullet_Gan_Standard):
    def __init__(self, parent, id, rate_of_fire, damage, radius_of_defeat, accuracy):
        super(Line_Bullet_Gan_Autocannon, self).__init__(parent, id, damage, radius_of_defeat, accuracy)
        self.rate_of_fire = rate_of_fire
        self.time = 0

    def shooting(self):
        if pygame.mouse.get_pressed()[0]:
            if pygame.time.get_ticks() - self.time >= self.rate_of_fire:
                self.time = pygame.time.get_ticks()
                return self.shoot()


class Line_Bullet_Gan_Automat(Line_Bullet_Gan_Standard):
    def __init__(self, parent, id, rate_of_fire, queue, damage, radius_of_defeat, accuracy):
        super(Line_Bullet_Gan_Automat, self).__init__(parent, id, damage, radius_of_defeat, accuracy)
        self.rate_of_fire = rate_of_fire
        self.queue = queue
        self.time = 0
        self.queue_now = [0, 0]

    def shooting(self):
        #print(pygame.time.get_ticks() - self.queue_now[1])
        print(self.queue)
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
                    return self.shoot()


class Line_Bullet_Gan_Gatling(Line_Bullet_Gan_Standard):
    def __init__(self, parent, id, rate_of_fire, damage, radius_of_defeat, accuracy_list):
        super(Line_Bullet_Gan_Gatling, self).__init__(parent, id, damage, radius_of_defeat, accuracy_list[0])
        self.accuracy_list = accuracy_list
        self.rate_of_fire = rate_of_fire
        self.time = 0
        self.speed = rate_of_fire[0]

    def shooting(self):
        #self.accuracy = self.accuracy_list[0] + ((self.accuracy_list[1] - self.accuracy_list[0]) * (self.speed - self.rate_of_fire[1]) / (self.rate_of_fire[2] - self.rate_of_fire[1] - self.rate_of_fire[1]))
        self.accuracy = self.accuracy_list[0] + (self.accuracy_list[1] - self.accuracy_list[0]) * (self.speed - self.rate_of_fire[0]) / (self.rate_of_fire[1] - self.rate_of_fire[0])
        self.accuracy  = int(self.accuracy)
        #print(self.accuracy[1], self.speed - self.rate_of_fire[1], self.rate_of_fire[2] - self.rate_of_fire[1] - self.rate_of_fire[1], accuracy)
        if pygame.mouse.get_pressed()[0]:
            if self.speed > self.rate_of_fire[1]:
                self.speed -= self.rate_of_fire[3]
                #print(self.speed)
            if self.speed <= self.rate_of_fire[0] - self.rate_of_fire[2]:
                if pygame.time.get_ticks() - self.time >= self.speed:
                    self.time = pygame.time.get_ticks()
                    return self.shoot()
        else:
            if self.speed < self.rate_of_fire[0]:
                self.speed += self.rate_of_fire[3]


def weapon_forming(parent, string):
    string_splited = string.split(';')
    id = string_splited[0].split('.')
    data_inf = [int(i) if not '..' in i else [int(j) for j in i.split('..')] for i in string_splited[1].split(':')]
    if id[0] == '02':
        if id[1] == '01':
            return Line_Bullet_Gan_Autocannon(parent, string_splited[0], *data_inf)
        elif id[1] == '02':
            return Line_Bullet_Gan_Automat(parent, string_splited[0], *data_inf)
        elif id[1] == '03':
            return Line_Bullet_Gan_Gatling(parent, string_splited[0], *data_inf)