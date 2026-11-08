import pygame
import high_score
import boules

def restart_game(game_state, pygame_handler, physic_space):
    if game_state.score > 0:
        game_state.highscores.append(game_state.score)
        game_state.highscores = sorted(game_state.highscores, reverse=True)[:5]
        high_score.save_highscores(game_state.highscores)

    game_state.game_over = False
    game_state.game_over_sound_played = False
    game_state.score = 0
    game_state.money_power = 0
    game_state.antigravity_cost = game_state.BASE_ANTIGRAVITY_COST
    game_state.delete_cost = game_state.BASE_DELETE_COST

    game_state.can_draw_the_gravity_line = False
    game_state.can_delete_a_boule = False
    game_state.time_without_gravity = None
    game_state.can_create_planete = True
    game_state.time_elapsed.clear()

    physic_space.space.gravity = (0, -1100)
    if physic_space.shape4 is not None:
        if physic_space.shape4 in physic_space.space.shapes:
            physic_space.space.remove(physic_space.shape4)
        physic_space.shape4 = None

    pygame_handler.red_game_over.set_alpha(0)
    pygame_handler.red_screen.stop()
    game_state.red_screen_playing = False
    pygame_handler.game_over_sound.stop()

    if game_state.music_info:
        pygame.mixer.music.unpause()

    game_state.texte = f"Score : {game_state.score}"

    for body in list(physic_space.space.bodies):
        for shape in list(body.shapes):
            physic_space.space.remove(shape)
        physic_space.space.remove(body)

    boules.Boules.instances.clear()
    game_state.selected_ball_type = game_state.pick_random_ball()
    game_state.next_selected_ball_type = game_state.pick_random_ball()