import pygame
from pygame_widgets.progressbar import ProgressBar

class PygameStuff:
    #initialisation des modules
    pygame.init()
    pygame.mixer.init()
    def __init__(self, game_state):
        self.game_state = game_state

        self.window_size = (1200, 700) # création d'une fenêtre pygame
        self.window = pygame.display.set_mode(self.window_size) #on met cette fenêtre en mode dessin
        pygame.display.set_caption("Watermelon Game") # on lui donne un nom

        self.font_score = pygame.font.SysFont('nirmala ui', 36)
        # définition de la font d'ecriture utilisée pour écrire le score en temps normal

        self.font_score_menu = pygame.font.SysFont('nirmala ui', 50)
        # définition de la font d'ecriture utilisée pour écrire le score dans les menus

        self.font_next_boule = pygame.font.SysFont('nirmala ui', 18)
        #font servant à écrire "Next" sur la secoupe volante affichant la prochaine boule

        self.font_end = pygame.font.SysFont('adlam display', 70)
        #font servant a afficher que la partie a été perdue

        self.red_game_over = pygame.Surface(self.window_size)  # la taille de notre surface rouge pour quand une boule est au dessus de la ligne
        self.red_game_over.set_alpha(0)  # niveau de transparence global = 0 pour le moment car pas de danger
        self.red_game_over.fill((255, 0, 0))  # ceci remplit toute la surface avec de rouge

        self.progressBar = ProgressBar(self.window, 900, 500, 200, 40, lambda: game_state.money_power / 400, completedColour=(0, 75, 255), incompletedColour=(255,255,255), curved=True)
        # barre de chargement du pouvoir trou noir
        self.progressBar2 = ProgressBar(self.window, 900, 400, 200, 40, lambda: game_state.money_power / 750, completedColour=(0, 75, 255), incompletedColour=(255,255,255), curved=True)
        # barre de chargement du pouvoir 0 gravité


        #chargement de toutes les images dont on a besoin pour le fond, les boutons, etc...
        self.background_image = pygame.image.load("espace watermelon game (2).png") #image de fond
        self.quit_image = pygame.image.load('exit-run.png') #image du bouton pour quitter
        self.restart_image = pygame.image.load('restart.png') #image du bouton de restart
        self.podium_image = pygame.image.load('podium.png') #image du bouton de podium
        self.sound_image = pygame.image.load('music_off.png') #image du bouton pour couper le son
        self.antigravity_image = pygame.image.load('pomme.png') #image du bouton pour le pouvoir d'anti gravité
        self.delete_boule_image = pygame.image.load('png-clipart-black-hole-car-black-hole-spiral-rim-thumbnail.png')
        # image du bouton pour le pouvoir de trou noir

        #chargement de tous les sons dont on a besoin : musique, effet sonore etc...
        pygame.mixer.music.load('musique_fond.mp3') #musique de fond qui tourne en boucle
        pygame.mixer.music.play(-1)
        self.new_boule1 = pygame.mixer.Sound("nouvelle_boule1.mp3")
        self.new_boule2 = pygame.mixer.Sound("nouvelle_boule2.mp3")
        self.new_boule3 = pygame.mixer.Sound("nouvelle_boule3.mp3")
        self.fusion_boule = pygame.mixer.Sound("fusion_boule.mp3")
        self.red_screen = pygame.mixer.Sound("ecran_rouge.mp3")
        self.game_over_sound = pygame.mixer.Sound("game_over.mp3")
        self.antigravity_sound = pygame.mixer.Sound("antigravity.mp3")
        self.delete_boules_sound = pygame.mixer.Sound("delete_boules.mp3")


#gestion de l'affichage des elements graphiques à l'ecran
    def affichage_image(self):
        #Trois lignes blanches sont dessinées pour créer un cadre.
        pygame.draw.line(self.window, (255, 255, 255), (400, 150), (400, 650), 7)  # ligne du bas
        pygame.draw.line(self.window, (255, 255, 255), (800, 150), (800, 650), 7)  # droite
        pygame.draw.line(self.window, (255, 255, 255), (400, 650), (800, 650), 7)  # gauche

        #affichage d'une image
        image_boules_life_cycle = pygame.image.load('Design_sans_titre__3_-removebg-preview.png')
        rect = image_boules_life_cycle.get_rect(center=(200, 375))
        self.window.blit(image_boules_life_cycle, rect.topleft)

        #texte du score
        texte_surface = self.font_score.render(self.game_state.texte, True, (255, 255, 255))
        # Obtenir le rectangle englobant le texte pour le centrer
        texte_rect = texte_surface.get_rect(center=(100, 100))
        # Dessiner le texte sur la fenêtre à la position texte_rect
        self.window.blit(texte_surface, texte_rect)

        #boules suivante
        next_boule = self.font_next_boule.render("NEXT :", True, (0, 0, 0))
        rect_next_boule = next_boule.get_rect(center=(1037, 122))
        self.window.blit(next_boule, rect_next_boule)


    #pour afficher un message a l'utilisateur lors de l'utilisation du pouvoir trou noir
    def delete_boule_message(self):
        font_delete_boule = pygame.font.Font(None, 20)

        message_surface_delete_a_boule = font_delete_boule.render(
            "Vous voulez utilisez un trou noir, il va supprimer une boule.", True, (255, 255, 255))
        text_rect_delete_a_boule = message_surface_delete_a_boule.get_rect(center=(1000, 350))  # Centrer le texte
        self.window.blit(message_surface_delete_a_boule, text_rect_delete_a_boule)

        message_surface_delete_a_boule2 = font_delete_boule.render("Attention, choisissez bien !", True,
                                                                    (255, 255, 255))
        text_rect_delete_a_boule2 = message_surface_delete_a_boule.get_rect(center=(1000, 365))  # Centrer le texte
        self.window.blit(message_surface_delete_a_boule2, text_rect_delete_a_boule2)

    #affiche la fenetre du highscore en superposition du jeu
    def highscores_visibles (self):
        s = pygame.Surface((800, 600))  # la taille de la surface
        s.set_alpha(200)  # niveau de transparence global
        s.fill((255, 255, 255))  # ceci remplit toute la surface
        self.window.blit(s, (200, 50))  # (0,0) coordonnées en haut à gauche
        # Afficher les meilleurs scores
        highscore_title_surface = self.font_score_menu.render("Meilleurs Scores :", True, (0, 0, 0))
        highscore_title_rect = highscore_title_surface.get_rect(center=(600, 150))
        self.window.blit(highscore_title_surface, highscore_title_rect)
        for i, highscore in enumerate(self.game_state.highscores):
            highscore_surface = self.font_score_menu.render(f"{i + 1}. {highscore}", True, (0, 0, 0))
            highscore_rect = highscore_surface.get_rect(center=(600, 250 + i * 70))
            self.window.blit(highscore_surface, highscore_rect)

    #permet d'afficher l'ecran game over
    def game_over_screen(self):
        self.red_screen.stop() #arret de l'ecran rouge
        self.game_state.red_screen_playing = False
        self.game_over_sound.play() #joue la musique game over
        self.window.fill((0, 0, 0))  # Fond noir
        # Afficher le message
        message_surface = self.font_end.render("GAME OVER", True, (255, 54, 0))
        text_rect = message_surface.get_rect(center=(self.window_size[0] // 2, 250))  # Centrer le texte
        self.window.blit(message_surface, text_rect)

        #affiche es score actuel
        texte_surface = self.font_score.render(self.game_state.texte, True, (255, 255, 255))
        texte_rect2 = texte_surface.get_rect(center=(self.window_size[0] // 2, 300))
        self.window.blit(texte_surface, texte_rect2)

        # Afficher les meilleurs scores
        highscore_title_surface = self.font_score.render("Meilleurs Scores :", True, (255, 255, 255))
        highscore_title_rect = highscore_title_surface.get_rect(center=(1000, 200))
        self.window.blit(highscore_title_surface, highscore_title_rect)

        for i, highscore in enumerate(self.game_state.highscores):
            highscore_surface = self.font_score.render(f"{i + 1}. {highscore}", True, (255, 255, 255))
            highscore_rect = highscore_surface.get_rect(center=(1000, 250 + i * 50))
            self.window.blit(highscore_surface, highscore_rect)