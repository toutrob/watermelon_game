import boules
from boules import Boule2, Boule3, Boule4, Boule5, Boule6, Boule7, Boule8, Boule9, Boule10, Boule11


#ce fichier stock la fonction qui se déroule au moment de la collision entre deux boules de mêmes types

def collision_callback(arbiter, space, data, window,game_state, pygame_handler):
    # Récupère les informations sur les objets en collision
    shape1, shape2 = arbiter.shapes

    #on défini le type de la prochaine boule créer
    new_shape_type = shape1.collision_type + 1

    #définition des points de contact des deux boules
    contact_x = 0
    contact_y = 0


    points = arbiter.contact_point_set.points
    for point in points:
        # Accède aux coordonnées du point de contact
        contact_x, contact_y = point.point_a

    #on recupere le centre des boules "physique" qui rentre en contact
    center_shape1 = shape1.body.position
    center_shape2 = shape2.body.position

    #création de 2 constantes pour trouver quel cercle OBJET boule doit être supprimé
    i = 0
    j = 0

    #On traverse la liste contenant tous les objets Boules
    for bouboules in boules.Boules.instances:

        #on regarde si chaque Objets Boules a unn centre en commun avec la première boule à détruire
        if bouboules.find_center() == center_shape1:
            #Si c'est le cas on détruit l'objet Boules
            #sinon on incrémente i dans le else
            del boules.Boules.instances[i]

            # une fois la 1ere boule detruite
            # on regarde si chaque Objets Boules a unn centre en commun avec la seconde boule à détruire

            for bouboules2 in boules.Boules.instances:

                if bouboules2.find_center() == center_shape2:
                    # Si c'est le cas on détruit l'objet Boules

                    del boules.Boules.instances[j]

                j += 1



        else:
            boule_a_supprimer1 = None
            boule_a_supprimer2 = None

        i += 1

    #on détruit ensuite les boules de l'espace physique
    space.remove(shape1, shape1.body)
    space.remove(shape2, shape2.body)

    #on joue le son de fusion des boules
    pygame_handler.fusion_boule.play()


    #Pour chaque type de boules, on créé une boule du type attendu
    #on incrémente le score et la monnaie de pouvoir
    if new_shape_type == 6:
        planet = Boule2(window, (contact_x, contact_y), space)
        planet.gravity()
        game_state.score += 1
        game_state.money_power += 1

    elif new_shape_type == 7:
        planet = Boule3(window, (contact_x, contact_y), space)
        planet.gravity()
        game_state.score += 3
        game_state.money_power += 3

    elif new_shape_type == 8:
        planet = Boule4(window, (contact_x, contact_y), space)
        planet.gravity()
        game_state.score += 6
        game_state.money_power += 6

    elif new_shape_type == 9:
        planet = Boule5(window, (contact_x, contact_y), space)
        planet.gravity()
        game_state.score += 10
        game_state.money_power += 10

    elif new_shape_type == 10:
        planet = Boule6(window, (contact_x, contact_y), space)
        planet.gravity()
        game_state.score += 15
        game_state.money_power += 15

    elif new_shape_type == 11:
        planet = Boule7(window, (contact_x, contact_y), space)
        planet.gravity()
        game_state.score += 21
        game_state.money_power += 21

    elif new_shape_type == 12:
        planet = Boule8(window, (contact_x, contact_y), space)
        planet.gravity()
        game_state.score += 28
        game_state.money_power += 28

    elif new_shape_type == 13:
        planet = Boule9(window, (contact_x, contact_y), space)
        planet.gravity()
        game_state.score += 36
        game_state.money_power += 36

    elif new_shape_type == 14:
        planet = Boule10(window, (contact_x, contact_y), space)
        planet.gravity()
        game_state.score += 45
        game_state.money_power += 45

    elif new_shape_type == 15:
        planet = Boule11(window, (contact_x, contact_y), space)
        planet.gravity()
        game_state.score += 55
        game_state.money_power += 55
    else:
        game_state.score += 66
        game_state.money_power += 66

    #on oublie pas de changer l'affichage du score a faire à l'écran
    game_state.texte = f"Score : {game_state.score}"

    return True  # Retourne True pour permettre à la collision de se produire