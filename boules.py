import random
import pygame
import pymunk


class Boules :
    def __init__(self,fenetre, centre, rayon, masse, type_, sprite, espace):
        self.fenetre = fenetre
        self.rayon = rayon
        self.masse = masse
        self.type = type_
        self.sprite = sprite
        self.espace = espace
        self.centre = centre
        self.window_size = (1200, 700)
        self.centre_masque = pymunk.Body(self.masse, 100)
        self.centre_masque.friction = 0.2

    def gravite(self):
        '''centremasque = pymunk.Body(self.masse, 100)'''
        self.centre_masque.position = self.centre

        ball_shape = pymunk.Circle(self.centre_masque, self.rayon)
        ball_shape.ball = self
        ball_shape.collision_type = self.type
        self.espace.add(self.centre_masque, ball_shape)



    def dessin(self):
        ball_pos = int(self.centre_masque.position.x), self.window_size[1] - int(self.centre_masque.position.y)
        pygame.draw.circle(self.fenetre, self.sprite, ball_pos, self.rayon)

    def trouver_par_position(cls, x, y):
        for instance in cls.instances:
            if instance.x == x and instance.y == y:
                return instance
        return None

    def dessin_preview(self):
        pygame.draw.circle(self.fenetre, self.sprite, self.centre, self.rayon)


class Boule1(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 10, 10, 5 , (0,255,0) , space)

class Boule2(Boules):
    def __init__(self,fenetre, centre, space):
        super().__init__(fenetre, centre, 20, 20, 6 , (255,0,0), space )

class Boule3(Boules):
    def __init__(self,fenetre, centre, space):
        super().__init__(fenetre, centre, 35, 35, 7, (0,0,255), space)

class Boule4(Boules):
    def __init__(self,fenetre, centre, space):
        super().__init__(fenetre, centre, 45, 45, 8, (255,255,0), space)

class Boule5(Boules):
    def __init__(self,fenetre, centre, space):
        super().__init__(fenetre, centre, 55, 55, 9, (0,255,255) ,space)

class Boule6(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 65, 65, 10, (255,0,255), space)

class Boule7(Boules):
    def __init__(self,fenetre, centre, space):
        super().__init__(fenetre, centre, 75, 75, 11, (130,255,130), space)

class Boule8(Boules):
    def __init__(self,fenetre, centre, space):
        super().__init__(fenetre, centre, 85, 85, 12, (130,130,255), space)