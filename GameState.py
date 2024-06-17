import high_score
import random

class GameState:
    def __init__(self):
        self.score = 0 #score actuel du joueur

        self.texte = f"Score : {self.score}" #texte montrant au joueur son score actuel

        self.money_pouvoir = 1000 #points permettant l'achet des pouvoirs

        self.highscores = high_score.load_highscores() #liste des highscore
        # usuellement à 5, monte à 6 lorsque une partie recommence

        self.game_over = False #constante changeant au moment ou une partie se finit ou recommence

        self.can_draw_the_gravity_line = False #constante se changeant lors de l'activation de pouvoir 0 gravité
        # empeche le clic pendant la durée du pouvoir
        # repasse a false une fois le pouvoir finit

        self.can_delete_a_boule = False
        # constante changeant au moment de l'acivation du pouvoir "destruction de boule"
        # empeche le clic autre que sur une boule
        # repasse a false une fois que l'on a cliquer une boule

        self.ecran_rouge_playing = False
        #constante gérant si l'ecran rouge de game over imminent doit rester activée

        self.selected_ball_type = random.randint(1, 3)  # Choix aléatoire d'un type de boule


        self.next_Bouboule = True
        #constante gérant l'apparition de la boule dans les airs

        self.next_selected_ball_type = None
        #selection de ce que va être la prochaine boule (en haut a droite)

        self.temps_sans_gravite = None
        #permet de garder en compte depuis combien de temps la gravité est inversée
        #une fois à 3 secondes, cette constante repasse a None

        self.running = True
        #permet de faire tourner la boucle principale

        self.can_create_planete = True
        #permet de dire si une planète peut etre créer ou non
        #permet de set-up le premier type de boule

        self.music_info = True
        #permet de savoir si la musique de fond principale doit être jouée ou non

        self.time_elapsed = {}
        #créer une liste afin de stocker le temps écoulé dedans, utilisé pour l'écran rouge ou les pouvoirs

