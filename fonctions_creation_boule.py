import random
import pygame
from boules import Boules, Boule1, Boule2, Boule3, Boule4, Boule5

PREVIEW_MAP = {
    1: ("eris.png",      Boules.BALL_CONFIG[5][0], Boule1),
    2: ("pluto 2.5.png", Boules.BALL_CONFIG[6][0], Boule2),
    3: ("mercury 2.png", Boules.BALL_CONFIG[7][0], Boule3),
    4: ("mars.png",      Boules.BALL_CONFIG[8][0], Boule4),
    5: ("venus.png",     Boules.BALL_CONFIG[9][0], Boule5),
}

def get_clamped_drop_x(mouse_x, ball_type):
    _, radius, _ = PREVIEW_MAP.get(ball_type, PREVIEW_MAP[1])
    min_x = 400 + radius + 4
    max_x = 800 - radius - 4
    return max(min_x, min(max_x, mouse_x))

def create_planete(window, space, position_x, ball_type):
    decalage = random.uniform(-0.4, 0.4)
    if ball_type not in PREVIEW_MAP:
        ball_type = 1

    _, _, planet_cls = PREVIEW_MAP[ball_type]
    clamped_x = get_clamped_drop_x(position_x, ball_type)
    planete = planet_cls(window, (clamped_x + decalage, 640), space)
    planete.gravity()
    # Impulsion initiale vers le bas pour éviter les collisions en l'air en tir rapide
    planete.center_masque.velocity = (0, -260)

def create_preview_ball(window, space, mouse_pos, ball_type, Next_Bouboule):
    if ball_type in PREVIEW_MAP:
        sprite_name, radius, _ = PREVIEW_MAP[ball_type]
        clamped_x = get_clamped_drop_x(mouse_pos, ball_type)
        image = Boules.get_cached_sprite(sprite_name, radius)
        rect = image.get_rect(center=(clamped_x, 50))
        window.blit(image, rect.topleft)
    else:
        pygame.draw.circle(window, (0, 0, 0), (mouse_pos, 50), 10)

def next_ball(window, space, next_ball_type):
    if next_ball_type in PREVIEW_MAP:
        sprite_name, radius, _ = PREVIEW_MAP[next_ball_type]
        image = Boules.get_cached_sprite(sprite_name, radius)
        rect = image.get_rect(center=(1037, 187))
        window.blit(image, rect.topleft)
    else:
        pygame.draw.circle(window, (0, 0, 0), (1037, 187), 10)