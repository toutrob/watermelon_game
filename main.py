import time
import pygame
import pymunk
import pygame_widgets
import Collisions
import Physic
import boutons
import boules
import fonctions_creation_boule
import RestartFunction
import GameState
import PygameStuff

games_state = GameState.GameState()
pygame_handler = PygameStuff.PygameStuff(games_state)
physic_space = Physic.Physic(games_state, pygame_handler)

for ball_type in range(5, 16):
    handler = physic_space.space.add_collision_handler(ball_type, ball_type)
    handler.begin = lambda arbiter, space, data: Collisions.collision_callback(
        arbiter, physic_space.space, data, pygame_handler.window, games_state, pygame_handler
    )

clock = pygame.time.Clock()
DROP_COOLDOWN_MS = 180

while games_state.running:
    events = pygame.event.get()

    if not games_state.game_over:
        for event in events:
            if event.type == pygame.QUIT:
                games_state.running = False

            elif event.type == pygame.USEREVENT:
                games_state.can_create_planete = True
                pygame.time.set_timer(pygame.USEREVENT, 0)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if games_state.can_delete_a_boule:
                    if boutons.DELETE_CLICK_ZONE.collidepoint(mouse_pos):
                        games_state.can_delete_a_boule = False
                    continue

                if games_state.can_draw_the_gravity_line:
                    continue

                # 1. Boutons du menu et des pouvoirs
                if boutons.RESTART_MENU_RECT.collidepoint(mouse_pos):
                    RestartFunction.restart_game(games_state, pygame_handler, physic_space)

                elif boutons.PODIUM_MENU_RECT.collidepoint(mouse_pos):
                    boutons.toggle_podium()

                elif boutons.SOUND_MENU_RECT.collidepoint(mouse_pos):
                    if games_state.music_info:
                        pygame.mixer.music.pause()
                        games_state.music_info = False
                    else:
                        pygame.mixer.music.unpause()
                        games_state.music_info = True

                elif boutons.ANTIGRAVITY_CLICK_ZONE.collidepoint(mouse_pos):
                    if games_state.money_power >= games_state.antigravity_cost:
                        physic_space.add_bar_antigravity()

                elif boutons.DELETE_CLICK_ZONE.collidepoint(mouse_pos):
                    if games_state.money_power >= games_state.delete_cost and len(boules.Boules.instances) > 0:
                        games_state.can_delete_a_boule = True

                elif boutons.QUIT_MENU_RECT.collidepoint(mouse_pos):
                    games_state.running = False

                # 2. Lâcher d'une planète dans la cuve
                elif not boutons.podium_visible and games_state.can_create_planete and 320 <= mouse_pos[0] <= 880:
                    current_type = games_state.selected_ball_type
                    fonctions_creation_boule.create_planete(
                        pygame_handler.window, physic_space.space, mouse_pos[0], current_type
                    )

                    if current_type == 1:
                        pygame_handler.new_boule1.play()
                    elif current_type == 3:
                        pygame_handler.new_boule3.play()
                    else:
                        pygame_handler.new_boule2.play()

                    games_state.selected_ball_type = games_state.next_selected_ball_type
                    games_state.next_selected_ball_type = games_state.pick_random_ball()

                    games_state.can_create_planete = False
                    pygame.time.set_timer(pygame.USEREVENT, DROP_COOLDOWN_MS)

        # Simulation physique + maintien strict des boules dans la cuve
        for _ in range(2):
            physic_space.space.step(1 / 120.0)
            physic_space.enforce_boundaries()

        # Fond d'écran
        pygame_handler.window.blit(pygame_handler.background_image, (0, 0))

        # Dessin des boules
        for ball in boules.Boules.instances:
            ball.draw()

        # Boule de prévisualisation en haut
        if games_state.selected_ball_type is not None:
            mouse_x = pygame.mouse.get_pos()[0]
            fonctions_creation_boule.create_preview_ball(
                pygame_handler.window, physic_space.space, mouse_x,
                games_state.selected_ball_type, games_state.next_Bouboule
            )

        # Détection de dépassement de la limite haute (Game Over) sans faux positif pendant la chute
        now = time.time()
        danger_active = False

        if not games_state.can_draw_the_gravity_line:
            active_bodies = set()
            for ball in boules.Boules.instances:
                body = ball.center_masque
                active_bodies.add(body)

                # Ignorer toute boule créée il y a moins de 1.5s ou encore en train de tomber
                age = now - ball.spawn_time
                is_falling = body.velocity.y < -60

                bottom_y = body.position.y - ball.radius
                if age > 1.5 and not is_falling and bottom_y > 550:
                    if body not in games_state.time_elapsed:
                        games_state.time_elapsed[body] = now
                    else:
                        elapsed = now - games_state.time_elapsed[body]
                        if elapsed > 0.5:
                            danger_active = True
                        if elapsed > 3.0:
                            if games_state.score > 0:
                                games_state.highscores.append(games_state.score)
                                games_state.highscores = sorted(games_state.highscores, reverse=True)[:5]
                            games_state.game_over = True
                else:
                    games_state.time_elapsed.pop(body, None)

            for body in list(games_state.time_elapsed.keys()):
                if body not in active_bodies:
                    del games_state.time_elapsed[body]

        if danger_active:
            pygame_handler.red_game_over.set_alpha(50)
            pygame.mixer.music.pause()
            if not games_state.red_screen_playing:
                pygame_handler.red_screen.play()
                games_state.red_screen_playing = True
        else:
            pygame_handler.red_game_over.set_alpha(0)
            if games_state.red_screen_playing:
                pygame_handler.red_screen.stop()
                games_state.red_screen_playing = False
                if games_state.music_info:
                    pygame.mixer.music.unpause()

        # Prochaine boule dans la soucoupe
        if games_state.next_selected_ball_type is not None:
            fonctions_creation_boule.next_ball(
                pygame_handler.window, physic_space.space, games_state.next_selected_ball_type
            )

        # Pouvoir Antigravité
        if games_state.can_draw_the_gravity_line:
            pygame.draw.line(pygame_handler.window, (255, 255, 255), (400, 150), (800, 150), 7)
            physic_space.anti_gravity_function()

        # Pouvoir Trou Noir
        if games_state.can_delete_a_boule:
            physic_space.delte_ball_function(events)

        # Affichage de l'UI et des barres de progression
        pygame_handler.affichage_image()
        pygame_widgets.update(events)
        pygame_handler.draw_power_overlays()

        boutons.draw_restart_button_menu(pygame_handler.window, pygame_handler.restart_image)
        boutons.draw_quit_button_menu(pygame_handler.window, pygame_handler.quit_image)
        boutons.draw_podium_button_menu(pygame_handler.window, pygame_handler.podium_image)
        boutons.draw_sound_button_menu(pygame_handler.window, pygame_handler.sound_image, games_state.music_info)
        boutons.draw_antigravity_button(
            pygame_handler.window, pygame_handler.antigravity_image,
            ready=(games_state.money_power >= games_state.antigravity_cost),
            active=games_state.can_draw_the_gravity_line
        )
        boutons.draw_delete_boules(
            pygame_handler.window, pygame_handler.delete_boule_image,
            ready=(games_state.money_power >= games_state.delete_cost),
            active=games_state.can_delete_a_boule
        )

        if boutons.podium_visible:
            pygame_handler.highscores_visibles()

        pygame_handler.window.blit(pygame_handler.red_game_over, (0, 0))

    else:
        pygame_handler.window.blit(pygame_handler.background_image, (0, 0))
        for ball in boules.Boules.instances:
            ball.draw()
        pygame_handler.affichage_image()

        pygame_handler.game_over_screen()
        restart_rect = boutons.draw_restart_button(pygame_handler.window)

        for event in events:
            if event.type == pygame.QUIT:
                games_state.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(pygame.mouse.get_pos()):
                    RestartFunction.restart_game(games_state, pygame_handler, physic_space)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()