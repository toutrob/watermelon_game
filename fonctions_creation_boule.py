
from boules import Boule1, Boule2, Boule3
import pygame

def create_planete(window, space, position_x, ball_type):
    '''decalage = random.randint(1, 2)
    if decalage == 1:
        decalage = 0.01
    elif decalage == 2:
        decalage = -0.01
    else:
        decalage = 0
'''
    if ball_type == 1:
        planete = Boule1(window, (position_x , 650), space)
    elif ball_type == 2:
        planete = Boule2(window, (position_x , 650), space)
    elif ball_type == 3:
        planete = Boule3(window, (position_x , 650), space)
    else:
        planete = 0
    planete.gravite()

def create_preview_ball(window, space, mouse_pos, ball_type, Next_Bouboule):
    sprite1 = 'eris.png'
    sprite2 = 'pluto 2.5.png'
    sprite3 = 'mercury 2.png'


    if ball_type == 1:
        image = pygame.image.load(sprite1)
        rect = image.get_rect(center=(mouse_pos, 50))
        window.blit(image, rect.topleft)

    elif ball_type == 2:
        image = pygame.image.load(sprite2)
        rect = image.get_rect(center=(mouse_pos, 50))
        window.blit(image, rect.topleft)

    elif ball_type == 3:
        image = pygame.image.load(sprite3)
        rect = image.get_rect(center=(mouse_pos, 50))
        window.blit(image, rect.topleft)

    else:
        pygame.draw.circle(window, (0, 0, 0), (mouse_pos, 50), 10)


def next_ball(window, space, next_ball_type):
    sprite1 = 'eris.png'
    sprite2 = 'pluto 2.5.png'
    sprite3 = 'mercury 2.png'

    if next_ball_type == 1:
        image = pygame.image.load(sprite1)
        rect = image.get_rect(center=(1037, 187))
        window.blit(image, rect.topleft)

    elif next_ball_type == 2:
        image = pygame.image.load(sprite2)
        rect = image.get_rect(center=(1037, 187))
        window.blit(image, rect.topleft)

    elif next_ball_type == 3:
        image = pygame.image.load(sprite3)
        rect = image.get_rect(center=(1037, 187))
        window.blit(image, rect.topleft)

    else:
        pygame.draw.circle(window, (0, 0, 0), (1037, 187), 10)
