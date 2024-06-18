import high_score
import pygame
import boules

#reinitialise l'etat du jeu pour recommencer une nouvelle partie

def restart_game(game_state, pygame_handler, physic_space):
    #sauvegarde du score si il fait partie des 5 meilleur
    if game_state.score > 0:
        game_state.highscores.append(game_state.score)
        game_state.highscores = sorted(game_state.highscores, reverse=True)[:5]  # Garder les 5 meilleurs scores
        high_score.save_highscores(game_state.highscores)
    #reinitialisation des variables d'etat
    game_state.game_over = False
    game_state.score = 0
    game_state.money_power = 0

    #supression de l'ecran game over pour repasser sur le jeu
    pygame_handler.red_game_over.set_alpha(0)
    pygame_handler.game_over_sound.stop()
    if game_state.music_info:
        pygame.mixer.music.unpause()

    #mise a jour de l'affichage du score
    game_state.texte = f"Score : {game_state.score}"

    # Supprimer toutes les balles de Pymunk
    for body in physic_space.space.bodies: #parcourir les corps physique
        for shape in body.shapes: #parcourir les formes des corps
            physic_space.space.remove(shape, body)  # Supprimer

    #supprimer les instances des boules
    while len(boules.Boules.instances) != 0:
        del boules.Boules.instances[0]

