import pygame
import math
import random
import M1_Objects
import M4_Functions
import M2_Player
import M6_Constants
import M7_Animations


class Large_Sprite_Group():
    def __init__(self, net):
        self.all_objects = Object_Sprite_Group(self)
        self.all_line_bullet = Line_Bullet_Group(self)
        self.list_peinted_line_bullet = {}
        self.all_animations = Animation_Group(self)
        self.all_cursors = Cursor_Group(self)
        self.cursor = M1_Objects.Cursor(M6_Constants.IMG['c_img'])
        self.add(self.cursor)
        self.new_line_bullets = []
        self.life = True
        self.new_player()
        self.net = net
        self.backgrounds = [M1_Objects.Background(i, j) for i, j in zip(M6_Constants.BACKGROUND, ((0, 0), (1920, 0), (0, 1080), (1920, 1080)))]

    def new_player(self):
        self.position = [0, 0]
        self.respawn_flag = False
        self.player = M2_Player.player_forming([M6_Constants.W // 2, M6_Constants.H // 2])
        self.add(self.player)
        self.life = True

    def respawn(self):
        if not self.player:
            self.respawn_flag = True

    def add(self, sprite):
        if hasattr(sprite, 'type'):
            if sprite.type == 0:
                self.all_objects.add(sprite)
            elif sprite.type == 1:
                self.all_line_bullet.add(sprite)
            elif sprite.type == 'cursor':
                self.all_cursors.add(sprite)

    def add_net(self, objekt):
        objekt_splited = objekt.split(':')
        if objekt_splited[0].split('.')[0] == '0101':
            self.all_objects.add(M1_Objects.Object(M6_Constants.IMG['astr_img'], objekt_splited[0], 15, [int(i) for i in objekt_splited[1].split('.')], angle=float(objekt_splited[2])))
        else:
            if self.player and objekt_splited[0] == self.player.id:
                return
            elif objekt:
                self.all_objects.add(M1_Objects.Object(M6_Constants.IMG['.'.join(objekt_splited[0].split('.')[:-1])], objekt_splited[0], 15, [int(i) for i in objekt_splited[1].split('.')], angle=float(objekt_splited[2])))

    def add_bullet_net(self, bullet):
        if bullet:
            bullet_splited = bullet.split(':')
            if bullet_splited[0] not in self.list_peinted_line_bullet.keys():
                self.all_line_bullet.add(M1_Objects.Bullet_Line(bullet_splited[0], [float(i) for i in bullet_splited[2].split('..')], [float(i) for i in bullet_splited[3].split('..')]))
                self.list_peinted_line_bullet[bullet_splited[0]] = pygame.time.get_ticks()

                if self.player:
                    x_sr = [float(i) for i in bullet_splited[2].split('..')][0] - self.player.cord[0]
                    y_sr = [float(i) for i in bullet_splited[2].split('..')][1] - self.player.cord[1]
                    new_angle = 180 + math.atan2(x_sr, y_sr) * 180 / math.pi + 90
                    #cos = math.cos(new_angle)
                    #sin = math.sin(-new_angle)
                    #print(new_angle, cos)
                    lenn = math.sqrt(x_sr ** 2 + y_sr ** 2)
                    #if cos > 0:
                    #    volume = (0, 1)
                    #else:
                    #    volume = (1, 0)
                    volume = (0, 0)
                    if lenn < 3000:
                        volume = 1 - lenn / 3000, 1 - lenn / 3000
                    if lenn < 80:
                        volume = (1, 1)
                    a = M6_Constants.SND[0].play()
                    if a:
                        a.set_volume(*volume)

                angle_inf = [float(i) for i in bullet_splited[2].split('..')] + [float(i) for i in bullet_splited[3].split('..')]
                #print(bullet_splited)
                self.all_animations.add(M7_Animations.Animation_angle_connection(M6_Constants.ANIMATIONS['03.02.001'], bullet_splited[0].split('..')[1], 180 + math.atan2(angle_inf[0] - angle_inf[2], angle_inf[1] - angle_inf[3]) * 180 / math.pi + 180))
                if bullet_splited[1] != '0':
                    self.all_animations.add(M7_Animations.Animation_angle(M6_Constants.ANIMATIONS['03.02.001'], [float(i) for i in bullet_splited[3].split('..')], math.atan2(angle_inf[0] - angle_inf[2], angle_inf[1] - angle_inf[3]) * 180 / math.pi + 180))
                    self.cursor.hit = 0

    def forming_player_inf(self):
        if self.player:
            return self.player.id + ':' + '.'.join([str(int(i)) for i in self.player.cord] + [str(self.player.width), str(self.player.height)]) + ':' + str(self.player.angle)
        else:
            if not self.respawn_flag:
                return 'False'
            else:
                return 'True'

    def update(self, *args, **kwargs):
        #try:
        res = self.net.send(self.net.id + ';;' + self.forming_player_inf() + ';;' + ';'.join(self.new_line_bullets))
        self.new_line_bullets = []
        row_splited = res.split(';;')
        self.all_objects.empty()
        self.life = eval(row_splited[0])
        if row_splited[-1]:
            print(row_splited)
        if self.life and not self.player:
            self.new_player()
        if not self.life:
            self.player = None
        for i in row_splited[1].split(';'):
            self.add_net(i)
        for i in row_splited[2].split(';'):
            self.add_bullet_net(i)
        for i in row_splited[3].split(';'):
            if i:
                self.all_animations.add(M7_Animations.Animation_angle(M6_Constants.ANIMATIONS['03.02.002'], [int(j) for j in i.split(':')[1].split('..')], random.randint(0, 360)))
        now_list_peinted_line_bullet = {}
        for i in self.list_peinted_line_bullet.items():
            if i[1] + 200 > pygame.time.get_ticks():
                now_list_peinted_line_bullet[i[0]] = i[1]
        self.list_peinted_line_bullet = now_list_peinted_line_bullet
        if self.player:
            self.add(self.player)
            self.position = self.player.update_player(self.position)
        self.all_line_bullet.update(*args, **kwargs)
        self.all_cursors.update(*args, **kwargs)
        self.all_animations.update(self.all_objects)
        #except Exception as a:
        #    print(a)
        #    print('xaxaxa')

    def calculation_relative_coordinates(self):
        self.all_objects.calculation_relative_coordinates(self.position)
        self.all_line_bullet.calculation_relative_coordinates(self.position)
        self.all_animations.calculation_relative_coordinates(self.position)
        #M6_Constants.BACKGROUND_RECT[0].center = self.position[0] + 0, self.position[1] + 0
        #M6_Constants.BACKGROUND_RECT[1].center = self.position[0] + 1920, self.position[1] + 0
        #M6_Constants.BACKGROUND_RECT[2].center = self.position[0] + 0, self.position[1] + 1080
        #M6_Constants.BACKGROUND_RECT[3].center = self.position[0] + 1920, self.position[1] + 1080
        for i in self.backgrounds:
            i.calculation_relative_coordinates(self.position)

    def action(self, *args, **kwargs):
        if self.player:
            act = self.player.action(*args, **kwargs)
            if act:
                self.new_line_bullets += [act]

    def draw(self, screen):
        for i in self.backgrounds:
            screen.blit(i.image, i.rect)
        self.all_objects.draw(screen)
        self.all_line_bullet.draw(screen)
        self.all_animations.draw(screen)
        self.all_cursors.draw(screen)


class Start_Sprite_Group():
    def __init__(self):
        self.all_cursors = Cursor_Group(self)
        self.all_buttons = pygame.sprite.Group()
        self.cursor = M1_Objects.Cursor(M6_Constants.IMG['c_img'])
        self.all_cursors.add(self.cursor)

    def add(self, sprite):
        if type(sprite) == M1_Objects.Button:
            self.all_buttons.add(sprite)

    def update(self, *args, **kwargs):
        for i in self.all_buttons:
            i.update_navedenie(0)
            if pygame.sprite.collide_mask(i, self.cursor):
                i.update_navedenie(1)
        self.all_cursors.update(*args, **kwargs)

    def draw(self, screen):
        self.all_buttons.draw(screen)
        self.all_cursors.draw(screen)


class Object_Sprite_Group(pygame.sprite.Group):
    def __init__(self, parent):
        super(Object_Sprite_Group, self).__init__()
        self.parent = parent

    def collide(self):
        for sprite_namber in range(len(self.sprites())):
            for sprite_namber1 in range(sprite_namber + 1, len(self.sprites())):
                sprite, sprite1 = self.sprites()[sprite_namber], self.sprites()[sprite_namber1]
                hits = pygame.sprite.collide_mask(sprite, sprite1)
                if hits:
                    sprite.kill()
                    sprite1.kill()
                    return False

    def action(self, *args, **kwargs):
        for sprite in self.sprites():
            new_sprits = sprite.action(*args, **kwargs)
            if new_sprits:
                self.parent.add(new_sprits)

    def calculation_relative_coordinates(self, *args, **kwargs):
        for sprite in self.sprites():
            sprite.calculation_relative_coordinates(*args, **kwargs)


class Line_Bullet_Group(pygame.sprite.Group):
    def __init__(self, parent):
        super(Line_Bullet_Group, self).__init__()
        self.parent = parent

    def draw(self, surface: pygame.Surface) -> None:
        for i in self.sprites():
            i.draw(surface)

    def collide_objekts(self, group):
        for i in self.sprites():
            if not i.life:
                purpose = False
                for j in group.sprites():
                    pass
                    if i.parent != j:
                        points = M4_Functions.collide_line_rect(i, j)
                        if any(points):
                            #i.kill()
                            len_line_point = {points[0]: False,
                                              points[1]: False,
                                              points[2]: False,
                                              points[3]: False}
                            #pprint(points)
                            #pprint(len_line_point)
                            if points[0]:
                                len_line_point[points[0]] = (abs((points[0][0] - i.cord[0])) ** 2 + abs(
                                    (points[0][1] - i.cord[1])) ** 2) ** 0.5
                            if points[1]:
                                len_line_point[points[1]] = (abs((points[1][0] - i.cord[0])) ** 2 + abs(
                                    (points[1][1] - i.cord[1])) ** 2) ** 0.5
                            if points[2]:
                                len_line_point[points[2]] = (abs((points[2][0] - i.cord[0])) ** 2 + abs(
                                    (points[2][1] - i.cord[1])) ** 2) ** 0.5
                            if points[3]:
                                len_line_point[points[3]] = (abs((points[3][0] - i.cord[0])) ** 2 + abs(
                                    (points[3][1] - i.cord[1])) ** 2) ** 0.5
                            i.end_cord = min([i for i in len_line_point.keys() if i], key=lambda x: len_line_point[x])
                            purpose = j
                if purpose:
                    purpose.health -= i.damage
                            #print(i.end_cord)
                            #if points[0]:
                            #    self.parent.all_animations.add(M1_Objects.Animation(points[0]))
                            #if points[1]:
                            #    self.parent.all_animations.add(M1_Objects.Animation(points[1]))
                            #if points[2]:
                            #    # print(points[2])
                            #    self.parent.all_animations.add(M1_Objects.Animation(points[2]))
                            #if points[3]:
                            #    self.parent.all_animations.add(M1_Objects.Animation(points[3]))

    def calculation_relative_coordinates(self, *args, **kwargs):
        for sprite in self.sprites():
            sprite.calculation_relative_coordinates(*args, **kwargs)


class Animation_Group(pygame.sprite.Group):
    def __init__(self, parent):
        super(Animation_Group, self).__init__()
        self.parent = parent

    def calculation_relative_coordinates(self, *args, **kwargs):
        for sprite in self.sprites():
            sprite.calculation_relative_coordinates(*args, **kwargs)


class Cursor_Group(pygame.sprite.Group):
    def __init__(self, parent):
        super(Cursor_Group, self).__init__()
        self.parent = parent