import math
import time
import pygame
import pymunk
import boules

class Physic:
    def __init__(self, game_state, pygame_handler):
        self.space = pymunk.Space()
        self.space.gravity = (0, -1100)
        self.space.damping = 0.99

        shape1 = pymunk.Segment(self.space.static_body, (400, 750), (400, 50), 4)
        shape1.friction = 0.22
        shape1.elasticity = 0.2
        self.space.add(shape1)

        shape2 = pymunk.Segment(self.space.static_body, (800, 750), (800, 50), 4)
        shape2.friction = 0.22
        shape2.elasticity = 0.2
        self.space.add(shape2)

        shape3 = pymunk.Segment(self.space.static_body, (400, 53), (800, 53), 4)
        shape3.friction = 0.25
        shape3.elasticity = 0.1
        self.space.add(shape3)

        self.shape4 = None
        self.game_state = game_state
        self.pygame_handler = pygame_handler

    def add_bar_antigravity(self):
        if self.game_state.can_draw_the_gravity_line:
            return
        self.pygame_handler.antigravity_sound.play()

        for ball in boules.Boules.instances:
            bx, by = ball.center_masque.position
            min_x = 400 + ball.radius + 4
            max_x = 800 - ball.radius - 4
            max_y = 550 - ball.radius - 5
            clamped_x = max(min_x, min(max_x, bx))
            clamped_y = min(max_y, max(53 + ball.radius + 3, by))
            ball.center_masque.position = (clamped_x, clamped_y)
            ball.center_masque.velocity = (ball.center_masque.velocity.x * 0.5, 180)

        self.shape4 = pymunk.Segment(self.space.static_body, (400, 550), (800, 550), 5)
        self.shape4.friction = 0.22
        self.shape4.elasticity = 0.15
        self.space.add(self.shape4)

        self.space.gravity = (0, 900)
        self.game_state.can_draw_the_gravity_line = True
        self.game_state.time_without_gravity = time.time()
        self.game_state.money_power -= self.game_state.antigravity_cost
        self.game_state.antigravity_cost += 250

    def enforce_boundaries(self):
        antigrav = self.game_state.can_draw_the_gravity_line
        for ball in boules.Boules.instances:
            bx, by = ball.center_masque.position
            vx, vy = ball.center_masque.velocity
            r = ball.radius

            min_x = 400 + r + 2
            max_x = 800 - r - 2
            min_y = 53 + r + 2

            new_x, new_y = bx, by
            new_vx, new_vy = vx, vy

            if bx < min_x:
                new_x = min_x
                new_vx = max(0, vx)
            elif bx > max_x:
                new_x = max_x
                new_vx = min(0, vx)

            if by < min_y:
                new_y = min_y
                new_vy = max(0, vy)

            if antigrav:
                max_y = 550 - r - 3
                if by > max_y:
                    new_y = max_y
                    new_vy = min(0, vy)

            if (new_x, new_y) != (bx, by):
                ball.center_masque.position = (new_x, new_y)
                ball.center_masque.velocity = (new_vx, new_vy)

    def anti_gravity_function(self):
        if self.game_state.time_without_gravity is not None:
            if time.time() - self.game_state.time_without_gravity > 3:
                self.game_state.can_draw_the_gravity_line = False
                if self.shape4 is not None:
                    if self.shape4 in self.space.shapes:
                        self.space.remove(self.shape4)
                    self.shape4 = None
                self.space.gravity = (0, -1100)
                self.game_state.time_without_gravity = None
                self.game_state.time_elapsed.clear()
        else:
            self.game_state.time_without_gravity = time.time()

    def delte_ball_function(self, events=None):
        self.pygame_handler.delete_boule_message()
        mouse_pos = pygame.mouse.get_pos()

        hovered_ball = None
        for ball in reversed(boules.Boules.instances):
            if ball.is_clicked(mouse_pos):
                hovered_ball = ball
                break

        planet_color = (185, 75, 255)
        if hovered_ball is not None:
            bx, by = hovered_ball.get_screen_pos()
            # Récupère la couleur stockée de la planète ciblée
            cfg = boules.Boules.BALL_CONFIG.get(hovered_ball.type)
            if cfg is not None:
                planet_color = cfg[4]

            inner_color = (
                min(255, planet_color[0] + 65),
                min(255, planet_color[1] + 65),
                min(255, planet_color[2] + 65)
            )
            pulse_r = hovered_ball.radius + 6 + int(3 * math.sin(time.time() * 10.0))
            pygame.draw.circle(self.pygame_handler.window, planet_color, (bx, by), pulse_r, 3)
            pygame.draw.circle(self.pygame_handler.window, inner_color, (bx, by), hovered_ball.radius + 2, 1)

        if events is None:
            return

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.game_state.can_delete_a_boule = False
                    return

                if event.button == 1 and hovered_ball is not None:
                    bx, by = hovered_ball.get_screen_pos()
                    self.pygame_handler.delete_boules_sound.play()
                    # Utilise la couleur de la planète pour l'animation de disparition
                    self.pygame_handler.trigger_blackhole_vfx(bx, by, hovered_ball.radius, planet_color)

                    self.game_state.time_elapsed.pop(hovered_ball.center_masque, None)
                    if hovered_ball.ball_shape in self.space.shapes:
                        self.space.remove(hovered_ball.ball_shape, hovered_ball.center_masque)
                    if hovered_ball in boules.Boules.instances:
                        boules.Boules.instances.remove(hovered_ball)

                    self.game_state.money_power -= self.game_state.delete_cost
                    self.game_state.delete_cost += 450
                    self.game_state.can_delete_a_boule = False
                    return