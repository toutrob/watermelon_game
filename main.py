import random
import pygame
import pymunk
from boules import Boules, Boule1, Boule2, Boule3, Boule4, Boule5, Boule6, Boule7, Boule8
import numpy

WINDOWSIZE = (1200, 700)
window = pygame.display.set_mode(WINDOWSIZE)
pygame.display.set_caption("Watermelon Game")

'''class boules :
    def __init__(self,fenetre, centre, rayon, masse, type, sprite):
        self.fenetre = fenetre
        self.rayon = rayon
        self.masse = masse
        self.type = type
        self.sprite = sprite
        self.centre = centre
        self.centremasque = pymunk.Body(1, 100)

    def gravite(self):
        ''''''centremasque = pymunk.Body(self.masse, 100)'''''''
        self.centremasque.position = self.centre

        ball_shape = pymunk.Circle(self.centremasque, self.rayon)
        ball_shape.ball = self
        ball_shape.collision_type = self.type
        space.add(self.centremasque, ball_shape)



    def dessin(self):
        ball_pos = int(self.centremasque.position.x), window_size[1] - int(self.centremasque.position.y)
        pygame.draw.circle(self.fenetre, self.sprite, ball_pos, self.rayon)

    def trouver_par_position(cls, x, y):
        for instance in cls.instances:
            if instance.x == x and instance.y == y:
                return instance
        return None

    def dessin_preview(self):
        pygame.draw.circle(self.fenetre, self.sprite, self.centre, self.rayon)


class boule1(boules):
    def __init__(self, centre):
        super().__init__(window, centre, 10, 100, 5 , (0,255,0) )

class boule2(boules):
    def __init__(self, centre):
        super().__init__(window, centre, 20, 200, 6 , (255,0,0) )

class boule3(boules):
    def __init__(self, centre):
        super().__init__(window, centre, 35, 350, 7, (0,0,255))

class boule4(boules):
    def __init__(self, centre):
        super().__init__(window, centre, 45, 400, 8, (255,255,0))

class boule5(boules):
    def __init__(self, centre):
        super().__init__(window, centre, 55, 450, 9, (0,255,255))

class boule6(boules):
    def __init__(self, centre):
        super().__init__(window, centre, 65, 500, 10, (255,0,255))

class boule7(boules):
    def __init__(self, centre):
        super().__init__(window, centre, 75, 550, 11, (130,255,130))

class boule8(boules):
    def __init__(self, centre):
        super().__init__(window, centre, 85, 600, 12, (130,130,255))'''






pygame.init()

static_lines = []


space = pymunk.Space()
space.gravity = (0, -600)


def collision_callback(arbiter, space, data):
    # Récupère les informations sur les objets en collision
    shape1, shape2 = arbiter.shapes
    new_shape_type = shape1.collision_type + 1

    points = arbiter.contact_point_set.points
    for point in points:
        # Accède aux coordonnées du point de contact
        contact_x, contact_y = point.point_a
        print("Point de contact : ({}, {})".format(contact_x, contact_y))

    space.remove(shape1, shape1.body)
    space.remove(shape2, shape2.body)


    if(new_shape_type == 6):
        planete = Boule2(window, (contact_x, contact_y), space)
        planete.gravite()

    if (new_shape_type == 7):
        planete = Boule3(window, (contact_x, contact_y), space)
        planete.gravite()

    if (new_shape_type == 8):
        planete = Boule4(window, (contact_x, contact_y), space)
        planete.gravite()

    if (new_shape_type == 9):
        planete = Boule5(window, (contact_x, contact_y), space)
        planete.gravite()

    if (new_shape_type == 10):
        planete = Boule6(window, (contact_x, contact_y), space)
        planete.gravite()

    if (new_shape_type == 11):
        planete = Boule7(window, (contact_x, contact_y), space)
        planete.gravite()




    return True  # Retourne True pour permettre à la collision de se produire

# Ajout du gestionnaire de collision
handler = space.add_collision_handler(5, 5)  # Collision entre les objets de type 5
handler2 = space.add_collision_handler(6,6)
handler3 = space.add_collision_handler(7,7)
handler4 = space.add_collision_handler(8,8)
handler5 = space.add_collision_handler(9,9)
handler6 = space.add_collision_handler(10,10)
handler7 = space.add_collision_handler(11,11)
handler.begin = collision_callback
handler2.begin = collision_callback
handler3.begin = collision_callback
handler4.begin = collision_callback
handler5.begin = collision_callback
handler6.begin = collision_callback
handler7.begin = collision_callback



shape1 = pymunk.Segment(space.static_body, (400, 700), (400, 100), 0)
space.add(shape1)

shape2 = pymunk.Segment(space.static_body, (800, 700), (800, 100), 0)
space.add(shape2)

shape3 = pymunk.Segment(space.static_body, (400, 100), (800, 100), 0)
space.add(shape3)

selected_ball_type = None

police = pygame.font.Font(None, 36)
texte = "Salut Pygame !"


running = True
clock = pygame.time.Clock()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        elif event.type == pygame.MOUSEMOTION:

            if selected_ball_type is None:  # Si la boule n'a pas encore été choisie

                selected_ball_type = random.randint(1, 3)  # Choix aléatoire d'un type de boule


        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position_x = pygame.mouse.get_pos()[0]
            if 420 <= mouse_position_x <= 780:
                #typeboule = random.randint(1,3)
                match selected_ball_type:
                    case 1:
                        planete = Boule1(window, (mouse_position_x, 650), space)
                        planete.gravite()
                    case 2:
                        planete = Boule2(window, (mouse_position_x, 650), space)
                        planete.gravite()
                    case 3:
                        planete = Boule3(window, (mouse_position_x, 650), space)
                        planete.gravite()
                selected_ball_type = random.randint(1, 3)



    space.step(1/60)


    clock.tick(60)

    window.fill((249, 228, 183))

    for body in space.bodies:
        for shape in body.shapes:
            if isinstance(shape, pymunk.Circle):
                shape.ball.dessin()

    if selected_ball_type is not None:
        mouse_pos = pygame.mouse.get_pos()
        if selected_ball_type == 1:
            preview_ball = Boule1(window, (mouse_pos[0], 50), space)
        elif selected_ball_type == 2:
            preview_ball = Boule2(window, (mouse_pos[0], 50), space)
        elif selected_ball_type == 3:
            preview_ball = Boule3(window, (mouse_pos[0], 50), space)
        preview_ball.dessin_preview()


    pygame.draw.line(window, (88, 41, 0), (400, 100), (400, 600), 7) #ligne du bas
    pygame.draw.line(window, (88, 41, 0), (800, 100), (800, 600), 7) #droite
    pygame.draw.line(window, (88, 41, 0), (400, 600), (800, 600), 7) #gauche

    texte_surface = police.render(texte, True, (0,0,0))
    # Obtenir le rectangle englobant le texte pour le centrer
    texte_rect = texte_surface.get_rect(center=(100, 100))
    # Dessiner le texte sur la fenêtre à la position texte_rect
    window.blit(texte_surface, texte_rect)

    clock.tick(60)


    # Draw shapes
    ##window.fill((255, 255, 255))
    ##pygame.draw.circle(window, (255, 255, 0), (150, 200), 50)
    ##pygame.draw.rect(window, (0, 200, 0), (100, 300, 300, 200))
    ##pygame.draw.line(window, (0, 0, 100), (100, 100), (700, 500), 5)

    pygame.display.flip()
pygame.quit()