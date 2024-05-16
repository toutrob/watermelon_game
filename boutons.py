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

def draw_quit_button_menu(window: object) -> object:
    quit_button = pygame.Rect(80, 20, 40, 40)
    pygame.draw.rect(window, (0, 255, 0), quit_button)
    font = pygame.font.Font(None, 20)
    text = font.render("quit", True, (0, 0, 0))
    text_rect = text.get_rect(center=quit_button.center)
    window.blit(text, text_rect)
    return quit_button

def draw_restart_button_menu(window):
    restart_button = pygame.Rect(20, 20, 40, 40)  # Position et taille du bouton (en haut à gauche)
    pygame.draw.rect(window, (0, 255, 0), restart_button)  # Couleur verte pour le bouton
    # Dessinez le texte sur le bouton
    font = pygame.font.Font(None, 20)
    text = font.render("restart", True, (0, 0, 0))  # Texte en noir
    text_rect = text.get_rect(center=restart_button.center)  # Centre du texte sur le bouton
    window.blit(text, text_rect)
    return restart_button