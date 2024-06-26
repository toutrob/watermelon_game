import pygame
#Fichier de gestion des boutons

podium_visible = False

#Bouton du menu game over
def draw_restart_button(window):
    # creation d'un rectangle qui represente le bouton
    restart_button = pygame.Rect(500, 400, 200, 50)  # Position et taille du bouton
    #dessiner le bouton
    pygame.draw.rect(window, (0, 255, 0), restart_button)  # Couleur verte pour le bouton
    # Dessinez le texte sur le bouton
    font = pygame.font.Font(None, 36) #Police et taille du texte
    #ecrit le texte dans le rectangle
    text = font.render("Recommencer", True, (0, 0, 0))  # Texte en noir
    #centrer le texte a l'interieur du bouton
    text_rect = text.get_rect(center=restart_button.center)
    window.blit(text, text_rect) #dessine le tesxte
    return restart_button  # Retourner le bouton pour qu'il puisse être utilisé dans la boucle principale

#Bontons de l'écran de jeu'
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

def draw_sound_button_menu(window, sound_image):
    sound_button = pygame.Rect(200, 20, 40, 40)  # Position et taille du bouton (en haut à gauche)
    sound_image = pygame.transform.scale(sound_image, (sound_button.width, sound_button.height))
    image_rect = sound_image.get_rect(center=sound_button.center)
    window.blit(sound_image, image_rect)
    return sound_button

#Boutons des pouvoirs
def draw_antigravity_button(window, antigravity_image):
    antigravity_button = pygame.Rect(880, 500, 40, 40)
    antigravity_image = pygame.transform.scale(antigravity_image, (antigravity_button.width, antigravity_button.height))
    image_rect = antigravity_image.get_rect(center=antigravity_button.center)
    window.blit(antigravity_image, image_rect)
    return antigravity_button

def draw_delete_boules(window, delete_boule_image):
    delete_bouton = pygame.Rect(880, 400, 40, 40)
    delete_boule_image = pygame.transform.scale(delete_boule_image, (delete_bouton.width, delete_bouton.height))
    image_rect = delete_boule_image.get_rect(center=delete_bouton.center)
    window.blit(delete_boule_image, image_rect)
    return delete_bouton

#Bascule l'etat d'affichage de la fenetre podium en jeu
def toggle_podium():
    global podium_visible
    podium_visible = not podium_visible

#Enleve la ligne qui ferme le rectangle quand le pouvoir antigravité est activé
def delete_antigravity_lines(space, forme_a_enlever):
    space.remove(forme_a_enlever)

