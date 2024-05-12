from boules import Boule1, Boule2, Boule3


def create_planete(window, space, position_x, ball_type):
    if ball_type == 1:
        planete = Boule1(window, (position_x, 650), space)
    elif ball_type == 2:
        planete = Boule2(window, (position_x, 650), space)
    elif ball_type == 3:
        planete = Boule3(window, (position_x, 650), space)
    else:
        planete = 0
    planete.gravite()

def create_preview_ball(window, space, mouse_pos, ball_type):
    if ball_type == 1:
        preview_ball = Boule1(window, (mouse_pos, 50), space)
    elif ball_type == 2:
        preview_ball = Boule2(window, (mouse_pos, 50), space)
    elif ball_type == 3:
        preview_ball = Boule3(window, (mouse_pos, 50), space)
    else:
        preview_ball = 0
    preview_ball.dessin_preview()

def next_ball(window, space, next_ball_type):
    if next_ball_type == 1:
        next_ball = Boule1(window, (1037, 187), space)
    elif next_ball_type == 2:
        next_ball = Boule2(window, (1037, 187), space)
    elif next_ball_type == 3:
        next_ball = Boule3(window, (1037, 187), space)
    else:
        next_ball = 0
    next_ball.dessin_preview()