import random
import pygame
import pymunk
import time
import pygame_widgets
import Collisions
import Physic
import boules
import boutons
import fonctions_creation_boule
import high_score
import GameState
import PygameStuff


etat_du_jeu = GameState.GameState()
affichage_pygame = PygameStuff.PygameStuff(etat_du_jeu)
espace_physique = Physic.Physic()

pygame.init()


space = pymunk.Space()
space.gravity = (0, -1000)
space.damping = 1


def restart_game():
    if etat_du_jeu.score > 0:
        etat_du_jeu.highscores.append(etat_du_jeu.score)
        etat_du_jeu.highscores = sorted(etat_du_jeu.highscores, reverse=True)[:5]  # Garder les 5 meilleurs scores
        high_score.save_highscores(etat_du_jeu.highscores)
    etat_du_jeu.game_over = False
    etat_du_jeu.score = 0
    etat_du_jeu.money_pouvoir = 0

    affichage_pygame.rouge_game_over.set_alpha(0)
    affichage_pygame.game_over_sound.stop()
    if etat_du_jeu.music_info:
        pygame.mixer.music.unpause()

    etat_du_jeu.texte = f"Score : {etat_du_jeu.score}"
    # Supprimer toutes les balles de Pymunk
    for body in space.bodies:
        for shape in body.shapes:
            space.remove(shape, body)  # Supprimer la forme du corp

    while len(boules.Boules.instances) != 0:
        del boules.Boules.instances[0]




# Ajout du gestionnaire de collision
handler = space.add_collision_handler(5, 5)  # Collision entre les objets de type 5
handler.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler2 = space.add_collision_handler(6, 6)
handler2.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler3 = space.add_collision_handler(7, 7)
handler3.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler4 = space.add_collision_handler(8, 8)
handler4.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler5 = space.add_collision_handler(9, 9)
handler5.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler6 = space.add_collision_handler(10, 10)
handler6.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler7 = space.add_collision_handler(11, 11)
handler7.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler8 = space.add_collision_handler(12, 12)
handler8.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler9 = space.add_collision_handler(13, 13)
handler9.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler10 = space.add_collision_handler(14, 14)
handler10.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler11 = space.add_collision_handler(15, 15)
handler11.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)




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

clock = pygame.time.Clock()


while etat_du_jeu.running:
    # Handle events
    if not etat_du_jeu.game_over:
        events = pygame.event.get()
        for event in events:

            if etat_du_jeu.can_draw_the_gravity_line == False and etat_du_jeu.can_delete_a_boule == False:

                if event.type == pygame.QUIT:
                    etat_du_jeu.running = False



                elif event.type == pygame.MOUSEMOTION:

                    if etat_du_jeu.next_selected_ball_type is None:  # Si la boule n'a pas encore été choisie
                        #next_selected_ball_type = 1
                        etat_du_jeu.next_selected_ball_type = random.randint(1, 3)  # Choix aléatoire d'un type de boule


                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if etat_du_jeu.can_create_planete == True:
                        mouse_position_x = pygame.mouse.get_pos()[0]
                        if 420 <= mouse_position_x <= 780:
                            fonctions_creation_boule.create_planete(affichage_pygame.window, space, mouse_position_x, etat_du_jeu.selected_ball_type)
                            if etat_du_jeu.selected_ball_type == 1:
                                affichage_pygame.nouvelle_boule1.play()
                            elif etat_du_jeu.selected_ball_type == 3:
                                affichage_pygame.nouvelle_boule3.play()
                            else:
                                affichage_pygame.nouvelle_boule2.play()
                            etat_du_jeu.selected_ball_type = etat_du_jeu.next_selected_ball_type
                            etat_du_jeu.next_selected_ball_type = random.randint(1, 3)
                            #next_selected_ball_type = 1

                        if 320 < mouse_position_x < 420:
                            fonctions_creation_boule.create_planete(affichage_pygame.window, space, 420, etat_du_jeu.selected_ball_type)
                            etat_du_jeu.selected_ball_type = etat_du_jeu.next_selected_ball_type
                            etat_du_jeu.next_selected_ball_type = random.randint(1, 3)


                        if 880 > mouse_position_x > 780:
                            fonctions_creation_boule.create_planete(affichage_pygame.window, space, 780, etat_du_jeu.selected_ball_type)
                            etat_du_jeu.selected_ball_type = etat_du_jeu.next_selected_ball_type
                            etat_du_jeu.next_selected_ball_type = random.randint(1, 3)



                        etat_du_jeu.can_create_planete = False
                        pygame.time.set_timer(pygame.USEREVENT, 500)

                if event.type == pygame.USEREVENT:
                    etat_du_jeu.can_create_planete = True


                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if boutons.draw_restart_button_menu(affichage_pygame.window, affichage_pygame.restart_image).collidepoint(mouse_pos):
                        restart_game()  # Redémarrer le jeu si le bouton est cliqué

                    if boutons.draw_podium_button_menu(affichage_pygame.window, affichage_pygame.podium_image).collidepoint(mouse_pos):
                        boutons.toggle_podium()

                    if boutons.draw_sound_button_menu(affichage_pygame.window, affichage_pygame.sound_image).collidepoint(mouse_pos):
                        if etat_du_jeu.music_info == True:
                            pygame.mixer.music.pause()
                            etat_du_jeu.music_info = False
                        else:
                            pygame.mixer.music.unpause()
                            etat_du_jeu.music_info = True

                    if boutons.draw_antigravity_button(affichage_pygame.window, affichage_pygame.antigravity_image).collidepoint(mouse_pos):
                        if(etat_du_jeu.money_pouvoir >= 400):
                            space.gravity = boutons.toggle_antigravity(affichage_pygame.window, space.gravity, affichage_pygame.antigravity_sound)
                            shape4 = pymunk.Segment(space.static_body, (400, 550), (800, 550), 0)
                            shape4.friction = 0.5  # Définir le coefficient de frottement
                            space.add(shape4)
                            etat_du_jeu.can_draw_the_gravity_line = True
                            etat_du_jeu.money_pouvoir -= 400


                    if boutons.draw_delete_boules(affichage_pygame.window, affichage_pygame.delete_boule_image).collidepoint(mouse_pos):
                        if(etat_du_jeu.money_pouvoir >= 750):
                            etat_du_jeu.can_delete_a_boule = True
                            etat_du_jeu.money_pouvoir -= 750



                    elif boutons.draw_quit_button_menu(affichage_pygame.window, affichage_pygame.quit_image).collidepoint(mouse_pos):
                        exit()



        space.step(1/60)


        affichage_pygame.window.blit(affichage_pygame.image_de_fond, (0, 0))

        for body in space.bodies:
            for shape in body.shapes:
                if isinstance(shape, pymunk.Circle):
                    shape.ball.dessin(body)

        if etat_du_jeu.selected_ball_type is not None:
            mouse_pos = pygame.mouse.get_pos()[0]
            if 420 <= mouse_pos <= 780:
                fonctions_creation_boule.create_preview_ball(affichage_pygame.window, space, mouse_pos, etat_du_jeu.selected_ball_type, etat_du_jeu.next_Bouboule)


            elif mouse_pos < 420:
                fonctions_creation_boule.create_preview_ball(affichage_pygame.window, space, 420, etat_du_jeu.selected_ball_type, etat_du_jeu.next_Bouboule)

            elif mouse_pos > 780:
                fonctions_creation_boule.create_preview_ball(affichage_pygame.window, space, 780, etat_du_jeu.selected_ball_type, etat_du_jeu.next_Bouboule)


            for body in space.bodies:
                for shape in body.shapes:
                    if isinstance(shape, pymunk.Circle):
                        bottom_y = shape.body.position.y - shape.radius  # Position en y du bas de la boule
                        if bottom_y > 550:  # Si la boule dépasse une certaine hauteur (par exemple 600 pixels)
                            if body in etat_du_jeu.time_elapsed:
                                if time.time() - etat_du_jeu.time_elapsed[body] > 0.6:
                                    affichage_pygame.rouge_game_over.set_alpha(50)
                                    pygame.mixer.music.pause()
                                    if not etat_du_jeu.ecran_rouge_playing:
                                        affichage_pygame.ecran_rouge.play()
                                        etat_du_jeu.ecran_rouge_playing = True
                                if time.time() - etat_du_jeu.time_elapsed[body] > 3:
                                    etat_du_jeu.game_over = True
                            else:
                                # Si c'est la première fois que le corps dépasse la limite, enregistrer le temps actuel
                                etat_du_jeu.time_elapsed[body] = time.time()

                                # Vous pouvez également ajouter du code pour avertir le joueur ici
                                print("Attention! Le corps dépasse la limite. Vous avez 3 secondes pour le remettre en dessous.")

            for body in list(etat_du_jeu.time_elapsed.keys()):
                # Convertir body.shapes en liste avant d'accéder à son premier élément
                shapes_list = list(body.shapes)
                if shapes_list and shapes_list[0].body.position.y - shapes_list[0].radius <= 500:
                    del etat_du_jeu.time_elapsed[body]
                    affichage_pygame.rouge_game_over.set_alpha(0)
                    affichage_pygame.ecran_rouge.stop()
                    etat_du_jeu.ecran_rouge_playing = False
                    if etat_du_jeu.music_info:
                        pygame.mixer.music.unpause()

        if etat_du_jeu.next_selected_ball_type is not None:
            fonctions_creation_boule.next_ball(affichage_pygame.window, space, etat_du_jeu.next_selected_ball_type)

        if etat_du_jeu.can_draw_the_gravity_line == True:
            pygame.draw.line(affichage_pygame.window, (255, 255, 255), (400, 150), (800, 150), 7)

            if etat_du_jeu.temps_sans_gravite is not None:
                if time.time() - etat_du_jeu.temps_sans_gravite > 3:
                    etat_du_jeu.can_draw_the_gravity_line = False
                    print("ok il faut mettre la fonction")
                    if shape4 is not None:
                        if shape4 in space.shapes:
                            space.remove(shape4)
                            shape4 = None
                        else:
                            shape4 = None

                    space.gravity = (0, -1000)
                    etat_du_jeu.temps_sans_gravite = None

            else:
                etat_du_jeu.temps_sans_gravite = time.time()

        if etat_du_jeu.can_delete_a_boule == True :
            affichage_pygame.delete_boule_message()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    p = 0
                    for shape in boules.Boules.instances:
                        if shape.dessin(shape.centre_masque).collidepoint(mouse_pos) == True:
                            affichage_pygame.delete_boules_sound.play()
                            space.remove(shape.ball_shape, shape.centre_masque)
                            del boules.Boules.instances[p]
                            etat_du_jeu.can_delete_a_boule = False
                        p += 1

        affichage_pygame.affichage_image()

        pygame_widgets.update(events)
        boutons.draw_restart_button_menu(affichage_pygame.window, affichage_pygame.restart_image)
        boutons.draw_quit_button_menu(affichage_pygame.window, affichage_pygame.quit_image)
        boutons.draw_podium_button_menu(affichage_pygame.window, affichage_pygame.podium_image)
        boutons.draw_sound_button_menu(affichage_pygame.window, affichage_pygame.sound_image)
        boutons.draw_antigravity_button(affichage_pygame.window, affichage_pygame.antigravity_image)
        boutons.draw_delete_boules(affichage_pygame.window, affichage_pygame.delete_boule_image)


        if boutons.podium_visible:
            affichage_pygame.highscores_visibles()

        affichage_pygame.window.blit(affichage_pygame.rouge_game_over, (0, 0))  # (0,0) sont les coordonnées en haut à gauche

    else:
        affichage_pygame.game_over_screen()
        boutons.draw_restart_button(affichage_pygame.window)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                etat_du_jeu.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if boutons.draw_restart_button(affichage_pygame.window).collidepoint(mouse_pos):
                    restart_game()  # Redémarrer le jeu si le bouton est cliqué



    clock.tick(60)

    pygame.display.flip()
pygame.quit()