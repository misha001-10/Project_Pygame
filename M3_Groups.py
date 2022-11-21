import pygame


class Large_Sprite_Group():
    def __init__(self):
        self.all_objects = Object_Sprite_Group(self)
        self.all_line_bullet = Line_Bullet_Group(self)

    def add(self, sprite):
        if sprite.type == 0:
            self.all_objects.add(sprite)
        elif sprite.type == 1:
            self.all_line_bullet.add(sprite)

    def update(self, *args, **kwargs):
        self.all_objects.update(*args, **kwargs)
        self.all_line_bullet.update(*args, **kwargs)

    def action(self, *args, **kwargs):
        self.all_objects.action(*args, **kwargs)

    def collide(self):
        self.all_objects.collide()

    def draw(self, screen):
        self.all_objects.draw(screen)
        self.all_line_bullet.draw(screen)


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

    def action(self, *args, **kwargs):
        for sprite in self.sprites():
            new_sprits = sprite.action(*args, **kwargs)
            if new_sprits:
                self.parent.all_line_bullet.add(new_sprits)


class Line_Bullet_Group(pygame.sprite.Group):
    def __init__(self, parent):
        super(Line_Bullet_Group, self).__init__()
        self.parent = parent

    def draw(self, surface: pygame.Surface) -> None:
        for i in self.sprites():
            i.draw(surface)
