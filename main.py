import random
import pygame
import pymunk
import time
import pygame_widgets
from pygame_widgets.progressbar import ProgressBar

import boules
from boules import Boule2, Boule3, Boule4, Boule5, Boule6, Boule7, Boule8, Boule9, Boule10, Boule11
import boutons
import fonctions_creation_boule
import high_score


WINDOWSIZE = (1200, 700)
window = pygame.display.set_mode(WINDOWSIZE)
pygame.display.set_caption("Watermelon Game")

highscores = high_score.load_highscores()

pygame.init()
pygame.mixer.init()

image_de_fond = pygame.image.load("espace watermelon game (2).png")
quit_image = pygame.image.load('exit-run.png')
restart_image = pygame.image.load('restart.png')
podium_image = pygame.image.load('podium.png')
antigravity_image = pygame.image.load('pomme.png')
delete_boule_image =pygame.image.load('png-clipart-black-hole-car-black-hole-spiral-rim-thumbnail.png')

static_lines = []

pygame.mixer.music.load('musique_fond.mp3')
pygame.mixer.music.play(-1)
nouvelle_boule = pygame.mixer.Sound("nouvelle_boule.mp3")
fusion_boule = pygame.mixer.Sound("fusion_boule.mp3")
ecran_rouge = pygame.mixer.Sound("ecran_rouge.mp3")
game_over_sound = pygame.mixer.Sound("game_over.mp3")

space = pymunk.Space()
space.gravity = (0, -1000)
space.damping = 1
can_draw_the_gravity_line = False
can_delete_a_boule = False


score = 0
texte = f"Score : {score}"
Next_Bouboule = True


def restart_game():
    global game_over, score, texte, highscores
    if score > 0:
        highscores.append(score)
        highscores = sorted(highscores, reverse=True)[:5]  # Garder les 5 meilleurs scores
        high_score.save_highscores(highscores)
    game_over = False
    score = 0
    rouge_game_over.set_alpha(0)
    game_over_sound.stop()
    pygame.mixer.music.unpause()
    texte = f"Score : {score}"
    # Supprimer toutes les balles de Pymunk
    for body in space.bodies:
        for shape in body.shapes:
            space.remove(shape, body)  # Supprimer la forme du corp

    while len(boules.Boules.instances) != 0:
        del boules.Boules.instances[0]


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

    centre_shape1 = shape1.body.position
    centre_shape2 = shape2.body.position


    i = 0
    j = 0

    for bouboules in boules.Boules.instances:
        if bouboules.trouver_centre() == centre_shape1:
            del boules.Boules.instances[i]

            for bouboules2 in boules.Boules.instances:

                if bouboules2.trouver_centre() == centre_shape2:
                    del boules.Boules.instances[j]

                j += 1



        else:
            print("t'as l'air con")
            boule_a_supprimer1 = None
            boule_a_supprimer2 = None

        i += 1

    '''if boule_a_supprimer1 is not None:
        
        del boule_a_supprimer1
    
    if boule_a_supprimer2 is not None:
        del boule_a_supprimer2'''


    space.remove(shape1, shape1.body)
    space.remove(shape2, shape2.body)

    fusion_boule.play()

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
shape1.friction = 0.5  # Définir le coefficient de frottement
space.add(shape1)


shape2 = pymunk.Segment(space.static_body, (800, 650), (800, 50), 0)
shape2.friction = 0.5  # Définir le coefficient de frottement
space.add(shape2)


shape3 = pymunk.Segment(space.static_body, (400, 53), (800, 53), 0)
shape3.friction = 0.5  # Définir le coefficient de frottement
space.add(shape3)

shape4 = None


next_selected_ball_type = None
selected_ball_type = random.randint(1, 3)  # Choix aléatoire d'un type de boule

police_score = pygame.font.SysFont('nirmala ui', 36)
police_score_menu = pygame.font.SysFont('nirmala ui', 50)
police_next_boule = pygame.font.SysFont('nirmala ui', 18)
police_end = pygame.font.SysFont('adlam display', 70)

game_over = False

time_elapsed = {}
temps_sans_gravite = None

running = True
can_create_planete = True
clock = pygame.time.Clock()

rouge_game_over = pygame.Surface(WINDOWSIZE)  # la taille de votre surface
rouge_game_over.set_alpha(0)  # niveau de transparence global
rouge_game_over.fill((255, 0, 0))  # ceci remplit toute la surface

progressBar = ProgressBar(window, 900, 500, 200, 40, lambda: score / 100, completedColour=(0, 200, 100), incompletedColour=(255,255,255), curved=True)
progressBar2 = ProgressBar(window, 900, 400, 200, 40, lambda: score / 100, completedColour=(0, 200, 100), incompletedColour=(255,255,255), curved=True)

while running:
    # Handle events
    if not game_over:
        events = pygame.event.get()
        for event in events:

            if can_draw_the_gravity_line == False and can_delete_a_boule == False:

                if event.type == pygame.QUIT:
                    running = False



                elif event.type == pygame.MOUSEMOTION:

                    if next_selected_ball_type is None:  # Si la boule n'a pas encore été choisie
                        next_selected_ball_type = 1
                        #next_selected_ball_type = random.randint(1, 3)  # Choix aléatoire d'un type de boule


                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if can_create_planete == True:
                        mouse_position_x = pygame.mouse.get_pos()[0]
                        if 420 <= mouse_position_x <= 780:
                            fonctions_creation_boule.create_planete(window, space, mouse_position_x, selected_ball_type)
                            selected_ball_type = next_selected_ball_type
                            next_selected_ball_type = random.randint(1, 3)
                            nouvelle_boule.play()
                            #next_selected_ball_type = 1

                        if 320 < mouse_position_x < 420:
                            fonctions_creation_boule.create_planete(window, space, 420, selected_ball_type)
                            selected_ball_type = next_selected_ball_type
                            next_selected_ball_type = random.randint(1, 3)
                            #next_selected_ball_type = 1

                        if 880 > mouse_position_x > 780:
                            fonctions_creation_boule.create_planete(window, space, 780, selected_ball_type)
                            selected_ball_type = next_selected_ball_type
                            next_selected_ball_type = random.randint(1, 3)
                            #next_selected_ball_type = 1


                        can_create_planete = False
                        pygame.time.set_timer(pygame.USEREVENT, 500)

                if event.type == pygame.USEREVENT:
                    can_create_planete = True


                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if boutons.draw_restart_button_menu(window, restart_image).collidepoint(mouse_pos):
                        restart_game()  # Redémarrer le jeu si le bouton est cliqué
                    if boutons.draw_podium_button_menu(window, podium_image).collidepoint(mouse_pos):
                        boutons.toggle_podium()
                    if boutons.draw_antigravity_button(window, antigravity_image).collidepoint(mouse_pos):
                        space.gravity = boutons.toggle_antigravity(window, space.gravity)
                        shape4 = pymunk.Segment(space.static_body, (400, 550), (800, 550), 0)
                        shape4.friction = 0.5  # Définir le coefficient de frottement
                        space.add(shape4)
                        can_draw_the_gravity_line = True
                    if boutons.draw_delete_boules(window, delete_boule_image).collidepoint(mouse_pos):
                        can_delete_a_boule = True

                    elif boutons.draw_quit_button_menu(window, quit_image).collidepoint(mouse_pos):
                        exit()




        space.step(1/60)



        window.blit(image_de_fond, (0, 0))

        for body in space.bodies:
            for shape in body.shapes:
                if isinstance(shape, pymunk.Circle):
                    shape.ball.dessin(body)

        if selected_ball_type is not None:
            mouse_pos = pygame.mouse.get_pos()[0]
            if 420 <= mouse_pos <= 780:
                fonctions_creation_boule.create_preview_ball(window, space, mouse_pos, selected_ball_type, Next_Bouboule)


            elif mouse_pos < 420:
                fonctions_creation_boule.create_preview_ball(window, space, 420, selected_ball_type, Next_Bouboule)

            elif mouse_pos > 780:
                fonctions_creation_boule.create_preview_ball(window, space, 780, selected_ball_type, Next_Bouboule)


            for body in space.bodies:
                for shape in body.shapes:
                    if isinstance(shape, pymunk.Circle):
                        bottom_y = shape.body.position.y - shape.radius  # Position en y du bas de la boule
                        if bottom_y > 550:  # Si la boule dépasse une certaine hauteur (par exemple 600 pixels)
                            if body in time_elapsed:
                                if time.time() - time_elapsed[body] > 0.6:
                                    rouge_game_over.set_alpha(50)
                                    pygame.mixer.music.pause()
                                    ecran_rouge.play()
                                if time.time() - time_elapsed[body] > 3:
                                    game_over = True
                            else:
                                # Si c'est la première fois que le corps dépasse la limite, enregistrer le temps actuel
                                time_elapsed[body] = time.time()

                                # Vous pouvez également ajouter du code pour avertir le joueur ici
                                print("Attention! Le corps dépasse la limite. Vous avez 3 secondes pour le remettre en dessous.")

            for body in list(time_elapsed.keys()):
                # Convertir body.shapes en liste avant d'accéder à son premier élément
                shapes_list = list(body.shapes)
                if shapes_list and shapes_list[0].body.position.y <= 500:
                    del time_elapsed[body]
                    rouge_game_over.set_alpha(0)
                    ecran_rouge.stop()
                    pygame.mixer.music.unpause()

        if next_selected_ball_type is not None:
            fonctions_creation_boule.next_ball(window, space, next_selected_ball_type)

        if can_draw_the_gravity_line == True:
            #forme_a_supprimer = boutons.draw_antigravity_lines(window, space, space.gravity)
            pygame.draw.line(window, (255, 255, 255), (400, 150), (800, 150), 7)

            if temps_sans_gravite is not None:
                if time.time() - temps_sans_gravite > 3:
                    can_draw_the_gravity_line = False
                    print("ok il faut mettre la fonction")
                    if shape4 is not None:
                        if shape4 in space.shapes:
                            space.remove(shape4)
                            shape4 = None
                        else:
                            shape4 = None

                    space.gravity = (0, -1000)
                    temps_sans_gravite = None

            else:
                temps_sans_gravite = time.time()

        if can_delete_a_boule == True :
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    p = 0
                    for shape in boules.Boules.instances:
                        if shape.dessin(shape.centre_masque).collidepoint(mouse_pos) == True:
                            space.remove(shape.ball_shape, shape.centre_masque)
                            del boules.Boules.instances[p]
                            print("on a atteint ce point")
                            can_delete_a_boule = False
                        p += 1


        image_cycle_des_boules = pygame.image.load('Design_sans_titre__3_-removebg-preview.png')
        rect = image_cycle_des_boules.get_rect(center=(200, 375))
        window.blit(image_cycle_des_boules, rect.topleft)

        pygame_widgets.update(events)
        boutons.draw_restart_button_menu(window, restart_image)
        boutons.draw_quit_button_menu(window, quit_image)
        boutons.draw_podium_button_menu(window, podium_image)
        boutons.draw_antigravity_button(window, antigravity_image)
        boutons.draw_delete_boules(window, delete_boule_image)


        if boutons.podium_visible:
            s = pygame.Surface((800, 600))  # la taille de votre surface
            s.set_alpha(200)  # niveau de transparence global
            s.fill((255, 255, 255))  # ceci remplit toute la surface
            window.blit(s, (200, 50))  # (0,0) sont les coordonnées en haut à gauche
            # Afficher les meilleurs scores
            highscore_title_surface = police_score_menu.render("Meilleurs Scores :", True, (0, 0, 0))
            highscore_title_rect = highscore_title_surface.get_rect(center=(600, 150))
            window.blit(highscore_title_surface, highscore_title_rect)
            for i, highscore in enumerate(highscores):
                highscore_surface = police_score_menu.render(f"{i + 1}. {highscore}", True, (0, 0, 0))
                highscore_rect = highscore_surface.get_rect(center=(600, 250 + i * 70))
                window.blit(highscore_surface, highscore_rect)





        window.blit(rouge_game_over, (0, 0))  # (0,0) sont les coordonnées en haut à gauche



        #print(f"il y a {len(boules.Boules.instances)} boules")


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
        ecran_rouge.stop()
        game_over_sound.play()
        window.fill((0, 0, 0))  # Fond noir
        # Afficher le message
        message_surface = police_end.render("GAME OVER", True, (255, 54, 0))
        text_rect = message_surface.get_rect(center=(WINDOWSIZE[0] // 2, 250))  # Centrer le texte
        window.blit(message_surface, text_rect)

        texte_surface = police_score.render(texte, True, (255, 255, 255))
        texte_rect2 = texte_surface.get_rect(center=(WINDOWSIZE[0] // 2, 300))
        window.blit(texte_surface, texte_rect2)

        # Afficher les meilleurs scores
        highscore_title_surface = police_score.render("Meilleurs Scores :", True, (255, 255, 255))
        highscore_title_rect = highscore_title_surface.get_rect(center=(1000, 200))
        window.blit(highscore_title_surface, highscore_title_rect)

        for i, highscore in enumerate(highscores):
            highscore_surface = police_score.render(f"{i + 1}. {highscore}", True, (255, 255, 255))
            highscore_rect = highscore_surface.get_rect(center=(1000, 250 + i * 50))
            window.blit(highscore_surface, highscore_rect)

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