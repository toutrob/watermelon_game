import random
import pygame
import pymunk
import time
from boules import Boule2, Boule3, Boule4, Boule5, Boule6, Boule7, Boule8, Boule9, Boule10, Boule11
import boutons
import fonctions_creation_boule


WINDOWSIZE = (1200, 700)
window = pygame.display.set_mode(WINDOWSIZE)
pygame.display.set_caption("Watermelon Game")


pygame.init()
image_de_fond = pygame.image.load("espace watermelon game (2).png")

static_lines = []


space = pymunk.Space()
space.gravity = (0, -1000)
space.damping = 0.8


score = 0
texte = f"Score : {score}"


def restart_game():
    global game_over, score, texte
    game_over = False
    score = 0
    texte = f"Score : {score}"
    # Supprimer toutes les balles de Pymunk
    for body in space.bodies:
        for shape in body.shapes:
            space.remove(shape, body)  # Supprimer la forme du corp


def collision_callback(arbiter, space, data):
    global score  # Utilisation de la variable score globale
    global texte


    # Récupère les informations sur les objets en collision
    shape1, shape2 = arbiter.shapes
    new_shape_type = shape1.collision_type + 1

    contact_x = 0
    contact_y = 0

    points = arbiter.contact_point_set.points
    for point in points:
        # Accède aux coordonnées du point de contact
        contact_x, contact_y = point.point_a
        print("Point de contact : ({}, {})".format(contact_x, contact_y))

    space.remove(shape1, shape1.body)
    space.remove(shape2, shape2.body)


    if new_shape_type == 6:
        planete = Boule2(window, (contact_x, contact_y), space)
        planete.gravite()
        score += 1

    elif new_shape_type == 7:
        planete = Boule3(window, (contact_x, contact_y), space)
        planete.gravite()
        score += 3

    elif new_shape_type == 8:
        planete = Boule4(window, (contact_x, contact_y), space)
        planete.gravite()
        score += 6

    elif new_shape_type == 9:
        planete = Boule5(window, (contact_x, contact_y), space)
        planete.gravite()
        score += 10

    elif new_shape_type == 10:
        planete = Boule6(window, (contact_x, contact_y), space)
        planete.gravite()
        score += 15

    elif new_shape_type == 11:
        planete = Boule7(window, (contact_x, contact_y), space)
        planete.gravite()
        score += 21

    elif new_shape_type == 12:
        planete = Boule8(window, (contact_x, contact_y), space)
        planete.gravite()
        score += 28

    elif new_shape_type == 13:
        planete = Boule9(window, (contact_x, contact_y), space)
        planete.gravite()
        score += 36

    elif new_shape_type == 14:
        planete = Boule10(window, (contact_x, contact_y), space)
        planete.gravite()
        score += 45

    elif new_shape_type == 15:
        planete = Boule11(window, (contact_x, contact_y), space)
        planete.gravite()
        score += 55
    else:
        score += 66


    texte = f"Score : {score}"



    return True  # Retourne True pour permettre à la collision de se produire

# Ajout du gestionnaire de collision
handler = space.add_collision_handler(5, 5)  # Collision entre les objets de type 5
handler2 = space.add_collision_handler(6, 6)
handler3 = space.add_collision_handler(7, 7)
handler4 = space.add_collision_handler(8, 8)
handler5 = space.add_collision_handler(9, 9)
handler6 = space.add_collision_handler(10, 10)
handler7 = space.add_collision_handler(11, 11)
handler8 = space.add_collision_handler(12, 12)
handler9 = space.add_collision_handler(13, 13)
handler10 = space.add_collision_handler(14, 14)
handler11 = space.add_collision_handler(15, 15)
handler.begin = collision_callback
handler2.begin = collision_callback
handler3.begin = collision_callback
handler4.begin = collision_callback
handler5.begin = collision_callback
handler6.begin = collision_callback
handler7.begin = collision_callback
handler8.begin = collision_callback
handler9.begin = collision_callback
handler10.begin = collision_callback
handler11.begin = collision_callback



shape1 = pymunk.Segment(space.static_body, (400, 650), (400, 50), 0)
space.add(shape1)

shape2 = pymunk.Segment(space.static_body, (800, 650), (800, 50), 0)
space.add(shape2)

shape3 = pymunk.Segment(space.static_body, (400, 53), (800, 53), 0)
space.add(shape3)

next_selected_ball_type = None
selected_ball_type = random.randint(1, 3)  # Choix aléatoire d'un type de boule

police_score = pygame.font.SysFont('nirmala ui', 36)
police_next_boule = pygame.font.SysFont('nirmala ui', 18)
police_end = pygame.font.SysFont('adlam display', 70)

game_over = False

time_elapsed = {}

running = True
can_create_planete = True
clock = pygame.time.Clock()




while running:
    # Handle events
    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


            elif event.type == pygame.MOUSEMOTION:

                if next_selected_ball_type is None:  # Si la boule n'a pas encore été choisie

                    next_selected_ball_type = random.randint(1, 3)  # Choix aléatoire d'un type de boule


            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if can_create_planete == True:
                    mouse_position_x = pygame.mouse.get_pos()[0]
                    if 420 <= mouse_position_x <= 780:
                        fonctions_creation_boule.create_planete(window, space, mouse_position_x, selected_ball_type)
                        selected_ball_type = next_selected_ball_type
                        next_selected_ball_type = random.randint(1, 3)
                    if 320 < mouse_position_x < 420:
                        fonctions_creation_boule.create_planete(window, space, 420, selected_ball_type)
                        selected_ball_type = next_selected_ball_type
                        next_selected_ball_type = random.randint(1, 3)
                    if 880 > mouse_position_x > 780:
                        fonctions_creation_boule.create_planete(window, space, 780, selected_ball_type)
                        selected_ball_type = next_selected_ball_type
                        next_selected_ball_type = random.randint(1, 3)

                    can_create_planete = False
                    pygame.time.set_timer(pygame.USEREVENT, 500)

            if event.type == pygame.USEREVENT:
                can_create_planete = True


            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if boutons.draw_restart_button_menu(window).collidepoint(mouse_pos):
                    restart_game()  # Redémarrer le jeu si le bouton est cliqué
                elif boutons.draw_quit_button_menu(window).collidepoint(mouse_pos):
                    exit()



        space.step(1/60)


        window.blit(image_de_fond, (0, 0))

        for body in space.bodies:
            for shape in body.shapes:
                if isinstance(shape, pymunk.Circle):
                    shape.ball.dessin()

        if selected_ball_type is not None:
            mouse_pos = pygame.mouse.get_pos()[0]
            if 420 <= mouse_pos <= 780:
                fonctions_creation_boule.create_preview_ball(window, space, mouse_pos, selected_ball_type)
            elif mouse_pos < 420:
                fonctions_creation_boule.create_preview_ball(window, space, 420, selected_ball_type)
            elif mouse_pos > 780:
                fonctions_creation_boule.create_preview_ball(window, space, 780, selected_ball_type)

            for body in space.bodies:
                for shape in body.shapes:
                    if isinstance(shape, pymunk.Circle):
                        bottom_y = shape.body.position.y - shape.radius  # Position en y du bas de la boule
                        if bottom_y > 550:  # Si la boule dépasse une certaine hauteur (par exemple 600 pixels)
                            if body in time_elapsed:
                                if time.time() - time_elapsed[body] > 3:
                                    game_over = True

                            else:
                                # Si c'est la première fois que le corps dépasse la limite, enregistrer le temps actuel
                                time_elapsed[body] = time.time()

                                # Vous pouvez également ajouter du code pour avertir le joueur ici
                                print(
                                    "Attention! Le corps dépasse la limite. Vous avez 3 secondes pour le remettre en dessous.")

            for body in list(time_elapsed.keys()):
                # Convertir body.shapes en liste avant d'accéder à son premier élément
                shapes_list = list(body.shapes)
                if shapes_list and shapes_list[0].body.position.y <= 500:
                    del time_elapsed[body]

        if next_selected_ball_type is not None:
            fonctions_creation_boule.next_ball(window, space, next_selected_ball_type)

        boutons.draw_restart_button_menu(window)
        boutons.draw_quit_button_menu(window)





        pygame.draw.line(window, (255, 255, 255), (400, 150), (400, 650), 7)  #ligne du bas
        pygame.draw.line(window, (255, 255, 255), (800, 150), (800, 650), 7)  #droite
        pygame.draw.line(window, (255, 255, 255), (400, 650), (800, 650), 7)  #gauche

        texte_surface = police_score.render(texte, True, (255, 255, 255))
        # Obtenir le rectangle englobant le texte pour le centrer
        texte_rect = texte_surface.get_rect(center=(100, 100))
        # Dessiner le texte sur la fenêtre à la position texte_rect
        window.blit(texte_surface, texte_rect)

        next_boule = police_next_boule.render("NEXT :", True, (0, 0, 0))
        rect_next_boule = next_boule.get_rect(center=(1037, 122))
        window.blit(next_boule, rect_next_boule)

    else:
        window.fill((0, 0, 0))  # Fond noir
        # Afficher le message
        message_surface = police_end.render("GAME OVER", True, (255, 54, 0))
        text_rect = message_surface.get_rect(center=(WINDOWSIZE[0] // 2, 250))  # Centrer le texte
        window.blit(message_surface, text_rect)

        texte_surface = police_score.render(texte, True, (255, 255, 255))
        texte_rect2 = texte_surface.get_rect(center=(WINDOWSIZE[0] // 2, 300))
        window.blit(texte_surface, texte_rect2)

        boutons.draw_restart_button(window)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if boutons.draw_restart_button(window).collidepoint(mouse_pos):
                    restart_game()  # Redémarrer le jeu si le bouton est cliqué

    clock.tick(60)

    pygame.display.flip()
pygame.quit()