import high_score
import pygame
import boules

def restart_game(game_state, pygame_handler, physic_space):
    if game_state.score > 0:
        game_state.highscores.append(game_state.score)
        game_state.highscores = sorted(game_state.highscores, reverse=True)[:5]  # Garder les 5 meilleurs scores
        high_score.save_highscores(game_state.highscores)
    game_state.game_over = False
    game_state.score = 0
    game_state.money_power = 0

    pygame_handler.rouge_game_over.set_alpha(0)
    pygame_handler.game_over_sound.stop()
    if game_state.music_info:
        pygame.mixer.music.unpause()

    game_state.texte = f"Score : {game_state.score}"
    # Supprimer toutes les balles de Pymunk
    for body in physic_space.space.bodies:
        for shape in body.shapes:
            physic_space.space.remove(shape, body)  # Supprimer la forme du corp

    while len(boules.Boules.instances) != 0:
        del boules.Boules.instances[0]

