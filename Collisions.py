import boules
from boules import Boule2, Boule3, Boule4, Boule5, Boule6, Boule7, Boule8, Boule9, Boule10, Boule11
import pygame



def collision_callback(arbiter, space, data, window,etat_du_jeu):
    # Récupère les informations sur les objets en collision
    shape1, shape2 = arbiter.shapes
    new_shape_type = shape1.collision_type + 1

    contact_x = 0
    contact_y = 0

    points = arbiter.contact_point_set.points
    for point in points:
        # Accède aux coordonnées du point de contact
        contact_x, contact_y = point.point_a

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
            boule_a_supprimer1 = None
            boule_a_supprimer2 = None

        i += 1

    space.remove(shape1, shape1.body)
    space.remove(shape2, shape2.body)

    #fusion_boule.play()

    if new_shape_type == 6:
        planete = Boule2(window, (contact_x, contact_y), space)
        planete.gravite()
        etat_du_jeu.score += 1
        etat_du_jeu.money_pouvoir += 1

    elif new_shape_type == 7:
        planete = Boule3(window, (contact_x, contact_y), space)
        planete.gravite()
        etat_du_jeu.score += 3
        etat_du_jeu.money_pouvoir += 3

    elif new_shape_type == 8:
        planete = Boule4(window, (contact_x, contact_y), space)
        planete.gravite()
        etat_du_jeu.score += 6
        etat_du_jeu.money_pouvoir += 6

    elif new_shape_type == 9:
        planete = Boule5(window, (contact_x, contact_y), space)
        planete.gravite()
        etat_du_jeu.score += 10
        etat_du_jeu.money_pouvoir += 10

    elif new_shape_type == 10:
        planete = Boule6(window, (contact_x, contact_y), space)
        planete.gravite()
        etat_du_jeu.score += 15
        etat_du_jeu.money_pouvoir += 15

    elif new_shape_type == 11:
        planete = Boule7(window, (contact_x, contact_y), space)
        planete.gravite()
        etat_du_jeu.score += 21
        etat_du_jeu.money_pouvoir += 21

    elif new_shape_type == 12:
        planete = Boule8(window, (contact_x, contact_y), space)
        planete.gravite()
        etat_du_jeu.score += 28
        etat_du_jeu.money_pouvoir += 28

    elif new_shape_type == 13:
        planete = Boule9(window, (contact_x, contact_y), space)
        planete.gravite()
        etat_du_jeu.score += 36
        etat_du_jeu.money_pouvoir += 36

    elif new_shape_type == 14:
        planete = Boule10(window, (contact_x, contact_y), space)
        planete.gravite()
        etat_du_jeu.score += 45
        etat_du_jeu.money_pouvoir += 45

    elif new_shape_type == 15:
        planete = Boule11(window, (contact_x, contact_y), space)
        planete.gravite()
        etat_du_jeu.score += 55
        etat_du_jeu.money_pouvoir += 55
    else:
        etat_du_jeu.score += 66
        etat_du_jeu.money_pouvoir += 66

    etat_du_jeu.texte = f"Score : {etat_du_jeu.score}"

    return True  # Retourne True pour permettre à la collision de se produire