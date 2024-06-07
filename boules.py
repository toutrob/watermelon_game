import pygame
import pymunk
import math

class Boules:
    instances = []

    def __init__(self, fenetre, centre, rayon, masse, type_, sprite, espace, coeff_vitesse):
        self.fenetre = fenetre
        self.rayon = rayon
        self.masse = masse
        self.type = type_
        self.sprite = sprite
        self.espace = espace
        self.centre = centre
        self.centre_actuel = None
        self.window_size = (1200, 700)
        moment = pymunk.moment_for_circle(self.masse, 0, self.rayon)
        self.centre_masque = pymunk.Body(self.masse, moment)
        self.centre_masque.friction = 0.5
        Boules.instances.append(self)
        self.alpha_all = 0
        self.coeff_vitesse = coeff_vitesse


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
        vitesse = self.centre_masque.velocity.x * self.coeff_vitesse
        vitesse_angulaire = vitesse / self.rayon
        alpha = vitesse_angulaire * (1/60)
        self.alpha_all = self.alpha_all + alpha
        ball_pos = int(self.centre_masque.position.x), self.window_size[1] - int(self.centre_masque.position.y)
        #self.angle = self.centre_masque.angle
        #angle = body.angle
        angle_degrees = math.degrees(body1.angle)
        #print(f"Angle de rotation: {angle_degrees:.2f} degrés")
        if self.image:
            #print(f"{vitesse}")
            #print(f"{vitesse_angulaire}")
            #print(f"{alpha}")
            rotated_image = pygame.transform.rotate(self.image, - self.alpha_all)
            rect = rotated_image.get_rect(center=ball_pos)
            self.fenetre.blit(rotated_image, rect.topleft)



        else:
            #print(f"{vitesse}")
            #print(f"{vitesse_angulaire}")
            #print(f"{alpha}")
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


    def trouver_centre(self):
        self.centre_actuel = self.centre_masque.position
        return self.centre_actuel


class Boule1(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 20, 15, 5, "eris.png", space, 100)

class Boule2(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 25, 25, 6, "pluto 2.5.png", space, 110)

class Boule3(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 35, 35, 7, "mercury 2.png", space, 120)

class Boule4(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 50, 45, 8, "mars.png", space, 130)

class Boule5(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 60, 55, 9, "venus.png", space, 140)

class Boule6(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 70, 65, 10, "earth.png", space, 150)

class Boule7(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 80, 75, 11, "neptune.png", space, 160)

class Boule8(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 90, 85, 12, "uranus.png", space, 170)

class Boule9(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 100, 95, 13, "saturne.png", space, 180)

class Boule10(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 110, 105, 14, "jupiter.png", space, 190)

class Boule11(Boules):
    def __init__(self, fenetre, centre, space):
        super().__init__(fenetre, centre, 120, 115, 15, "sun.png", space, 200)