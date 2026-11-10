import random
import time
import high_score

class GameState:
    BASE_ANTIGRAVITY_COST = 500
    BASE_DELETE_COST = 900

    def __init__(self):
        self.score = 0
        self.texte = f"Score : {self.score}"

        self.money_power = 0
        self.display_money_power = 0.0
        self.antigravity_cost = self.BASE_ANTIGRAVITY_COST
        self.delete_cost = self.BASE_DELETE_COST
        self.antigravity_armed_until = 0.0  # Sécurité anti-missclick

        self.highscores = high_score.load_highscores()
        self.game_over = False
        self.game_over_sound_played = False
        self.paused = False

        self.can_draw_the_gravity_line = False
        self.can_delete_a_boule = False
        self.red_screen_playing = False
        self.red_overlay_alpha = 0.0

        self.selected_ball_type = self.pick_random_ball()
        self.next_selected_ball_type = self.pick_random_ball()
        self.next_ball_anim_time = time.time()
        self.next_Bouboule = True

        self.time_without_gravity = None
        self.running = True
        self.can_create_planete = True
        self.music_info = True
        self.time_elapsed = {}

    def pick_random_ball(self):
        if self.score >= 250:
            return random.choices([1, 2, 3, 4, 5], weights=[32, 28, 20, 13, 7], k=1)[0]
        elif self.score >= 80:
            return random.choices([1, 2, 3, 4], weights=[38, 30, 20, 12], k=1)[0]
        return random.choices([1, 2, 3], weights=[45, 35, 20], k=1)[0]