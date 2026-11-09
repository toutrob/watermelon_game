import math
import random
import time
import pygame
from boules import Boules, Boule1, Boule2, Boule3, Boule4, Boule5

PREVIEW_MAP = {
    1: ("eris.png",      Boules.BALL_CONFIG[5][0], Boule1, Boules.BALL_CONFIG[5][4]),
    2: ("pluto 2.5.png", Boules.BALL_CONFIG[6][0], Boule2, Boules.BALL_CONFIG[6][4]),
    3: ("mercury 2.png", Boules.BALL_CONFIG[7][0], Boule3, Boules.BALL_CONFIG[7][4]),
    4: ("mars.png",      Boules.BALL_CONFIG[8][0], Boule4, Boules.BALL_CONFIG[8][4]),
    5: ("venus.png",     Boules.BALL_CONFIG[9][0], Boule5, Boules.BALL_CONFIG[9][4]),
}

_smooth_preview_x = 600.0

def get_clamped_drop_x(mouse_x, ball_type):
    _, radius, _, _ = PREVIEW_MAP.get(ball_type, PREVIEW_MAP[1])
    min_x = 400 + radius + 4
    max_x = 800 - radius - 4
    return max(min_x, min(max_x, mouse_x))

def create_planete(window, space, position_x, ball_type):
    decalage = random.uniform(-0.4, 0.4)
    if ball_type not in PREVIEW_MAP:
        ball_type = 1

    _, _, planet_cls, _ = PREVIEW_MAP[ball_type]
    clamped_x = get_clamped_drop_x(position_x, ball_type)
    planete = planet_cls(window, (clamped_x + decalage, 640), space, is_merge=False)
    planete.gravity()
    planete.center_masque.velocity = (0, -280)

def create_preview_ball(window, space, mouse_pos, ball_type, Next_Bouboule):
    global _smooth_preview_x
    if ball_type in PREVIEW_MAP:
        sprite_name, radius, _, glow_col = PREVIEW_MAP[ball_type]
        target_x = get_clamped_drop_x(mouse_pos, ball_type)
        _smooth_preview_x += (target_x - _smooth_preview_x) * 0.35
        draw_x = int(_smooth_preview_x)

        t = time.time()
        bob_y = 50 + int(math.sin(t * 5.0) * 3)

        halo_surf = pygame.Surface((radius * 2 + 24, radius * 2 + 24), pygame.SRCALPHA)
        pulse = int(50 + 25 * math.sin(t * 6.0))
        pygame.draw.circle(halo_surf, (*glow_col, pulse), (radius + 12, radius + 12), radius + 8)
        pygame.draw.circle(halo_surf, (*glow_col, 160), (radius + 12, radius + 12), radius + 4, 2)
        window.blit(halo_surf, halo_surf.get_rect(center=(draw_x, bob_y)))

        image = Boules.get_cached_sprite(sprite_name, radius)
        rect = image.get_rect(center=(draw_x, bob_y))
        window.blit(image, rect.topleft)
    else:
        pygame.draw.circle(window, (0, 0, 0), (mouse_pos, 50), 10)

def next_ball(window, space, next_ball_type, anim_start_time=0.0):
    if next_ball_type in PREVIEW_MAP:
        sprite_name, radius, _, glow_col = PREVIEW_MAP[next_ball_type]
        t = time.time()
        center_x = 1037
        center_y = 187 + int(math.sin(t * 3.8) * 6)

        holo_surf = pygame.Surface((130, 130), pygame.SRCALPHA)
        ring_r1 = int(radius + 10 + 4 * math.sin(t * 4.5))
        ring_r2 = int(radius + 18 + 4 * math.cos(t * 4.5))
        pygame.draw.circle(holo_surf, (*glow_col, 60), (65, 65), ring_r2)
        pygame.draw.circle(holo_surf, (*glow_col, 175), (65, 65), ring_r1, 2)
        window.blit(holo_surf, holo_surf.get_rect(center=(center_x, center_y)))

        image = Boules.get_cached_sprite(sprite_name, radius)

        age = t - anim_start_time
        if age < 0.22:
            p = age / 0.22
            scale = 0.25 + 0.75 * math.sin(p * math.pi * 0.5)
            sz = max(4, int(2 * radius * scale))
            image = pygame.transform.smoothscale(image, (sz, sz))

        rotated = pygame.transform.rotate(image, (t * 28.0) % 360)
        rect = rotated.get_rect(center=(center_x, center_y))
        window.blit(rotated, rect.topleft)
    else:
        pygame.draw.circle(window, (0, 0, 0), (1037, 187), 10)