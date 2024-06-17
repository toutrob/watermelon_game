import pymunk
import pygame
import time
import boules

class Physic:

    def __init__(self, etat_du_jeu, affichage_pygame):
        self.space = pymunk.Space() #création d'un espace de gravité
        self.space.gravity = (0, -1000) #set-up des variables de cette espace (-1000 de gravité)
        self.space.damping = 1 #rétention des objets dans l'espace

        shape1 = pymunk.Segment(self.space.static_body, (400, 650), (400, 50), 0)
        shape1.friction = 0.5  # Définir le coefficient de frottement
        self.space.add(shape1)
        #defition des collisions de la barres de gauche

        shape2 = pymunk.Segment(self.space.static_body, (800, 650), (800, 50), 0)
        shape2.friction = 0.5  # Définir le coefficient de frottement
        self.space.add(shape2)
        # defition des collisions de la barres de droite

        shape3 = pymunk.Segment(self.space.static_body, (400, 53), (800, 53), 0)
        shape3.friction = 0.5  # Définir le coefficient de frottement
        self.space.add(shape3)
        # defition des collisions de la barres du bas

        self.shape4 = None #création de ce qui sera plus tard une barre quand la gravité sera inversée

        self.etat_du_jeu = etat_du_jeu

        self.affichage_pygame = affichage_pygame





    def add_bar_antigravity(self):
        self.affichage_pygame.antigravity_sound.play()
        self.space.gravity = (0, 1000)
        self.shape4 = pymunk.Segment(self.space.static_body, (400, 550), (800, 550), 0)
        self.shape4.friction = 0.5  # Définir le coefficient de frottement
        self.space.add(self.shape4)
        self.etat_du_jeu.can_draw_the_gravity_line = True
        self.etat_du_jeu.money_pouvoir -= 400

    def anti_gravity_function(self):

        if self.etat_du_jeu.temps_sans_gravite is not None:
            if time.time() - self.etat_du_jeu.temps_sans_gravite > 3:
                self.etat_du_jeu.can_draw_the_gravity_line = False
                if self.shape4 is not None:

                    if self.shape4 in self.space.shapes:
                        self.space.remove(self.shape4)
                        self.shape4 = None
                    else:
                        self.shape4 = None

                self.space.gravity = (0, -1000)
                self.etat_du_jeu.temps_sans_gravite = None

        else:
            self.etat_du_jeu.temps_sans_gravite = time.time()

    def delte_ball_function(self):
        self.affichage_pygame.delete_boule_message()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                p = 0
                for shape in boules.Boules.instances:
                    if shape.dessin(shape.centre_masque).collidepoint(mouse_pos) == True:
                        self.affichage_pygame.delete_boules_sound.play()
                        self.space.remove(shape.ball_shape, shape.centre_masque)
                        del boules.Boules.instances[p]
                        self.etat_du_jeu.can_delete_a_boule = False
                    p += 1

