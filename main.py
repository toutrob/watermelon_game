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


games_state = GameState.GameState()
#création d'un objet etat du jeu, stockant énormément de variable globale
pygame_handler = PygameStuff.PygameStuff(games_state)
#création d'un objet Gérant tout ce qui concerne pygame, (musique, image, texte ...)
physic_space = Physic.Physic(games_state, pygame_handler)
#cration d'un ojet gérant tout ce qui concerne l'espace physique (space, gravité, trou_noir...)




# Ajout du gestionnaire de collision
handler = physic_space.space.add_collision_handler(5, 5)  # Collision entre les objets de type 5
#handler.begin dit ce qui va se passer lorsque une collision entre deux forme de type (5,5) va se passer
#la fonction lambda est une fonction qui va donner les 3 arguments arbiter, space, data
#c'est un moyen d'écrire et d'appeler une fonction de manière concise
handler.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, physic_space.space, data, pygame_handler.window, games_state, pygame_handler)

handler2 = physic_space.space.add_collision_handler(6, 6)
handler2.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, physic_space.space, data, pygame_handler.window,games_state, pygame_handler)

handler3 = physic_space.space.add_collision_handler(7, 7)
handler3.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, physic_space.space, data, pygame_handler.window,games_state, pygame_handler)

handler4 = physic_space.space.add_collision_handler(8, 8)
handler4.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, physic_space.space, data, pygame_handler.window,games_state, pygame_handler)

handler5 = physic_space.space.add_collision_handler(9, 9)
handler5.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, physic_space.space, data, pygame_handler.window,games_state, pygame_handler)

handler6 = physic_space.space.add_collision_handler(10, 10)
handler6.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, physic_space.space, data, pygame_handler.window,games_state, pygame_handler)

handler7 = physic_space.space.add_collision_handler(11, 11)
handler7.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, physic_space.space, data, pygame_handler.window,games_state, pygame_handler)

handler8 = physic_space.space.add_collision_handler(12, 12)
handler8.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, physic_space.space, data, pygame_handler.window,games_state, pygame_handler)

handler9 = physic_space.space.add_collision_handler(13, 13)
handler9.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, physic_space.space, data, pygame_handler.window,games_state, pygame_handler)

handler10 = physic_space.space.add_collision_handler(14, 14)
handler10.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, physic_space.space, data, pygame_handler.window,games_state, pygame_handler)

handler11 = physic_space.space.add_collision_handler(15, 15)
handler11.begin = lambda arbiter, space, data: Collisions.collision_callback(arbiter, physic_space.space, data, pygame_handler.window,games_state, pygame_handler)



clock = pygame.time.Clock()

#début de la boucle principale
while games_state.running:
    # gestion des evenements
    if not games_state.game_over:
        events = pygame.event.get()
        for event in events:
            #Si une dee ces variables = true, une pouvoir est en cours,
            #on bloque alors toute action autre que celles autoriser pour les pouvoirs
            # (menus, boutons, création de boule...)
            if games_state.can_draw_the_gravity_line == False and games_state.can_delete_a_boule == False:

                if event.type == pygame.QUIT:
                    games_state.running = False



                elif event.type == pygame.MOUSEMOTION:

                    if games_state.next_selected_ball_type is None:  # Si la boule n'a pas encore été choisie
                        games_state.next_selected_ball_type = random.randint(1, 3)  # Choix aléatoire d'un type de boule

                #losrque clique -> on pose une boule au bon endroit
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if games_state.can_create_planete == True:
                        mouse_position_x = pygame.mouse.get_pos()[0]
                        #permet de pouvoir placer la boule si on clique dans la cuve
                        if 420 <= mouse_position_x <= 780:
                            fonctions_creation_boule.create_planete(pygame_handler.window, physic_space.space, mouse_position_x, games_state.selected_ball_type)
                            if games_state.selected_ball_type == 1:
                                #on joue le son d'apparition des boules
                                pygame_handler.new_boule1.play()
                            elif games_state.selected_ball_type == 3:
                                pygame_handler.new_boule3.play()
                            else:
                                pygame_handler.new_boule2.play()
                            #on passe le type de la prochaine boule comme le type de la boule actuelle
                            games_state.selected_ball_type = games_state.next_selected_ball_type

                            #on créer un nouveau type aléatoire pour la boule suivante
                            games_state.next_selected_ball_type = random.randint(1, 3)

                        #permet ici de placer une boule légèrement à gauche de la cuve
                        if 320 < mouse_position_x < 420:
                            fonctions_creation_boule.create_planete(pygame_handler.window, physic_space.space, 420, games_state.selected_ball_type)
                            games_state.selected_ball_type = games_state.next_selected_ball_type
                            games_state.next_selected_ball_type = random.randint(1, 3)
                            if games_state.selected_ball_type == 1:
                                pygame_handler.new_boule1.play()
                            elif games_state.selected_ball_type == 3:
                                pygame_handler.new_boule3.play()
                            else:
                                pygame_handler.new_boule2.play()

                        # permet ici de placer une boule légèrement à droite de la cuve
                        if 880 > mouse_position_x > 780:
                            fonctions_creation_boule.create_planete(pygame_handler.window, physic_space.space, 780, games_state.selected_ball_type)
                            games_state.selected_ball_type = games_state.next_selected_ball_type
                            games_state.next_selected_ball_type = random.randint(1, 3)
                            if games_state.selected_ball_type == 1:
                                pygame_handler.new_boule1.play()
                            elif games_state.selected_ball_type == 3:
                                pygame_handler.new_boule3.play()
                            else:
                                pygame_handler.new_boule2.play()


                        #Si la souris n'est pas au bon endroit on empêche la création de boule
                        games_state.can_create_planete = False
                        #permet d'empecher le spam de spawn de boules
                        pygame.time.set_timer(pygame.USEREVENT, 500)

                #re-permet de créer des boules
                if event.type == pygame.USEREVENT:
                    games_state.can_create_planete = True

                #Gestion de tous les clicks sur les boutons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if boutons.draw_restart_button_menu(pygame_handler.window, pygame_handler.restart_image).collidepoint(mouse_pos):
                        RestartFunction.restart_game(games_state, pygame_handler, physic_space)  # Redémarrer le jeu si le bouton est cliqué

                    if boutons.draw_podium_button_menu(pygame_handler.window, pygame_handler.podium_image).collidepoint(mouse_pos):
                        boutons.toggle_podium()     #affiche les highscores quand le bouton est cliqué

                    if boutons.draw_sound_button_menu(pygame_handler.window, pygame_handler.sound_image).collidepoint(mouse_pos):
                        #enlève et remet la musique si ce bouton est cliqué
                        if games_state.music_info == True:
                            pygame.mixer.music.pause()
                            games_state.music_info = False
                        else:
                            pygame.mixer.music.unpause()
                            games_state.music_info = True

                    if boutons.draw_antigravity_button(pygame_handler.window, pygame_handler.antigravity_image).collidepoint(mouse_pos):
                        #active le pouvoir d'antigravité si bouton cliqué et assez d'argent
                        if(games_state.money_power >= 400):
                            physic_space.add_bar_antigravity()


                    if boutons.draw_delete_boules(pygame_handler.window, pygame_handler.delete_boule_image).collidepoint(mouse_pos):
                        #active le pouvoir de trou noir si bouton cliqué et assez d'argent
                        if(games_state.money_power >= 750):
                            games_state.can_delete_a_boule = True
                            games_state.money_power -= 750



                    elif boutons.draw_quit_button_menu(pygame_handler.window, pygame_handler.quit_image).collidepoint(mouse_pos):
                        #permet de quitter le jeu
                        exit()


        physic_space.space.step(1/60)

        #affiche l'image de fond
        pygame_handler.window.blit(pygame_handler.background_image, (0, 0))

        #gère l'affichage de toutes les boules en parcourant la liste de tous les corps physique
        for body in physic_space.space.bodies:
            for shape in body.shapes:
                if isinstance(shape, pymunk.Circle):
                    shape.ball.draw(body)

        #gestion de l'affichage de la boule qui flotte
        if games_state.selected_ball_type is not None:
            #si dans la cuve on suit le curseur
            mouse_pos = pygame.mouse.get_pos()[0]
            if 420 <= mouse_pos <= 780:
                fonctions_creation_boule.create_preview_ball(pygame_handler.window, physic_space.space, mouse_pos, games_state.selected_ball_type, games_state.next_Bouboule)

            #si trop a gauche on colle a gauche
            elif mouse_pos < 420:
                fonctions_creation_boule.create_preview_ball(pygame_handler.window, physic_space.space, 420, games_state.selected_ball_type, games_state.next_Bouboule)

            #si trop a droite on colle a droite
            elif mouse_pos > 780:
                fonctions_creation_boule.create_preview_ball(pygame_handler.window, physic_space.space, 780, games_state.selected_ball_type, games_state.next_Bouboule)

            #gestion de l'ecran rouge pour le game over
            for body in physic_space.space.bodies:
                for shape in body.shapes:
                    if isinstance(shape, pymunk.Circle):
                        bottom_y = shape.body.position.y - shape.radius  # Position en y du bas de la boule
                        if bottom_y > 550:  # Si la boule dépasse une certaine hauteur (par exemple 600 pixels)
                            if body in games_state.time_elapsed:
                                #si le temps au dessus de la ligne > 0.6 on active l'ecran rouge et la musique sinon rien
                                if time.time() - games_state.time_elapsed[body] > 0.6:
                                    pygame_handler.red_game_over.set_alpha(50)
                                    pygame.mixer.music.pause()
                                    if not games_state.red_screen_playing:
                                        pygame_handler.red_screen.play()
                                        games_state.red_screen_playing = True
                                #si le temps au dessus de 3 secondes, on declenche le game_over
                                if time.time() - games_state.time_elapsed[body] > 3:
                                    games_state.game_over = True
                            else:
                                # Si c'est la première fois que le corps dépasse la limite,on enregistre le temps actuel
                                games_state.time_elapsed[body] = time.time()

                                # ajouter du code pour avertir le joueur ici
                                print("Attention! Le corps dépasse la limite. Vous avez 3 secondes pour le remettre en dessous.")

            #enleve les boules de la liste de l'ecran rouge et enleve l'ecran rouge si il desend en dessous de la ligne
            for body in list(games_state.time_elapsed.keys()):
                # Convertir body.shapes en liste avant d'accéder à son premier élément
                shapes_list = list(body.shapes)
                if shapes_list and shapes_list[0].body.position.y - shapes_list[0].radius <= 550:
                    del games_state.time_elapsed[body]
                    pygame_handler.red_game_over.set_alpha(0)
                    pygame_handler.red_screen.stop()
                    games_state.red_screen_playing = False
                    if games_state.music_info:
                        pygame.mixer.music.unpause()

        #création de la boule en haut a gauche
        if games_state.next_selected_ball_type is not None:
            fonctions_creation_boule.next_ball(pygame_handler.window, physic_space.space, games_state.next_selected_ball_type)

        #si le bouton anti gravity est activé, on fait la fonction anti_gravité
        if games_state.can_draw_the_gravity_line == True:
            pygame.draw.line(pygame_handler.window, (255, 255, 255), (400, 150), (800, 150), 7)
            physic_space.anti_gravity_function()

        #si le bouton trou noir est activé, on fait la fonction trou noir
        if games_state.can_delete_a_boule == True :
            physic_space.delte_ball_function()


        #affichage des images
        pygame_handler.affichage_image()


        #afffichage des boutons
        pygame_widgets.update(events)
        boutons.draw_restart_button_menu(pygame_handler.window, pygame_handler.restart_image)
        boutons.draw_quit_button_menu(pygame_handler.window, pygame_handler.quit_image)
        boutons.draw_podium_button_menu(pygame_handler.window, pygame_handler.podium_image)
        boutons.draw_sound_button_menu(pygame_handler.window, pygame_handler.sound_image)
        boutons.draw_antigravity_button(pygame_handler.window, pygame_handler.antigravity_image)
        boutons.draw_delete_boules(pygame_handler.window, pygame_handler.delete_boule_image)

        #on montre les highscores
        if boutons.podium_visible:
            pygame_handler.highscores_visibles()

        pygame_handler.window.blit(pygame_handler.red_game_over, (0, 0))  # (0,0) sont les coordonnées en haut à gauche


    #gestion de l'ecran de game_over
    else:
        pygame_handler.game_over_screen()
        boutons.draw_restart_button(pygame_handler.window)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                games_state.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if boutons.draw_restart_button(pygame_handler.window).collidepoint(mouse_pos):
                    RestartFunction.restart_game(games_state, pygame_handler, physic_space)  # Redémarrer le jeu si le bouton est cliqué



    clock.tick(60)

    pygame.display.flip()
pygame.quit()