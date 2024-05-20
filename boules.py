import pygame
import pymunk
import math
def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 600

class Boules:
    instances = []

    def __init__(self, fenetre, centre, rayon, masse, type_, sprite, espace):
        self.fenetre = fenetre
        self.rayon = rayon
        self.masse = masse
        self.type = type_
        self.sprite = sprite
        self.espace = espace
        self.centre = centre
        self.window_size = (1200, 700)
        moment = pymunk.moment_for_circle(self.masse, 0, self.rayon)
        self.centre_masque = pymunk.Body(self.masse, moment)
        self.centre_masque.friction = 0.5
        Boules.instances.append(self)
        self.alpha_all = 0


        # Charger le sprite si c'est un chemin d'image
        if isinstance(self.sprite, str):
            self.image = pygame.image.load(self.sprite)
            self.image = pygame.transform.scale(self.image, (2 * self.rayon, 2 * self.rayon))
        else:
            self.image = None


    def gravite(self):
        self.centre_masque.position = self.centre


        ball_shape = pymunk.Circle(self.centre_masque, self.rayon)
        ball_shape.ball = self
        ball_shape.collision_type = self.type
        self.espace.add(self.centre_masque, ball_shape)



    def dessin(self, body1):
        vitesse = self.centre_masque.velocity.x * 200
        vitesse_angulaire = vitesse / self.rayon
        alpha = vitesse_angulaire * (1/60)
        self.alpha_all = self.alpha_all + alpha
        ball_pos = int(self.centre_masque.position.x), self.window_size[1] - int(self.centre_masque.position.y)
        #self.angle = self.centre_masque.angle
        #angle = body.angle
        angle_degrees = math.degrees(body1.angle)
        print(f"Angle de rotation: {angle_degrees:.2f} degrés")
        if self.image:
            print(f"{vitesse}")
            print(f"{vitesse_angulaire}")
            print(f"{alpha}")
            rotated_image = pygame.transform.rotate(self.image, self.alpha_all)
            rect = rotated_image.get_rect(center=ball_pos)
            self.fenetre.blit(rotated_image, rect.topleft)



        else:
            print(f"{vitesse}")
            print(f"{vitesse_angulaire}")
            print(f"{alpha}")
            pygame.draw.circle(self.fenetre, self.sprite, ball_pos, self.rayon)


    def trouver_par_position(cls, x, y):
        for instance in cls.instances:
            if instance.x == x and instance.y == y:
                return instance
        return None

    def dessin_preview(self):
        '''pygame.draw.circle(self.fenetre, self.sprite, self.centre, self.rayon)'''
        ball_pos = self.centre

        if self.image:
            rect = self.image.get_rect(center=ball_pos)
            self.fenetre.blit(self.image, rect)
        else:
            pygame.draw.circle(self.fenetre, self.sprite, ball_pos, self.rayon)



class Boule1(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 15, 15, 5, (0, 255, 0), space)

class Boule2(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 25, 25, 6, (255, 0, 0), space)

class Boule3(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 35, 35, 7, (0, 0, 255), space)

class Boule4(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 45, 45, 8, (255, 255, 0), space)

class Boule5(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 55, 55, 9, (0, 255, 255), space)

class Boule6(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 65, 65, 10, (255, 0, 255), space)

class Boule7(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 75, 75, 11, (130, 255, 130), space)

class Boule8(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 85, 85, 12, (130, 130, 255), space)

class Boule9(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 95, 95, 13, (130, 130, 130), space)

class Boule10(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 105, 105, 14, (156, 130, 20), space)

class Boule11(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 115, 115, 15, "sun.png", space)