import pygame

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