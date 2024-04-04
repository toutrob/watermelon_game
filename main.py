import pygame
import pymunk
import numpy

pygame.init()

BLUE = (0, 0, 255)
static_lines = []

window_size = (1200, 700)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Watermelon Game")

space = pymunk.Space()
space.gravity = (0, -500)

ball_body = pymunk.Body(1, 100)
ball_body.position = (500, 700)

ball_shape = pymunk.Circle(ball_body, 20)
space.add(ball_body, ball_shape)


def create_ball(position):
    ball_body = pymunk.Body(1, 100)
    ball_body.position = position
    ball_shape = pymunk.Circle(ball_body, 20)
    space.add(ball_body, ball_shape)


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



running = True
clock = pygame.time.Clock()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            create_ball(mouse_position)


    space.step(1/60)

    window.fill((249, 228, 183))

    for body in space.bodies:
        for shape in body.shapes:
            if isinstance(shape, pymunk.Circle):
                pos_x, pos_y = int(body.position.x), window_size[1] - int(body.position.y)
                pygame.draw.circle(window, BLUE, (pos_x, pos_y), int(shape.radius))


    pygame.draw.line(window, (88, 41, 0), (400, 100), (400, 600), 7)
    pygame.draw.line(window, (88, 41, 0), (800, 100), (800, 600), 7)
    pygame.draw.line(window, (88, 41, 0), (400, 600), (800, 600), 7)

    pygame.display.flip()

    clock.tick(60)


    # Draw shapes
    ##window.fill((255, 255, 255))
    ##pygame.draw.circle(window, (255, 255, 0), (150, 200), 50)
    ##pygame.draw.rect(window, (0, 200, 0), (100, 300, 300, 200))
    ##pygame.draw.line(window, (0, 0, 100), (100, 100), (700, 500), 5)


pygame.quit()