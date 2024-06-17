import random
import pygame
import pymunk
import time
import pygame_widgets
import Collisions
import Physic
import boutons
import fonctions_creation_boule
import RestartFunction
import GameState
import PygameStuff


etat_du_jeu = GameState.GameState()
affichage_pygame = PygameStuff.PygameStuff(etat_du_jeu)
espace_physique = Physic.Physic(etat_du_jeu, affichage_pygame)




# Ajout du gestionnaire de collision
handler = espace_physique.space.add_collision_handler(5, 5)  # Collision entre les objets de type 5
handler.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, espace_physique.space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler2 = espace_physique.space.add_collision_handler(6, 6)
handler2.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, espace_physique.space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler3 = espace_physique.space.add_collision_handler(7, 7)
handler3.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, espace_physique.space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler4 = espace_physique.space.add_collision_handler(8, 8)
handler4.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, espace_physique.space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler5 = espace_physique.space.add_collision_handler(9, 9)
handler5.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, espace_physique.space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler6 = espace_physique.space.add_collision_handler(10, 10)
handler6.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, espace_physique.space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler7 = espace_physique.space.add_collision_handler(11, 11)
handler7.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, espace_physique.space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler8 = espace_physique.space.add_collision_handler(12, 12)
handler8.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, espace_physique.space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler9 = espace_physique.space.add_collision_handler(13, 13)
handler9.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, espace_physique.space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler10 = espace_physique.space.add_collision_handler(14, 14)
handler10.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, espace_physique.space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)

handler11 = espace_physique.space.add_collision_handler(15, 15)
handler11.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, espace_physique.space, data, affichage_pygame.window,etat_du_jeu, affichage_pygame)




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
                            fonctions_creation_boule.create_planete(affichage_pygame.window, espace_physique.space, mouse_position_x, etat_du_jeu.selected_ball_type)
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
                            fonctions_creation_boule.create_planete(affichage_pygame.window, espace_physique.space, 420, etat_du_jeu.selected_ball_type)
                            etat_du_jeu.selected_ball_type = etat_du_jeu.next_selected_ball_type
                            etat_du_jeu.next_selected_ball_type = random.randint(1, 3)
                            if etat_du_jeu.selected_ball_type == 1:
                                affichage_pygame.nouvelle_boule1.play()
                            elif etat_du_jeu.selected_ball_type == 3:
                                affichage_pygame.nouvelle_boule3.play()
                            else:
                                affichage_pygame.nouvelle_boule2.play()


                        if 880 > mouse_position_x > 780:
                            fonctions_creation_boule.create_planete(affichage_pygame.window, espace_physique.space, 780, etat_du_jeu.selected_ball_type)
                            etat_du_jeu.selected_ball_type = etat_du_jeu.next_selected_ball_type
                            etat_du_jeu.next_selected_ball_type = random.randint(1, 3)
                            if etat_du_jeu.selected_ball_type == 1:
                                affichage_pygame.nouvelle_boule1.play()
                            elif etat_du_jeu.selected_ball_type == 3:
                                affichage_pygame.nouvelle_boule3.play()
                            else:
                                affichage_pygame.nouvelle_boule2.play()



                        etat_du_jeu.can_create_planete = False
                        pygame.time.set_timer(pygame.USEREVENT, 500)

                if event.type == pygame.USEREVENT:
                    etat_du_jeu.can_create_planete = True


                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if boutons.draw_restart_button_menu(affichage_pygame.window, affichage_pygame.restart_image).collidepoint(mouse_pos):
                        RestartFunction.restart_game(etat_du_jeu, affichage_pygame, espace_physique)  # Redémarrer le jeu si le bouton est cliqué

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
                            espace_physique.add_bar_antigravity()


                    if boutons.draw_delete_boules(affichage_pygame.window, affichage_pygame.delete_boule_image).collidepoint(mouse_pos):
                        if(etat_du_jeu.money_pouvoir >= 750):
                            etat_du_jeu.can_delete_a_boule = True
                            etat_du_jeu.money_pouvoir -= 750



                    elif boutons.draw_quit_button_menu(affichage_pygame.window, affichage_pygame.quit_image).collidepoint(mouse_pos):
                        exit()



        espace_physique.space.step(1/60)


        affichage_pygame.window.blit(affichage_pygame.image_de_fond, (0, 0))

        for body in espace_physique.space.bodies:
            for shape in body.shapes:
                if isinstance(shape, pymunk.Circle):
                    shape.ball.dessin(body)

        if etat_du_jeu.selected_ball_type is not None:
            mouse_pos = pygame.mouse.get_pos()[0]
            if 420 <= mouse_pos <= 780:
                fonctions_creation_boule.create_preview_ball(affichage_pygame.window, espace_physique.space, mouse_pos, etat_du_jeu.selected_ball_type, etat_du_jeu.next_Bouboule)


            elif mouse_pos < 420:
                fonctions_creation_boule.create_preview_ball(affichage_pygame.window, espace_physique.space, 420, etat_du_jeu.selected_ball_type, etat_du_jeu.next_Bouboule)

            elif mouse_pos > 780:
                fonctions_creation_boule.create_preview_ball(affichage_pygame.window, espace_physique.space, 780, etat_du_jeu.selected_ball_type, etat_du_jeu.next_Bouboule)


            for body in espace_physique.space.bodies:
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
            fonctions_creation_boule.next_ball(affichage_pygame.window, espace_physique.space, etat_du_jeu.next_selected_ball_type)

        if etat_du_jeu.can_draw_the_gravity_line == True:
            pygame.draw.line(affichage_pygame.window, (255, 255, 255), (400, 150), (800, 150), 7)
            espace_physique.anti_gravity_function()

        if etat_du_jeu.can_delete_a_boule == True :
            espace_physique.delte_ball_function()

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
                    RestartFunction.restart_game(etat_du_jeu, affichage_pygame, espace_physique)  # Redémarrer le jeu si le bouton est cliqué



    clock.tick(60)

    pygame.display.flip()
pygame.quit()