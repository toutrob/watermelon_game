import random

import pygame
import pymunk
import numpy

window_size = (1200, 700)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Watermelon Game")

class boules :
    def __init__(self,fenetre, centre, rayon, masse, type, sprite):
        self.fenetre = fenetre
        self.rayon = rayon
        self.masse = masse
        self.type = type
        self.sprite = sprite
        self.centre = centre
        self.centremasque = pymunk.Body(1, 100)

    def gravite(self):
        '''centremasque = pymunk.Body(self.masse, 100)'''
        self.centremasque.position = self.centre

        ball_shape = pymunk.Circle(self.centremasque, self.rayon)
        space.add(self.centremasque, ball_shape)



    def dessin(self):
        ball_pos = int(self.centremasque.position.x), window_size[1] - int(self.centremasque.position.y)
        pygame.draw.circle(self.fenetre, (255,0,0), ball_pos, self.rayon)

class boule1(boules):
    def __init__(self, centre):
        super().__init__(window, centre, 10, 10, 1 , "https" )

class boule2(boules):
    def __init__(self, centre):
        super().__init__(window, centre, 20, 10, 2 , "https" )

class boule3(boules):
    def __init__(self, centre):
        super().__init__(window, centre, 35, 10, 2, "https")






pygame.init()

BLUE = (0, 0, 255)
static_lines = []

'''window_size = (1200, 700)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Watermelon Game")'''

space = pymunk.Space()
space.gravity = (0, -500)

'''ball_body = pymunk.Body(1, 100)
ball_body.position = (500, 700)

ball_shape = pymunk.Circle(ball_body, 20)
space.add(ball_body, ball_shape)'''


'''def create_ball(position):
    ball_body = pymunk.Body(1, 100)
    ball_body.position = position
    ball_shape = pymunk.Circle(ball_body, 20)
    space.add(ball_body, ball_shape)'''

shape1 = pymunk.Segment(
    space.static_body, (400, 600), (400, 100), 0.0
    )
space.add(shape1)

shape2 = pymunk.Segment(
    space.static_body, (800, 600), (800, 100), 0.0
    )
space.add(shape2)

shape3 = pymunk.Segment(
    space.static_body, (400, 100), (800, 100), 0.0
    )
space.add(shape3)

terre = boule1((500,500))
mars = boule2((700,500))
terre.gravite()
mars.gravite()

running = True
clock = pygame.time.Clock()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            '''elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                create_ball(mouse_position)'''

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            typeboule = random.randint(1,3)
            match typeboule:
                case 1:
                    planete = boule1(mouse_position)
                    planete.gravite()
                case 2:
                    planete = boule2(mouse_position)
                    planete.gravite()
                case 3:
                    planete = boule3(mouse_position)
                    planete.gravite()

    space.step(1/60)
    '''ball_pos = int(ball_body.position.x), window_size[1] - int(ball_body.position.y)
    pygame.draw.circle(window, BLUE, ball_pos, 20)'''

    '''pygame.display.flip()'''
    clock.tick(60)

    window.fill((249, 228, 183))

    for body in space.bodies:
        for shape in body.shapes:
            if isinstance(shape, pymunk.Circle):
                pos_x, pos_y = int(body.position.x), window_size[1] - int(body.position.y)
                pygame.draw.circle(window, BLUE, (pos_x, pos_y), int(shape.radius))


    pygame.draw.line(window, (88, 41, 0), (400, 100), (400, 600), 7)
    pygame.draw.line(window, (88, 41, 0), (800, 100), (800, 600), 7)
    pygame.draw.line(window, (88, 41, 0), (400, 600), (800, 600), 7)
    '''terre.dessin()'''

    pygame.display.flip()

    clock.tick(60)


    # Draw shapes
    ##window.fill((255, 255, 255))
    ##pygame.draw.circle(window, (255, 255, 0), (150, 200), 50)
    ##pygame.draw.rect(window, (0, 200, 0), (100, 300, 300, 200))
    ##pygame.draw.line(window, (0, 0, 100), (100, 100), (700, 500), 5)

    pygame.display.flip()
pygame.quit()