import pygame
import M4_Functions


class Server_Line_Bullet_Group(pygame.sprite.Group):
    def collide_objekts(self, group):
        for i in self.sprites():
            try:
                if not i.life:
                    #print(i.cord, i.end_cord)
                    i.life = 1
                    purpose = False
                    for j in group.sprites():
                        pass
                        if i.parent != j.id:
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
                                print('1\n\n111\n\n1')
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
            except Exception:
                pass


    def str_transformation(self):
        preparation_list = []
        for i in self.sprites():
            if i.life:
                preparation_list += [i.id + ':' + '..'.join([str(j) for j in i.cord]) + ':' + '..'.join([str(j) for j in i.end_cord])]
        return ';'.join(preparation_list)