import pygame
import pymunk
class Boules:
    instances = []

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
        self.center_masque.friction = 0.5
        Boules.instances.append(self)
        self.alpha_all = 0
        self.speed_coefficient = speed_coefficient
        self.ball_shape = None

        # Charger le sprite si c'est un chemin d'image
        if isinstance(self.sprite, str):
            self.image = pygame.image.load(self.sprite)
            self.image = pygame.transform.scale(self.image, (2 * self.radius, 2 * self.radius))
        else:
            self.image = None


    def gravity(self):
        self.center_masque.position = self.center


        ball_shape = pymunk.Circle(self.center_masque, self.radius)
        ball_shape.ball = self
        ball_shape.collision_type = self.type
        self.space.add(self.center_masque, ball_shape)
        self.ball_shape = ball_shape



    def draw(self, body1):
        velocity = self.center_masque.velocity.x * self.speed_coefficient
        angular_velocity = velocity / self.radius
        alpha = angular_velocity * (1/60)
        self.alpha_all = self.alpha_all + alpha
        ball_pos = int(self.center_masque.position.x), self.window_size[1] - int(self.center_masque.position.y)

        clickable_rect = None
        if self.image:
            rotated_image = pygame.transform.rotate(self.image, - self.alpha_all)
            rect = rotated_image.get_rect(center=ball_pos)
            self.window.blit(rotated_image, rect.topleft)
            clickable_rect = pygame.Rect(ball_pos[0] - (self.radius/2) - (self.radius/6), ball_pos[1] - (self.radius/2) - (self.radius/6), (self.radius +round(1/3 * (self.radius))), (self.radius + round(1/3 * (self.radius))))



        else:
            pygame.draw.circle(self.window, self.sprite, ball_pos, self.radius)

        return clickable_rect


    def find_per_position(cls, x, y):
        for instance in cls.instances:
            if instance.x == x and instance.y == y:
                return instance
        return None

    def draw_preview(self):
        ball_pos = self.center

        if self.image:
            rect = self.image.get_rect(center=ball_pos)
            self.window.blit(self.image, rect)
        else:
            pygame.draw.circle(self.window, self.sprite, ball_pos, self.radius)


    def find_center(self):
        self.actual_center = self.center_masque.position
        return self.actual_center


class Boule1(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 20, 20, 5, "eris.png", space, 100)

class Boule2(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 25, 25, 6, "pluto 2.5.png", space, 110)

class Boule3(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 35, 35, 7, "mercury 2.png", space, 120)

class Boule4(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 50, 50, 8, "mars.png", space, 130)

class Boule5(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 60, 60, 9, "venus.png", space, 140)

class Boule6(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 70, 70, 10, "earth.png", space, 150)

class Boule7(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 80, 80, 11, "neptune.png", space, 160)

class Boule8(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 90, 90, 12, "uranus.png", space, 170)

class Boule9(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 100, 100, 13, "saturne.png", space, 180)

class Boule10(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 110, 110, 14, "jupiter.png", space, 190)

class Boule11(Boules):
    def __init__(self, window, center, space):
        super().__init__(window, center, 120, 120, 15, "sun.png", space, 200)