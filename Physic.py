import pymunk
import pygame
import time
import boules

class Physic:

    def __init__(self, game_state, pygame_handler):
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

        self.game_state = game_state

        self.pygame_handler = pygame_handler





    def add_bar_antigravity(self):
        self.pygame_handler.antigravity_sound.play()
        self.space.gravity = (0, 1000)
        self.shape4 = pymunk.Segment(self.space.static_body, (400, 550), (800, 550), 0)
        self.shape4.friction = 0.5  # Définir le coefficient de frottement
        self.space.add(self.shape4)
        self.game_state.can_draw_the_gravity_line = True
        self.game_state.money_power -= 400

    def anti_gravity_function(self):

        if self.game_state.time_without_gravity is not None:
            if time.time() - self.game_state.time_without_gravity > 3:
                self.game_state.can_draw_the_gravity_line = False
                if self.shape4 is not None:

                    if self.shape4 in self.space.shapes:
                        self.space.remove(self.shape4)
                        self.shape4 = None
                    else:
                        self.shape4 = None

                self.space.gravity = (0, -1000)
                self.game_state.time_without_gravity = None

        else:
            self.game_state.time_without_gravity = time.time()

    def delte_ball_function(self):
        self.pygame_handler.delete_boule_message()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                p = 0
                for shape in boules.Boules.instances:
                    if shape.draw(shape.center_masque).collidepoint(mouse_pos) == True:
                        self.pygame_handler.delete_boules_sound.play()
                        self.space.remove(shape.ball_shape, shape.center_masque)
                        del boules.Boules.instances[p]
                        self.game_state.can_delete_a_boule = False
                    p += 1

