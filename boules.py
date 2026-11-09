import math
import time
import pygame
import pymunk

class Boules:
    instances = []
    _sprite_cache = {}

    # Rouge spatial pastel partagé entre le clignotement de la boule et la barre circulaire
    DANGER_SPACE_RED = (225, 80, 110)

    # type_collision -> (rayon, masse, sprite, coeff_rotation, couleur_halo)
    BALL_CONFIG = {
        5:  (16,  12,  "eris.png",        100, (190, 200, 220)),  # Eris
        6:  (22,  24,  "pluto 2.5.png",   110, (215, 215, 215)),  # Pluto (#c1c1c1 éclairci)
        7:  (30,  45,  "mercury 2.png",   120, (70, 140, 210)),   # Mercury 2 (#3475b6 éclairci)
        8:  (39,  75,  "mars.png",        130, (255, 170, 115)),  # Mars (#f79d65 éclairci)
        9:  (49,  120, "venus.png",       140, (255, 230, 105)),  # Venus (#f9dc5c éclairci)
        10: (60,  180, "earth.png",       150, (75, 155, 255)),   # Earth
        11: (72,  260, "neptune.png",     160, (20, 95, 185)),    # Neptune (#004690 éclairci)
        12: (85,  360, "uranus.png",      170, (100, 165, 235)),  # Uranus (#5492d9 éclairci)
        13: (99,  490, "saturne.png",     180, (145, 30, 215)),   # Saturne (#7209b7 éclairci)
        14: (114, 650, "jupiter.png",     190, (255, 190, 100)),  # Jupiter (#fcaf58 éclairci)
        15: (130, 850, "sun.png",         200, (255, 195, 45)),   # Sun (#fdb31b éclairci)
    }

    @classmethod
    def get_cached_sprite(cls, sprite_path, radius):
        key = (sprite_path, radius)
        if key not in cls._sprite_cache:
            raw_img = pygame.image.load(sprite_path).convert_alpha()
            cls._sprite_cache[key] = pygame.transform.smoothscale(raw_img, (2 * radius, 2 * radius))
        return cls._sprite_cache[key]

    def __init__(self, window, center, radius, weight, type_, sprite, space, speed_coefficient, is_merge=False):
        self.window = window
        self.radius = radius
        self.weight = weight
        self.type = type_
        self.sprite = sprite
        self.space = space
        self.center = center
        self.actual_center = None
        self.window_size = (1200, 700)

        moment = pymunk.moment_for_circle(self.weight, 0, self.radius)
        self.center_masque = pymunk.Body(self.weight, moment)
        Boules.instances.append(self)

        self.alpha_all = 0
        self.speed_coefficient = speed_coefficient
        self.ball_shape = None
        self.merged = False
        self.spawn_time = time.time()
        self.is_merge = is_merge
        self.in_danger = False

        if isinstance(self.sprite, str):
            self.image = self.get_cached_sprite(self.sprite, self.radius)
        else:
            self.image = None

    def gravity(self):
        self.center_masque.position = self.center
        ball_shape = pymunk.Circle(self.center_masque, self.radius)
        ball_shape.friction = 0.22
        ball_shape.elasticity = 0.12
        ball_shape.ball = self
        ball_shape.collision_type = self.type
        self.space.add(self.center_masque, ball_shape)
        self.ball_shape = ball_shape

    def get_screen_pos(self):
        return int(self.center_masque.position.x), self.window_size[1] - int(self.center_masque.position.y)

    def is_clicked(self, mouse_pos):
        bx, by = self.get_screen_pos()
        return math.hypot(mouse_pos[0] - bx, mouse_pos[1] - by) <= self.radius + 3

    def _get_pop_scale(self):
        age = time.time() - self.spawn_time
        if self.is_merge:
            duration = 0.24
            if age < duration:
                p = age / duration
                return 1.0 - 0.45 * math.exp(-6.0 * p) * math.cos(p * math.pi * 2.5)
        else:
            duration = 0.12
            if age < duration:
                p = age / duration
                return 0.75 + 0.25 * math.sin(p * math.pi * 0.5)
        return 1.0

    def draw(self, body1=None):
        velocity = self.center_masque.velocity.x * self.speed_coefficient
        angular_velocity = velocity / self.radius
        alpha = angular_velocity * (1 / 60)
        self.alpha_all = self.alpha_all + alpha
        ball_pos = self.get_screen_pos()

        clickable_rect = pygame.Rect(
            ball_pos[0] - self.radius,
            ball_pos[1] - self.radius,
            2 * self.radius,
            2 * self.radius
        )

        if self.image:
            scale = self._get_pop_scale()
            if abs(scale - 1.0) > 0.015:
                scaled_size = max(4, int(2 * self.radius * scale))
                base_img = pygame.transform.smoothscale(self.image, (scaled_size, scaled_size))
            else:
                base_img = self.image

            rotated_image = pygame.transform.rotate(base_img, -self.alpha_all)
            rect = rotated_image.get_rect(center=ball_pos)
            self.window.blit(rotated_image, rect.topleft)

            # Clignotement rouge pastel semi-transparent (opacité max ~45% pour bien voir la planète)
            if self.in_danger:
                pulse = 0.5 + 0.5 * math.sin(time.time() * 10.0)
                overlay_alpha = int(25 + 90 * pulse)  # Entre 25 et 115 sur 255
                mask = pygame.mask.from_surface(rotated_image)
                tint_surf = mask.to_surface(
                    setcolor=(*self.DANGER_SPACE_RED, overlay_alpha),
                    unsetcolor=(0, 0, 0, 0)
                )
                self.window.blit(tint_surf, rect.topleft)
        else:
            pygame.draw.circle(self.window, self.sprite, ball_pos, self.radius)

        return clickable_rect

    def find_center(self):
        self.actual_center = self.center_masque.position
        return self.actual_center


class Boule1(Boules):
    def __init__(self, window, center, space, is_merge=False):
        super().__init__(window, center, *Boules.BALL_CONFIG[5][:2], 5, "eris.png", space, 100, is_merge)

class Boule2(Boules):
    def __init__(self, window, center, space, is_merge=False):
        super().__init__(window, center, *Boules.BALL_CONFIG[6][:2], 6, "pluto 2.5.png", space, 110, is_merge)

class Boule3(Boules):
    def __init__(self, window, center, space, is_merge=False):
        super().__init__(window, center, *Boules.BALL_CONFIG[7][:2], 7, "mercury 2.png", space, 120, is_merge)

class Boule4(Boules):
    def __init__(self, window, center, space, is_merge=False):
        super().__init__(window, center, *Boules.BALL_CONFIG[8][:2], 8, "mars.png", space, 130, is_merge)

class Boule5(Boules):
    def __init__(self, window, center, space, is_merge=False):
        super().__init__(window, center, *Boules.BALL_CONFIG[9][:2], 9, "venus.png", space, 140, is_merge)

class Boule6(Boules):
    def __init__(self, window, center, space, is_merge=False):
        super().__init__(window, center, *Boules.BALL_CONFIG[10][:2], 10, "earth.png", space, 150, is_merge)

class Boule7(Boules):
    def __init__(self, window, center, space, is_merge=False):
        super().__init__(window, center, *Boules.BALL_CONFIG[11][:2], 11, "neptune.png", space, 160, is_merge)

class Boule8(Boules):
    def __init__(self, window, center, space, is_merge=False):
        super().__init__(window, center, *Boules.BALL_CONFIG[12][:2], 12, "uranus.png", space, 170, is_merge)

class Boule9(Boules):
    def __init__(self, window, center, space, is_merge=False):
        super().__init__(window, center, *Boules.BALL_CONFIG[13][:2], 13, "saturne.png", space, 180, is_merge)

class Boule10(Boules):
    def __init__(self, window, center, space, is_merge=False):
        super().__init__(window, center, *Boules.BALL_CONFIG[14][:2], 14, "jupiter.png", space, 190, is_merge)

class Boule11(Boules):
    def __init__(self, window, center, space, is_merge=False):
        super().__init__(window, center, *Boules.BALL_CONFIG[15][:2], 15, "sun.png", space, 200, is_merge)

BALL_CLASSES = {
    5: Boule1,
    6: Boule2,
    7: Boule3,
    8: Boule4,
    9: Boule5,
    10: Boule6,
    11: Boule7,
    12: Boule8,
    13: Boule9,
    14: Boule10,
    15: Boule11,
}