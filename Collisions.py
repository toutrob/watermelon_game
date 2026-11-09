import math
import time
from boules import BALL_CLASSES, Boules

RECOMPENSES_FUSION = {
    6:  (1,  1),
    7:  (3,  3),
    8:  (6,  6),
    9:  (10, 10),
    10: (15, 15),
    11: (21, 21),
    12: (28, 28),
    13: (36, 36),
    14: (45, 45),
    15: (55, 55),
}

def collision_callback(arbiter, space, data, window, game_state, pygame_handler):
    shape1, shape2 = arbiter.shapes
    ball1 = getattr(shape1, "ball", None)
    ball2 = getattr(shape2, "ball", None)

    if ball1 is None or ball2 is None or ball1.merged or ball2.merged:
        return False

    ball1.merged = True
    ball2.merged = True

    new_shape_type = shape1.collision_type + 1
    pos1 = shape1.body.position
    pos2 = shape2.body.position
    mid_x = (pos1.x + pos2.x) / 2.0
    mid_y = (pos1.y + pos2.y) / 2.0

    # Si l'une des deux boules était déjà en alerte de dépassement, on conserve son ancienneté !
    inherited_alert_time = None
    t1 = game_state.time_elapsed.get(shape1.body)
    t2 = game_state.time_elapsed.get(shape2.body)
    if t1 is not None and t2 is not None:
        inherited_alert_time = min(t1, t2)
    elif t1 is not None:
        inherited_alert_time = t1
    elif t2 is not None:
        inherited_alert_time = t2

    def post_step_merge(space_obj, key):
        game_state.time_elapsed.pop(shape1.body, None)
        game_state.time_elapsed.pop(shape2.body, None)

        if ball1 in Boules.instances:
            Boules.instances.remove(ball1)
        if ball2 in Boules.instances:
            Boules.instances.remove(ball2)

        if shape1 in space_obj.shapes:
            space_obj.remove(shape1, shape1.body)
        if shape2 in space_obj.shapes:
            space_obj.remove(shape2, shape2.body)

        pygame_handler.fusion_boule.play()

        gain_score, gain_power = RECOMPENSES_FUSION.get(new_shape_type, (66, 66))
        game_state.score += gain_score
        game_state.money_power += gain_power
        game_state.texte = f"Score : {game_state.score}"

        if new_shape_type in BALL_CLASSES:
            cfg = Boules.BALL_CONFIG[new_shape_type]
            new_radius = cfg[0]
            effect_color = cfg[4]

            spawn_x = max(400 + new_radius + 3, min(800 - new_radius - 3, mid_x))
            spawn_y = max(53 + new_radius + 3, mid_y)

            if game_state.can_draw_the_gravity_line:
                spawn_y = min(550 - new_radius - 4, spawn_y)

            planet_cls = BALL_CLASSES[new_shape_type]
            planet = planet_cls(window, (spawn_x, spawn_y), space_obj, is_merge=True)
            planet.gravity()

            # Si la fusion a lieu au-dessus de la ligne haute, elle n'annule pas le chrono d'alerte
            if inherited_alert_time is not None and (spawn_y + new_radius * 0.4 > 550):
                planet.spawn_time = time.time() - 1.0
                game_state.time_elapsed[planet.center_masque] = inherited_alert_time

            screen_x = int(spawn_x)
            screen_y = 700 - int(spawn_y)
            pygame_handler.trigger_merge_vfx(screen_x, screen_y, new_radius, effect_color, gain_score)

            for other in Boules.instances:
                if other is not planet:
                    dx = other.center_masque.position.x - spawn_x
                    dy = other.center_masque.position.y - spawn_y
                    dist = math.hypot(dx, dy)
                    reach = new_radius + other.radius + 30
                    if 0 < dist < reach:
                        push = (1.0 - dist / reach) * 75
                        vx, vy = other.center_masque.velocity
                        other.center_masque.velocity = (
                            vx + (dx / dist) * push,
                            vy + (dy / dist) * push * 0.5
                        )
        else:
            screen_x = int(mid_x)
            screen_y = 700 - int(mid_y)
            pygame_handler.trigger_merge_vfx(screen_x, screen_y, 140, (253, 195, 45), gain_score)

    space.add_post_step_callback(post_step_merge, (shape1, shape2))
    return False