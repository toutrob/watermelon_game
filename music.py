import pygame


class SoundManager:
    def __init__(self):
        # Initialiser le mixer de Pygame
        pygame.mixer.init()

        # Charger et jouer la musique de fond en boucle
        pygame.mixer.music.load('musique_fond.mp3')
        pygame.mixer.music.play(-1)
        self.music1 = pygame.mixer.Sound("nouvelle_boule1.mp3")

        # Charger les effets sonores
        self.sounds = {
            'nouvelle_boule1': pygame.mixer.Sound("nouvelle_boule1.mp3"),
            'nouvelle_boule2': pygame.mixer.Sound("nouvelle_boule2.mp3"),
            'nouvelle_boule3': pygame.mixer.Sound("nouvelle_boule3.mp3"),
            'fusion_boule': pygame.mixer.Sound("fusion_boule.mp3"),
            'ecran_rouge': pygame.mixer.Sound("ecran_rouge.mp3"),
            'game_over': pygame.mixer.Sound("game_over.mp3"),
            'antigravity': pygame.mixer.Sound("antigravity.mp3"),
            'delete_boules': pygame.mixer.Sound("delete_boules.mp3")
        }

    def play_sound(self, sound_name):
        """Jouer un son donné par son nom."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Le son '{sound_name}' n'existe pas dans le SoundManager.")