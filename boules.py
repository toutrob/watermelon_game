import math
import time
import pygame
import pymunk

class Boules:
    instances = []
    _sprite_cache = {}

    # type_collision -> (rayon, masse, sprite, coeff_rotation)
    BALL_CONFIG = {
        5:  (16,  12,  "eris.png",        100),
        6:  (22,  24,  "pluto 2.5.png",   110),
        7:  (30,  45,  "mercury 2.png",   120),
        8:  (39,  75,  "mars.png",        130),
        9:  (49,  120, "venus.png",       140),
        10: (60,  180, "earth.png",       150),
        11: (72,  260, "neptune.png",     160),
        12: (85,  360, "uranus.png",      170),
        13: (99,  490, "saturne.png",     180),
        14: (114, 650, "jupiter.png",     190),
        15: (130, 850, "sun.png",         200),
    }

    @classmethod
    def get_cached_sprite(cls, sprite_path, radius):
        key = (sprite_path, radius)
        if key not in cls._sprite_cache:
            raw_img = pygame.image.load(sprite_path).convert_alpha()
            cls._sprite_cache[key] = pygame.transform.smoothscale(raw_img, (2 * radius, 2 * radius))
        return cls._sprite_cache[key]

    def __init__(self, window, center, radius, weight, type_, sprite, space, speed_coefficient):
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
        self.spawn_time = time.time()  # Enregistre l'heure d'apparition de la boule

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
            rotated_image = pygame.transform.rotate(self.image, -self.alpha_all)
            rect = rotated_image.get_rect(center=ball_pos)
            self.window.blit(rotated_image, rect.topleft)
        else:
            pygame.draw.circle(self.window, self.sprite, ball_pos, self.radius)

        return clickable_rect

    def find_center(self):
        self.actual_center = self.center_masque.position
        return self.actual_center


class Boule1(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, *Boules.BALL_CONFIG[5][:2], 5, "eris.png", space, 100)

class Boule2(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, *Boules.BALL_CONFIG[6][:2], 6, "pluto 2.5.png", space, 110)

class Boule3(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, *Boules.BALL_CONFIG[7][:2], 7, "mercury 2.png", space, 120)

class Boule4(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, *Boules.BALL_CONFIG[8][:2], 8, "mars.png", space, 130)

class Boule5(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, *Boules.BALL_CONFIG[9][:2], 9, "venus.png", space, 140)

class Boule6(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, *Boules.BALL_CONFIG[10][:2], 10, "earth.png", space, 150)

class Boule7(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, *Boules.BALL_CONFIG[11][:2], 11, "neptune.png", space, 160)

class Boule8(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, *Boules.BALL_CONFIG[12][:2], 12, "uranus.png", space, 170)

class Boule9(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, *Boules.BALL_CONFIG[13][:2], 13, "saturne.png", space, 180)

class Boule10(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, *Boules.BALL_CONFIG[14][:2], 14, "jupiter.png", space, 190)

class Boule11(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, *Boules.BALL_CONFIG[15][:2], 15, "sun.png", space, 200)

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