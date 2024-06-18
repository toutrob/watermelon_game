import pygame
import pymunk
class Boules:
    instances = [] # création d'un liste dans laquelle in mettra toutes les boules

    def __init__(self, window, center, radius, weight, type_, sprite, space, speed_coefficient):
        self.window = window #le fenetre pygame sur laquel les boules vont etre dessinées
        self.radius = radius # le rayon que les boules bont avoir
        self.weight = weight #la masse que les boules vont avoir
        self.type = type_   #le type de la boule, augmentant en fonction de sa taille
        self.sprite = sprite    #l'image que sera la boule
        self.space = space      #l'espace physique dans lequel les objets vont être placés
        self.center = center    #Le centre de la boule
        self.actual_center = None #sert dans une fonction pour return un centre
        self.window_size = (1200, 700)  #defini la taille de la fenetre dan laquelle la boule évolue
        moment = pymunk.moment_for_circle(self.weight, 0, self.radius) #l'accélération de la boule
        self.center_masque = pymunk.Body(self.weight, moment) #création d'un corps physique via pymunk
        self.center_masque.friction = 0.5 # définition de conefficient de frottement de cette boule
        Boules.instances.append(self) # on place la boule dans la liste des boules a sa création
        self.alpha_all = 0 #définition de l'angle dans lequel sera tourné le sprite de la boule
        self.speed_coefficient = speed_coefficient #définition d'un coefficient permettant de rendre naturel
        #la rotation du sprite de la boule
        self.ball_shape = None

        # Charger le sprite si c'est un chemin d'image
        if isinstance(self.sprite, str):
            #charger les sprites dans une variables image
            self.image = pygame.image.load(self.sprite)
            self.image = pygame.transform.scale(self.image, (2 * self.radius, 2 * self.radius))
        else:
            self.image = None


    #fonction liant le corps physique pymunk et le plaçant sur une forme circulaire
    def gravity(self):
        self.center_masque.position = self.center
        #création d'un corps centré sur le centre de l'OBJET Boule


        ball_shape = pymunk.Circle(self.center_masque, self.radius)
        #le corps physique debient un cercle
        ball_shape.ball = self
        ball_shape.collision_type = self.type
        self.space.add(self.center_masque, ball_shape)
        #ajout dans l'espace physique
        self.ball_shape = ball_shape


    #fonctions de dessin des boules
    def draw(self, body1):
        #calcul de la vitesse de la boule * coeff afin d'avoir une vitesse suffisamment grande
        velocity = self.center_masque.velocity.x * self.speed_coefficient
        #utilisation physique de la formule de la vitesse angulaire
        angular_velocity = velocity / self.radius
        #calcul de l'angle en utilisant la definition physique de la vitesse angulaire
        alpha = angular_velocity * (1/60)
        #calcul de la nouvelle rotation du sprite
        self.alpha_all = self.alpha_all + alpha
        #calucl de la position de la boule en pymunk
        ball_pos = int(self.center_masque.position.x), self.window_size[1] - int(self.center_masque.position.y)

        #definition d'un rectangle que l'on pourra cliquer
        #utile pour le super pouvoir de destruction de boule
        clickable_rect = None
        if self.image:
            #si on a bien une image de définie
            #on tourne cette image de l'angle defini plus tôt et on renvoie cette image
            rotated_image = pygame.transform.rotate(self.image, - self.alpha_all)
            rect = rotated_image.get_rect(center=ball_pos)
            self.window.blit(rotated_image, rect.topleft)

            #on attribut au rectangle clickable defini plus tot une dimension suffisamment petite
            #pour que celui ci soit contenu dans la boule et qu'il ne dépasse pas
            clickable_rect = pygame.Rect(ball_pos[0] - (self.radius/2) - (self.radius/6), ball_pos[1] - (self.radius/2) - (self.radius/6), (self.radius +round(1/3 * (self.radius))), (self.radius + round(1/3 * (self.radius))))



        else:
            pygame.draw.circle(self.window, self.sprite, ball_pos, self.radius)

        #on renvoie le rectangle clickable que l'on utilise dans la fonction de suppression d'une boule
        return clickable_rect



    def draw_preview(self):
        ball_pos = self.center

        if self.image:
            rect = self.image.get_rect(center=ball_pos)
            self.window.blit(self.image, rect)
        else:
            pygame.draw.circle(self.window, self.sprite, ball_pos, self.radius)


    #fonction utilisée dans la fonction gérant les collisions
    #permet d'obtenir le centre d'un corps physique
    def find_center(self):
        self.actual_center = self.center_masque.position
        return self.actual_center



#création des différentes boules avec des classes filles dont certains paramètres sont prédéfinies

class Boule1(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 20, 20, 5, "eris.png", space, 100)

class Boule2(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 25, 25, 6, "pluto 2.5.png", space, 110)

class Boule3(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 35, 35, 7, "mercury 2.png", space, 120)

class Boule4(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 50, 50, 8, "mars.png", space, 130)

class Boule5(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 60, 60, 9, "venus.png", space, 140)

class Boule6(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 70, 70, 10, "earth.png", space, 150)

class Boule7(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 80, 80, 11, "neptune.png", space, 160)

class Boule8(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 90, 90, 12, "uranus.png", space, 170)

class Boule9(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 100, 100, 13, "saturne.png", space, 180)

class Boule10(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 110, 110, 14, "jupiter.png", space, 190)

class Boule11(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 120, 120, 15, "sun.png", space, 200)