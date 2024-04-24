import random

import pygame
import pymunk


class boules :
    def __init__(self,fenetre, centre, rayon, masse, type, sprite, espace):
        self.fenetre = fenetre
        self.rayon = rayon
        self.masse = masse
        self.type = type
        self.sprite = sprite
        self.espace = espace
        self.centre = centre
        self.window_size = (1200, 700)
        self.centremasque = pymunk.Body(1, 100)

    def gravite(self):
        '''centremasque = pymunk.Body(self.masse, 100)'''
        self.centremasque.position = self.centre

        ball_shape = pymunk.Circle(self.centremasque, self.rayon)
        ball_shape.ball = self
        ball_shape.collision_type = self.type
        self.espace.add(self.centremasque, ball_shape)



    def dessin(self):
        ball_pos = int(self.centremasque.position.x), self.window_size[1] - int(self.centremasque.position.y)
        pygame.draw.circle(self.fenetre, self.sprite, ball_pos, self.rayon)

    def trouver_par_position(cls, x, y):
        for instance in cls.instances:
            if instance.x == x and instance.y == y:
                return instance
        return None

    def dessin_preview(self):
        pygame.draw.circle(self.fenetre, self.sprite, self.centre, self.rayon)


class boule1(boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 10, 100, 5 , (0,255,0) , space)

class boule2(boules):
    def __init__(self,fenetre, centre, space):
        super().__init__(fenetre, centre, 20, 200, 6 , (255,0,0), space )

class boule3(boules):
    def __init__(self,fenetre, centre, space):
        super().__init__(fenetre, centre, 35, 350, 7, (0,0,255), space)

class boule4(boules):
    def __init__(self,fenetre, centre, space):
        super().__init__(fenetre, centre, 45, 400, 8, (255,255,0), space)

class boule5(boules):
    def __init__(self,fenetre, centre, space):
        super().__init__(fenetre, centre, 55, 450, 9, (0,255,255) ,space)

class boule6(boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 65, 500, 10, (255,0,255), space)

class boule7(boules):
    def __init__(self,fenetre, centre, space):
        super().__init__(fenetre, centre, 75, 550, 11, (130,255,130), space)

class boule8(boules):
    def __init__(self,fenetre, centre, space):
        super().__init__(fenetre, centre, 85, 600, 12, (130,130,255), space)