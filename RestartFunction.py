import high_score
import pygame
import boules

def restart_game(etat_du_jeu, affichage_pygame, espace_physique):
    if etat_du_jeu.score > 0:
        etat_du_jeu.highscores.append(etat_du_jeu.score)
        etat_du_jeu.highscores = sorted(etat_du_jeu.highscores, reverse=True)[:5]  # Garder les 5 meilleurs scores
        high_score.save_highscores(etat_du_jeu.highscores)
    etat_du_jeu.game_over = False
    etat_du_jeu.score = 0
    etat_du_jeu.money_pouvoir = 0

    affichage_pygame.rouge_game_over.set_alpha(0)
    affichage_pygame.game_over_sound.stop()
    if etat_du_jeu.music_info:
        pygame.mixer.music.unpause()

    etat_du_jeu.texte = f"Score : {etat_du_jeu.score}"
    # Supprimer toutes les balles de Pymunk
    for body in espace_physique.space.bodies:
        for shape in body.shapes:
            espace_physique.space.remove(shape, body)  # Supprimer la forme du corp

    while len(boules.Boules.instances) != 0:
        del boules.Boules.instances[0]

