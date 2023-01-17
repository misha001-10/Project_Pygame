import pygame
import M4_Functions


class Server_Object_Group(pygame.sprite.Group):
    def collide(self):
        for sprite_namber in range(len(self.sprites())):
            for sprite_namber1 in range(sprite_namber + 1, len(self.sprites())):
                sprite, sprite1 = self.sprites()[sprite_namber], self.sprites()[sprite_namber1]
                hits = sprite.rect.colliderect(sprite1)
                if hits:
                    sprite.kill()
                    sprite1.kill()


class Server_Line_Bullet_Group(pygame.sprite.Group):
    def collide_objekts(self, group):
        for i in self.sprites():
            try:
                if not i.life:
                    i.life = 1
                    purpose = False
                    for j in group.sprites():
                        pass
                        if i.parent != j.id:
                            points = M4_Functions.collide_line_rect(i, j)
                            if any(points):
                                len_line_point = {points[0]: False,
                                                  points[1]: False,
                                                  points[2]: False,
                                                  points[3]: False}
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
                                print('1\n\n111\n\n1')
                                i.end_cord = min([i for i in len_line_point.keys() if i], key=lambda x: len_line_point[x])
                                purpose = j
                    if purpose:
                        purpose.health -= i.damage
                        i.strike = '1'
                        i.id += '..' + purpose.id
            except Exception:
                pass

    def str_transformation(self):
        preparation_list = []
        for i in self.sprites():
            if i.life:
                preparation_list += [i.id + ':' + i.strike + ':' + '..'.join([str(j) for j in i.cord]) + ':' + '..'.join([str(j) for j in i.end_cord])]
        return ';'.join(preparation_list)