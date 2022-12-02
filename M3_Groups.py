import pygame
import M1_Objects
import M4_Functions
import M2_Player
import M6_Constants
from M5_Network import Network
from pprint import pprint


class Large_Sprite_Group():
    def __init__(self, p_img):
        self.all_objects = Object_Sprite_Group(self)
        self.all_line_bullet = Line_Bullet_Group(self)
        #self.all_animations = Animation_Group(self)
        self.all_cursors = Cursor_Group(self)
        self.player = M2_Player.Player(p_img)
        self.add(self.player)
        self.net = Network()

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
        if objekt_splited[0].split('.')[0] == '002':
            if objekt_splited[0].split('.')[1] == self.player.id:
                return
        elif objekt_splited[0].split('.')[0] == '001':
            self.all_objects.add(M1_Objects.Object(M6_Constants.IMG['astr_img'], [int(i) for i in objekt_splited[1].split('.')]))
        #print([int(i) for i in objekt_splited[1].split('.')])

    def update(self, *args, **kwargs):
        #print(self.player.id)
        #print(self.net.id + ';;' + self.player.id + ':' + '.'.join([str(i) for i in self.player.cord]) + ':' + '150')
        #print(self.net.id + ';;' + self.player.id + ':' + '.'.join([str(i) for i in self.player.cord]) + ':' + '150')
        res = self.net.send(self.net.id + ';;' + self.player.id + ':' + '.'.join([str(i) for i in self.player.cord]) + ':' + '150')
        #pprint(res.split(';'))
        self.all_objects.empty()
        for i in res.split(';'):
            #print(i)
            self.add_net(i)
        self.add(self.player)
        #print(res)
        #self.all_objects.update(*args, **kwargs)
        self.all_line_bullet.update(*args, **kwargs)
        #self.all_animations.update(*args, **kwargs)
        self.all_cursors.update(*args, **kwargs)

    def calculation_relative_coordinates(self, *args, **kwargs):
        self.all_objects.calculation_relative_coordinates(*args, **kwargs)
        self.all_line_bullet.calculation_relative_coordinates(*args, **kwargs)

    def action(self, *args, **kwargs):
        self.add(self.player.action(*args, **kwargs))

    def collide(self):
        self.all_objects.collide()
        self.all_line_bullet.collide_objekts(self.all_objects)

    def draw(self, screen):
        self.all_objects.draw(screen)
        self.all_line_bullet.draw(screen)
        #self.all_animations.draw(screen)
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

    def draw(self, surface: pygame.Surface) -> None:
        for i in self.sprites():
            i.draw(surface)


class Cursor_Group(pygame.sprite.Group):
    def __init__(self, parent):
        super(Cursor_Group, self).__init__()
        self.parent = parent