import time
import pygame
import pymunk
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

def freeze_while_paused():
    """Fige complètement l'exécution du jeu tant qu'il est en pause ou en arrière-plan."""
    if games_state.game_over:
        return

    games_state.paused = True
    pause_start = time.time()
    pygame.mixer.music.pause()
    pygame.mixer.pause()

    pygame_handler.draw_pause_overlay()
    pygame.display.flip()

    while games_state.paused and games_state.running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                games_state.running = False
                games_state.paused = False
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                games_state.paused = False
            elif ev.type == pygame.KEYDOWN and ev.key in (pygame.K_p, pygame.K_ESCAPE):
                games_state.paused = False
        clock.tick(15)

    paused_duration = time.time() - pause_start
    for b in list(games_state.time_elapsed.keys()):
        games_state.time_elapsed[b] += paused_duration
    if games_state.time_without_gravity is not None:
        games_state.time_without_gravity += paused_duration
    for ball in boules.Boules.instances:
        ball.spawn_time += paused_duration

    pygame.mixer.unpause()
    if games_state.music_info and not games_state.red_screen_playing:
        pygame.mixer.music.unpause()

while games_state.running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            games_state.running = False
        elif event.type in (pygame.WINDOWFOCUSLOST, pygame.WINDOWMINIMIZED):
            freeze_while_paused()
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
            freeze_while_paused()

    if not games_state.running:
        break

    if not games_state.game_over:
        for event in events:
            if event.type == pygame.USEREVENT:
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

                # 1. Boutons du menu et barres de pouvoirs cliquables
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

                # 2. Lâcher d'une planète (bloqué si une boule dépasse déjà hors de la case)
                elif (
                    not boutons.podium_visible
                    and games_state.can_create_planete
                    and not games_state.red_screen_playing
                    and 320 <= mouse_pos[0] <= 880
                ):
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
                    games_state.next_ball_anim_time = time.time()

                    games_state.can_create_planete = False
                    pygame.time.set_timer(pygame.USEREVENT, DROP_COOLDOWN_MS)

        # Simulation physique
        for _ in range(2):
            physic_space.space.step(1 / 120.0)
            physic_space.enforce_boundaries()

        # Détection fiable des boules dont le BAS dépasse la ligne haute (bottom_y > 550)
        now = time.time()
        danger_balls_info = []

        if not games_state.can_draw_the_gravity_line:
            active_bodies = set()
            for ball in boules.Boules.instances:
                body = ball.center_masque
                active_bodies.add(body)
                age = now - ball.spawn_time
                bottom_y = body.position.y - ball.radius

                # Après 0.5s (fin de la chute depuis le haut), si le bas de la boule est hors de la case (> 550)
                if age > 0.5 and bottom_y > 550:
                    if body not in games_state.time_elapsed:
                        games_state.time_elapsed[body] = now
                        ball.in_danger = False
                    else:
                        elapsed = now - games_state.time_elapsed[body]
                        if elapsed > 0.2:
                            danger_elapsed = elapsed - 0.2
                            ball.in_danger = True
                            danger_balls_info.append((ball, danger_elapsed))
                            if danger_elapsed >= 3.0:
                                if games_state.score > 0:
                                    games_state.highscores.append(games_state.score)
                                    games_state.highscores = sorted(games_state.highscores, reverse=True)[:5]
                                games_state.game_over = True
                else:
                    ball.in_danger = False
                    games_state.time_elapsed.pop(body, None)

            for body in list(games_state.time_elapsed.keys()):
                if body not in active_bodies:
                    del games_state.time_elapsed[body]
        else:
            for ball in boules.Boules.instances:
                ball.in_danger = False

        # Gestion sonore de l'alerte (sans clignotement d'écran rouge)
        if danger_balls_info:
            pygame.mixer.music.pause()
            if not games_state.red_screen_playing:
                pygame_handler.red_screen.play()
                games_state.red_screen_playing = True
        else:
            if games_state.red_screen_playing:
                pygame_handler.red_screen.stop()
                games_state.red_screen_playing = False
                if games_state.music_info:
                    pygame.mixer.music.unpause()

        # 1. Fond d'écran + Intérieur spatial de la cuve
        pygame_handler.window.blit(pygame_handler.background_image, (0, 0))
        pygame_handler.draw_chamber_backdrop()

        # 2. Dessin des boules (celles avec ball.in_danger=True clignotent directement en rouge)
        for ball in boules.Boules.instances:
            ball.draw()

        # 3. Boule de prévisualisation en haut
        if games_state.selected_ball_type is not None and not games_state.red_screen_playing:
            mouse_x = pygame.mouse.get_pos()[0]
            fonctions_creation_boule.create_preview_ball(
                pygame_handler.window, physic_space.space, mouse_x,
                games_state.selected_ball_type, games_state.next_Bouboule
            )

        # 4. Prochaine planète animée dans la soucoupe
        if games_state.next_selected_ball_type is not None:
            fonctions_creation_boule.next_ball(
                pygame_handler.window, physic_space.space,
                games_state.next_selected_ball_type, games_state.next_ball_anim_time
            )

        # 5. Pouvoirs actifs
        if games_state.can_draw_the_gravity_line:
            physic_space.anti_gravity_function()

        if games_state.can_delete_a_boule:
            physic_space.delte_ball_function(events)

        # 6. Cadre plasma, chenillard rouge + chrono sur la boule, VFX et barres de pouvoirs
        pygame_handler.affichage_image()
        pygame_handler.draw_danger_zone_and_balls(danger_balls_info)
        pygame_handler.update_and_draw_vfx()
        pygame_handler.draw_power_bars()

        boutons.draw_restart_button_menu(pygame_handler.window, pygame_handler.restart_image)
        boutons.draw_quit_button_menu(pygame_handler.window, pygame_handler.quit_image)
        boutons.draw_podium_button_menu(pygame_handler.window, pygame_handler.podium_image)
        boutons.draw_sound_button_menu(pygame_handler.window, pygame_handler.sound_image, games_state.music_info)

        if boutons.podium_visible:
            pygame_handler.highscores_visibles()

    else:
        pygame_handler.window.blit(pygame_handler.background_image, (0, 0))
        pygame_handler.draw_chamber_backdrop()
        for ball in boules.Boules.instances:
            ball.draw()
        pygame_handler.affichage_image()

        pygame_handler.game_over_screen()
        restart_rect = boutons.draw_restart_button(pygame_handler.window)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(pygame.mouse.get_pos()):
                    RestartFunction.restart_game(games_state, pygame_handler, physic_space)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()