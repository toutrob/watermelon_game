import pygame
import pygame_widgets
from pygame_widgets.progressbar import ProgressBar

class PygameStuff:
    pygame.init()
    pygame.mixer.init()
    def __init__(self, etat_du_jeu):
        self.etat_du_jeu = etat_du_jeu

        self.window_size = (1200, 700) # création d'une fenêtre pygame
        self.window = pygame.display.set_mode(self.window_size) #on met cette fenêtre en mode dessin
        pygame.display.set_caption("Watermelon Game") # on lui donne un nom

        self.police_score = pygame.font.SysFont('nirmala ui', 36)
        # définition de la police d'ecriture utilisée pour écrire le score en temps normal

        self.police_score_menu = pygame.font.SysFont('nirmala ui', 50)
        # définition de la police d'ecriture utilisée pour écrire le score dans les menus

        self.police_next_boule = pygame.font.SysFont('nirmala ui', 18)
        #police servant à écrire "Next" sur la secoupe volante affichant la prochaine boule

        self.police_end = pygame.font.SysFont('adlam display', 70)
        #police servant a afficher que la partie a été perdue

        self.rouge_game_over = pygame.Surface(self.window_size)  # la taille de notre surface
        self.rouge_game_over.set_alpha(0)  # niveau de transparence global
        self.rouge_game_over.fill((255, 0, 0))  # ceci remplit toute la surface

        self.progressBar = ProgressBar(self.window, 900, 500, 200, 40, lambda: etat_du_jeu.money_pouvoir / 400, completedColour=(0, 200, 100), incompletedColour=(255,255,255), curved=True)
        # barre de chargement du pouvoir trou noir
        self.progressBar2 = ProgressBar(self.window, 900, 400, 200, 40, lambda: etat_du_jeu.money_pouvoir / 750, completedColour=(0, 200, 100), incompletedColour=(255,255,255), curved=True)
        # barre de chargement du pouvoir 0 gravité


        #chargement de toutes les images dont on a besoin pour le fond, les boutons, etc...
        self.image_de_fond = pygame.image.load("espace watermelon game (2).png") #image de fond
        self.quit_image = pygame.image.load('exit-run.png') #image du bouton pour quitter
        self.restart_image = pygame.image.load('restart.png') #image du bouton de restart
        self.podium_image = pygame.image.load('podium.png') #image du bouton de podium
        self.sound_image = pygame.image.load('music_off.png') #image du bouton pour couper le son
        self.antigravity_image = pygame.image.load('pomme.png') #image du bouton pour le pouvoir d'anti gravité
        self.delete_boule_image = pygame.image.load('png-clipart-black-hole-car-black-hole-spiral-rim-thumbnail.png')
        # image du bouton pour le pouvoir de trou noir

        #chargement de tous les sons dont on a besoin : musique, effet sonore etc...
        pygame.mixer.music.load('musique_fond.mp3')
        pygame.mixer.music.play(-1)
        self.nouvelle_boule1 = pygame.mixer.Sound("nouvelle_boule1.mp3")
        self.nouvelle_boule2 = pygame.mixer.Sound("nouvelle_boule2.mp3")
        self.nouvelle_boule3 = pygame.mixer.Sound("nouvelle_boule3.mp3")
        self.fusion_boule = pygame.mixer.Sound("fusion_boule.mp3")
        self.ecran_rouge = pygame.mixer.Sound("ecran_rouge.mp3")
        self.game_over_sound = pygame.mixer.Sound("game_over.mp3")
        self.antigravity_sound = pygame.mixer.Sound("antigravity.mp3")
        self.delete_boules_sound = pygame.mixer.Sound("delete_boules.mp3")



    def affichage_image(self):
        pygame.draw.line(self.window, (255, 255, 255), (400, 150), (400, 650), 7)  # ligne du bas
        pygame.draw.line(self.window, (255, 255, 255), (800, 150), (800, 650), 7)  # droite
        pygame.draw.line(self.window, (255, 255, 255), (400, 650), (800, 650), 7)  # gauche

        image_cycle_des_boules = pygame.image.load('Design_sans_titre__3_-removebg-preview.png')
        rect = image_cycle_des_boules.get_rect(center=(200, 375))
        self.window.blit(image_cycle_des_boules, rect.topleft)

        texte_surface = self.police_score.render(self.etat_du_jeu.texte, True, (255, 255, 255))
        # Obtenir le rectangle englobant le texte pour le centrer
        texte_rect = texte_surface.get_rect(center=(100, 100))
        # Dessiner le texte sur la fenêtre à la position texte_rect
        self.window.blit(texte_surface, texte_rect)

        next_boule = self.police_next_boule.render("NEXT :", True, (0, 0, 0))
        rect_next_boule = next_boule.get_rect(center=(1037, 122))
        self.window.blit(next_boule, rect_next_boule)


    def delete_boule_message(self):
        police_delete_boule = pygame.font.Font(None, 20)

        message_surface_delete_a_boule = police_delete_boule.render(
            "Vous voulez utilisez un trou noir, il va supprimer une boule.", True, (255, 255, 255))
        text_rect_delete_a_boule = message_surface_delete_a_boule.get_rect(center=(1000, 350))  # Centrer le texte
        self.window.blit(message_surface_delete_a_boule, text_rect_delete_a_boule)

        message_surface_delete_a_boule2 = police_delete_boule.render("Attention, choisissez bien !", True,
                                                                    (255, 255, 255))
        text_rect_delete_a_boule2 = message_surface_delete_a_boule.get_rect(center=(1000, 365))  # Centrer le texte
        self.window.blit(message_surface_delete_a_boule2, text_rect_delete_a_boule2)


    def highscores_visibles (self):
        s = pygame.Surface((800, 600))  # la taille de votre surface
        s.set_alpha(200)  # niveau de transparence global
        s.fill((255, 255, 255))  # ceci remplit toute la surface
        self.window.blit(s, (200, 50))  # (0,0) sont les coordonnées en haut à gauche
        # Afficher les meilleurs scores
        highscore_title_surface = self.police_score_menu.render("Meilleurs Scores :", True, (0, 0, 0))
        highscore_title_rect = highscore_title_surface.get_rect(center=(600, 150))
        self.window.blit(highscore_title_surface, highscore_title_rect)
        for i, highscore in enumerate(self.etat_du_jeu.highscores):
            highscore_surface = self.police_score_menu.render(f"{i + 1}. {highscore}", True, (0, 0, 0))
            highscore_rect = highscore_surface.get_rect(center=(600, 250 + i * 70))
            self.window.blit(highscore_surface, highscore_rect)


    def game_over_screen(self):
        self.ecran_rouge.stop()
        self.etat_du_jeu.ecran_rouge_playing = False
        self.game_over_sound.play()
        self.window.fill((0, 0, 0))  # Fond noir
        # Afficher le message
        message_surface = self.police_end.render("GAME OVER", True, (255, 54, 0))
        text_rect = message_surface.get_rect(center=(self.window_size[0] // 2, 250))  # Centrer le texte
        self.window.blit(message_surface, text_rect)

        texte_surface = self.police_score.render(self.etat_du_jeu.texte, True, (255, 255, 255))
        texte_rect2 = texte_surface.get_rect(center=(self.window_size[0] // 2, 300))
        self.window.blit(texte_surface, texte_rect2)

        # Afficher les meilleurs scores
        highscore_title_surface = self.police_score.render("Meilleurs Scores :", True, (255, 255, 255))
        highscore_title_rect = highscore_title_surface.get_rect(center=(1000, 200))
        self.window.blit(highscore_title_surface, highscore_title_rect)

        for i, highscore in enumerate(self.etat_du_jeu.highscores):
            highscore_surface = self.police_score.render(f"{i + 1}. {highscore}", True, (255, 255, 255))
            highscore_rect = highscore_surface.get_rect(center=(1000, 250 + i * 50))
            self.window.blit(highscore_surface, highscore_rect)