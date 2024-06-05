import pygame
import pymunk

podium_visible = False

def draw_restart_button(window):
    # Dessinez le bouton sur l'écran
    restart_button = pygame.Rect(500, 400, 200, 50)  # Position et taille du bouton
    pygame.draw.rect(window, (0, 255, 0), restart_button)  # Couleur verte pour le bouton
    # Dessinez le texte sur le bouton
    font = pygame.font.Font(None, 36)
    text = font.render("Recommencer", True, (0, 0, 0))  # Texte en noir
    text_rect = text.get_rect(center=restart_button.center)  # Utilisation de restart_button au lieu de button
    window.blit(text, text_rect)
    return restart_button  # Retourner le bouton pour qu'il puisse être utilisé dans la boucle principale

def draw_quit_button_menu(window, quit_image):
    quit_button = pygame.Rect(80, 20, 40, 40)
    quit_image = pygame.transform.scale(quit_image, (quit_button.width, quit_button.height))
    image_rect = quit_image.get_rect(center=quit_button.center)
    window.blit(quit_image, image_rect)
    return quit_button

def draw_restart_button_menu(window, restart_image):
    restart_button = pygame.Rect(20, 20, 40, 40)  # Position et taille du bouton (en haut à gauche)
    restart_image = pygame.transform.scale(restart_image, (restart_button.width, restart_button.height))
    image_rect = restart_image.get_rect(center=restart_button.center)
    window.blit(restart_image, image_rect)
    return restart_button

def draw_podium_button_menu(window, podium_image):
    podium_button = pygame.Rect(140, 20, 40, 40)  # Position et taille du bouton (en haut à gauche)
    podium_image = pygame.transform.scale(podium_image, (podium_button.width, podium_button.height))
    image_rect = podium_image.get_rect(center=podium_button.center)
    window.blit(podium_image, image_rect)
    return podium_button

def draw_antigravity_button(window, antigravity_image):
    antigravity_button = pygame.Rect(1000, 500, 40, 40)
    antigravity_image = pygame.transform.scale(antigravity_image, (antigravity_button.width, antigravity_button.height))
    image_rect = antigravity_image.get_rect(center=antigravity_button.center)
    window.blit(antigravity_image, image_rect)
    return antigravity_button

def toggle_podium():
    global podium_visible
    podium_visible = not podium_visible

def toggle_antigravity(window, gravity):
    gravity = (0, 1000)
    return gravity

'''def draw_antigravity_lines(window, space, gravity):
    pygame.draw.line(window, (255, 255, 255), (400, 150), (800, 150), 7)
    shape4 = pymunk.Segment(space.static_body, (400, 550), (800, 550), 0)
    shape4.friction = 0.5  # Définir le coefficient de frottement
    space.add(shape4)
    return shape4'''

def delete_antigravity_lines(space, forme_a_enlever):
    space.remove(forme_a_enlever)

