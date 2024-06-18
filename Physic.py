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

        self.game_state = game_state #on va utiliser un objeet de la classe GameState

        self.pygame_handler = pygame_handler  #on va utiliser un objeet de la classe PygameHandler





    def add_bar_antigravity(self):
        self.pygame_handler.antigravity_sound.play() #jouer le son du pouvoir d'anti-gravité
        self.space.gravity = (0, 1000) #changement de gravité dans l'espace
        self.shape4 = pymunk.Segment(self.space.static_body, (400, 550), (800, 550), 0)
        #création de collision sur une barre rajouté en haut de la boite sur la shape4

        self.shape4.friction = 0.5  # Définir le coefficient de frottement
        self.space.add(self.shape4) # ajout de la shape4 dan s l'espace
        self.game_state.can_draw_the_gravity_line = True
        #On definit une constante a True qui empechera la click dans la boucle principale
        #elle sera remise a False au bout de 3 secondes
        self.game_state.money_power -= 400
        #on soustrait le cout du pouvoir

    def anti_gravity_function(self):

        if self.game_state.time_without_gravity is not None:
            #si le on a deja un temps sans gravité on regarde si il est supérieur a 3
            if time.time() - self.game_state.time_without_gravity > 3:
                # on regarde si cela fait 3 secondes que le pouvoir est actif
                # si oui on remet la constante a False et on ré autorise le click
                self.game_state.can_draw_the_gravity_line = False
                if self.shape4 is not None:

                    if self.shape4 in self.space.shapes:
                        self.space.remove(self.shape4)
                        # on supprime la forme de l'espace
                        # on la refixe a None jusqu'a la prochaine activation
                        self.shape4 = None
                    else:
                        self.shape4 = None

                #Enfin on remet fixe la gravité de base
                self.space.gravity = (0, -1000)
                self.game_state.time_without_gravity = None

        else:
            #sinon on défnit le temps de de début du pouvoir
            self.game_state.time_without_gravity = time.time()

    def delte_ball_function(self):
        self.pygame_handler.delete_boule_message()
        #on affiche le message de déscrition du pouvoir

        #on attend un click
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                p = 0
                for shape in boules.Boules.instances:
                    #on attend la collision entre le click et la boule
                    if shape.draw(shape.center_masque).collidepoint(mouse_pos) == True:
                        #si il y a collision entre les deux
                        #on joue le son de suppression des boules
                        self.pygame_handler.delete_boules_sound.play()
                        #on enleve de l'espace la boule à l'endroit du click
                        self.space.remove(shape.ball_shape, shape.center_masque)
                        #on supprime l'OBJET boules
                        del boules.Boules.instances[p]
                        #on repasse la constante empechant le click autre part que sur une boule
                        # a False pour autoriser le click
                        self.game_state.can_delete_a_boule = False
                    p += 1

