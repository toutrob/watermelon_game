import math
import random
import time
import pygame
import boutons
from boules import Boules

class PygameStuff:
    pygame.init()
    pygame.mixer.init()

    def __init__(self, game_state):
        self.game_state = game_state
        self.window_size = (1200, 700)
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Watermelon Game")

        self.font_score = pygame.font.SysFont('nirmala ui', 32, bold=True)
        self.font_sub = pygame.font.SysFont('nirmala ui', 18, bold=True)
        self.font_score_menu = pygame.font.SysFont('nirmala ui', 40, bold=True)
        self.font_next_boule = pygame.font.SysFont('nirmala ui', 18, bold=True)
        self.font_end = pygame.font.SysFont('adlam display', 58)
        self.font_delete_boule = pygame.font.SysFont('nirmala ui', 16, bold=True)
        self.font_popup = pygame.font.SysFont('nirmala ui', 24, bold=True)
        self.font_podium_rank = pygame.font.SysFont('nirmala ui', 26, bold=True)
        self.font_podium_score = pygame.font.SysFont('nirmala ui', 22, bold=True)

        self.red_game_over = pygame.Surface(self.window_size)
        self.red_game_over.set_alpha(0)
        self.red_game_over.fill((225, 80, 110))

        self.chamber_glass = pygame.Surface((400, 500), pygame.SRCALPHA)
        self.chamber_glass.fill((10, 14, 36, 90))
        for gx in range(40, 400, 40):
            pygame.draw.line(self.chamber_glass, (70, 120, 210, 18), (gx, 0), (gx, 500), 1)
        for gy in range(40, 500, 40):
            pygame.draw.line(self.chamber_glass, (70, 120, 210, 18), (0, gy), (400, gy), 1)

        self.chamber_stars = [
            [random.uniform(408, 792), random.uniform(155, 645), random.uniform(0.4, 1.4), random.choice([(140, 200, 255), (200, 160, 255), (255, 255, 255)])]
            for _ in range(28)
        ]

        self.particles = []
        self.shockwaves = []
        self.floating_texts = []

        self.background_image = pygame.image.load("espace watermelon game (2).png").convert()
        self.quit_image = pygame.transform.smoothscale(pygame.image.load('exit-run.png').convert_alpha(), (32, 32))
        self.restart_image = pygame.transform.smoothscale(pygame.image.load('restart.png').convert_alpha(), (32, 32))
        self.podium_image = pygame.transform.smoothscale(pygame.image.load('podium.png').convert_alpha(), (32, 32))
        self.sound_image = pygame.transform.smoothscale(pygame.image.load('music_off.png').convert_alpha(), (32, 32))
        self.antigravity_image = pygame.transform.smoothscale(pygame.image.load('pomme.png').convert_alpha(), (34, 34))
        self.delete_boule_image = pygame.transform.smoothscale(
            pygame.image.load('png-clipart-black-hole-car-black-hole-spiral-rim-thumbnail.png').convert_alpha(),
            (34, 34)
        )
        self.image_boules_life_cycle = pygame.image.load('Design_sans_titre__3_-removebg-preview.png').convert_alpha()
        self.life_cycle_rect = self.image_boules_life_cycle.get_rect(center=(200, 415))

        pygame.mixer.music.load('musique_fond.mp3')
        pygame.mixer.music.play(-1)
        self.new_boule1 = pygame.mixer.Sound("nouvelle_boule1.mp3")
        self.new_boule2 = pygame.mixer.Sound("nouvelle_boule2.mp3")
        self.new_boule3 = pygame.mixer.Sound("nouvelle_boule3.mp3")
        self.fusion_boule = pygame.mixer.Sound("fusion_boule.mp3")
        self.red_screen = pygame.mixer.Sound("ecran_rouge.mp3")
        self.game_over_sound = pygame.mixer.Sound("game_over.mp3")
        self.antigravity_sound = pygame.mixer.Sound("antigravity.mp3")
        self.delete_boules_sound = pygame.mixer.Sound("delete_boules.mp3")

    def _draw_panel(self, x, y, w, h, border_color=(90, 120, 200), bg_alpha=185):
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (15, 20, 42, bg_alpha), panel.get_rect(), border_radius=14)
        pygame.draw.rect(panel, border_color, panel.get_rect(), width=2, border_radius=14)
        self.window.blit(panel, (x, y))

    def draw_chamber_backdrop(self):
        self.window.blit(self.chamber_glass, (400, 150))

        antigrav = self.game_state.can_draw_the_gravity_line
        for star in self.chamber_stars:
            if antigrav:
                star[1] -= star[2] * 3.2
                if star[1] < 155:
                    star[1] = 645
                    star[0] = random.uniform(408, 792)
            else:
                star[1] += star[2] * 0.6
                if star[1] > 645:
                    star[1] = 155
                    star[0] = random.uniform(408, 792)

            sx, sy = int(star[0]), int(star[1])
            if antigrav:
                pygame.draw.line(self.window, (100, 240, 255), (sx, sy), (sx, sy + 8), 2)
            else:
                pygame.draw.circle(self.window, star[3], (sx, sy), 2 if star[2] > 0.9 else 1)

    def _draw_plasma_beam(self, p1, p2, outer_col, core_col=(235, 250, 255)):
        pygame.draw.line(self.window, outer_col, p1, p2, 11)
        mid_col = (
            max(0, min(255, (outer_col[0] + core_col[0]) // 2)),
            max(0, min(255, (outer_col[1] + core_col[1]) // 2)),
            max(0, min(255, (outer_col[2] + core_col[2]) // 2))
        )
        pygame.draw.line(self.window, mid_col, p1, p2, 6)
        pygame.draw.line(self.window, core_col, p1, p2, 2)

    def _draw_emitter_node(self, pos, color):
        x, y = pos
        pygame.draw.circle(self.window, (20, 28, 58), (x, y), 10)
        pygame.draw.circle(self.window, color, (x, y), 10, 2)
        pygame.draw.circle(self.window, (240, 250, 255), (x, y), 4)

    def draw_danger_zone_and_balls(self, danger_balls_info):
        """Affiche une barre circulaire continue (sans crans ni chrono) qui tourne dans le sens antihoraire."""
        bar_color = (*Boules.DANGER_SPACE_RED, 220)

        for ball, elapsed in danger_balls_info:
            bx, by = ball.get_screen_pos()
            r = ball.radius
            ratio = min(1.0, max(0.0, elapsed / 3.0))

            ring_r = r + 7
            surf_size = (ring_r + 8) * 2
            bar_surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
            cx, cy = surf_size // 2, surf_size // 2

            steps = max(2, int(90 * ratio))
            points = []
            for i in range(steps + 1):
                t_step = (i / steps) * ratio
                angle = -math.pi / 2 - t_step * math.tau
                px = cx + math.cos(angle) * ring_r
                py = cy + math.sin(angle) * ring_r
                points.append((px, py))

            if len(points) >= 2:
                pygame.draw.lines(bar_surf, bar_color, False, points, 5)
                pygame.draw.circle(bar_surf, bar_color, (int(points[0][0]), int(points[0][1])), 2)
                pygame.draw.circle(bar_surf, bar_color, (int(points[-1][0]), int(points[-1][1])), 2)

            self.window.blit(bar_surf, bar_surf.get_rect(center=(bx, by)))

    def affichage_image(self):
        t = time.time()
        pulse = int(30 * math.sin(t * 4.0))

        if self.game_state.can_draw_the_gravity_line:
            beam_col = (40, 230, 255)
        else:
            beam_col = (
                max(0, min(255, 75 + pulse // 2)),
                max(0, min(255, 135 + pulse)),
                255
            )

        self._draw_plasma_beam((400, 150), (400, 650), beam_col)
        self._draw_plasma_beam((800, 150), (800, 650), beam_col)
        self._draw_plasma_beam((400, 650), (800, 650), beam_col)

        if self.game_state.can_draw_the_gravity_line:
            self._draw_plasma_beam((400, 150), (800, 150), (0, 245, 255))
            pts = [(400, 150)]
            for x in range(425, 800, 25):
                pts.append((x, 150 + random.randint(-5, 5)))
            pts.append((800, 150))
            pygame.draw.lines(self.window, (220, 255, 255), False, pts, 2)

        for corner in [(400, 150), (800, 150), (400, 650), (800, 650)]:
            self._draw_emitter_node(corner, beam_col)

        self.window.blit(self.image_boules_life_cycle, self.life_cycle_rect.topleft)

        self._draw_panel(20, 80, 235, 88)
        score_surf = self.font_score.render(f"Score : {self.game_state.score}", True, (255, 255, 255))
        self.window.blit(score_surf, (35, 88))

        best_score = max([self.game_state.score] + self.game_state.highscores) if self.game_state.highscores else self.game_state.score
        best_surf = self.font_sub.render(f"Record : {best_score}", True, (255, 215, 80))
        self.window.blit(best_surf, (37, 134))

        next_boule = self.font_next_boule.render("NEXT :", True, (20, 30, 55))
        rect_next_boule = next_boule.get_rect(center=(1037, 122))
        self.window.blit(next_boule, rect_next_boule)

    def draw_power_bars(self):
        diff = self.game_state.money_power - self.game_state.display_money_power
        self.game_state.display_money_power += diff * 0.2

        # 1. Trou Noir : Violet Cosmique (150, 45, 245)
        boutons.draw_integrated_power_bar(
            self.window,
            boutons.DELETE_CLICK_ZONE,
            self.delete_boule_image,
            "TROU NOIR",
            self.game_state.display_money_power,
            self.game_state.delete_cost,
            theme_color=(150, 45, 245),
            active=self.game_state.can_delete_a_boule,
            active_text="CIBLEZ UNE PLANÈTE"
        )

        # 2. Antigravité : Bleu Cyan Électrique (0, 150, 255)
        anti_text = ""
        if self.game_state.can_draw_the_gravity_line and self.game_state.time_without_gravity:
            rem = max(0.0, 3.0 - (time.time() - self.game_state.time_without_gravity))
            anti_text = f"ACTIF : {rem:.1f}s"

        is_armed = time.time() < getattr(self.game_state, "antigravity_armed_until", 0.0)

        boutons.draw_integrated_power_bar(
            self.window,
            boutons.ANTIGRAVITY_CLICK_ZONE,
            self.antigravity_image,
            "ANTIGRAVITÉ",
            self.game_state.display_money_power,
            self.game_state.antigravity_cost,
            theme_color=(0, 150, 255),
            active=self.game_state.can_draw_the_gravity_line,
            active_text=anti_text,
            armed=is_armed
        )

    def trigger_merge_vfx(self, x, y, radius, color, points_gained):
        self.shockwaves.append({
            "x": x, "y": y,
            "r": max(8, radius // 2),
            "max_r": radius + 45,
            "color": color,
            "alpha": 230
        })

        count = min(35, 12 + radius // 4)
        for _ in range(count):
            ang = random.uniform(0, math.tau)
            spd = random.uniform(1.8, 6.5)
            self.particles.append({
                "x": float(x), "y": float(y),
                "vx": math.cos(ang) * spd,
                "vy": math.sin(ang) * spd - 1.0,
                "r": random.uniform(2.5, 5.5),
                "color": color,
                "life": 1.0,
                "decay": random.uniform(0.025, 0.045)
            })

        self.floating_texts.append({
            "x": float(x), "y": float(y - radius // 2),
            "text": f"+{points_gained}",
            "color": (255, 245, 150),
            "life": 1.0
        })

    def trigger_blackhole_vfx(self, x, y, radius, color=(185, 75, 255)):
        """Animation de disparition utilisant la couleur de la planète supprimée."""
        self.shockwaves.append({
            "x": x, "y": y,
            "r": radius + 35,
            "max_r": 4,
            "color": color,
            "alpha": 250,
            "implode": True
        })
        for _ in range(28):
            ang = random.uniform(0, math.tau)
            dist = random.uniform(radius * 0.5, radius * 1.45)
            px = x + math.cos(ang) * dist
            py = y + math.sin(ang) * dist
            self.particles.append({
                "x": px, "y": py,
                "vx": (x - px) * 0.08,
                "vy": (y - py) * 0.08,
                "r": random.uniform(3.0, 6.0),
                "color": color,
                "life": 1.0,
                "decay": 0.04
            })

    def update_and_draw_vfx(self):
        for sw in list(self.shockwaves):
            if sw.get("implode"):
                sw["r"] += (sw["max_r"] - sw["r"]) * 0.22
                sw["alpha"] -= 14
            else:
                sw["r"] += (sw["max_r"] - sw["r"]) * 0.18
                sw["alpha"] -= 12

            if sw["alpha"] <= 10:
                self.shockwaves.remove(sw)
                continue

            r_int = max(2, int(sw["r"]))
            sw_surf = pygame.Surface((r_int * 2 + 8, r_int * 2 + 8), pygame.SRCALPHA)
            pygame.draw.circle(sw_surf, (*sw["color"], max(0, min(255, int(sw["alpha"])))), (r_int + 4, r_int + 4), r_int, 3)
            self.window.blit(sw_surf, sw_surf.get_rect(center=(int(sw["x"]), int(sw["y"]))))

        for p in list(self.particles):
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vx"] *= 0.95
            p["vy"] = p["vy"] * 0.95 + 0.08
            p["life"] -= p["decay"]
            if p["life"] <= 0:
                self.particles.remove(p)
                continue

            rad = max(1, int(p["r"] * p["life"]))
            alpha = max(0, min(255, int(255 * p["life"])))
            p_surf = pygame.Surface((rad * 2 + 4, rad * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*p["color"], alpha), (rad + 2, rad + 2), rad)
            self.window.blit(p_surf, (int(p["x"]) - rad, int(p["y"]) - rad))

        for ft in list(self.floating_texts):
            ft["y"] -= 1.3
            ft["life"] -= 0.025
            if ft["life"] <= 0:
                self.floating_texts.remove(ft)
                continue

            txt_surf = self.font_popup.render(ft["text"], True, ft["color"])
            shadow_surf = self.font_popup.render(ft["text"], True, (10, 12, 28))
            alpha = max(0, min(255, int(255 * min(1.0, ft["life"] * 1.4))))
            txt_surf.set_alpha(alpha)
            shadow_surf.set_alpha(alpha)

            pos = txt_surf.get_rect(center=(int(ft["x"]), int(ft["y"])))
            self.window.blit(shadow_surf, (pos.x + 2, pos.y + 2))
            self.window.blit(txt_surf, pos)

    def delete_boule_message(self):
        self._draw_panel(880, 310, 295, 64, border_color=(180, 90, 255))
        msg1 = self.font_delete_boule.render("Cliquez sur une planète à aspirer", True, (255, 255, 255))
        msg2 = self.font_delete_boule.render("(Clic droit ou barre : Annuler)", True, (215, 185, 255))
        self.window.blit(msg1, msg1.get_rect(center=(1027, 330)))
        self.window.blit(msg2, msg2.get_rect(center=(1027, 353)))

    def draw_pause_overlay(self):
        overlay = pygame.Surface(self.window_size, pygame.SRCALPHA)
        overlay.fill((8, 12, 28, 195))
        self.window.blit(overlay, (0, 0))

        self._draw_panel(380, 250, 440, 190, border_color=(100, 180, 255), bg_alpha=240)
        title = self.font_score_menu.render("JEU EN PAUSE", True, (255, 255, 255))
        sub = self.font_sub.render("Cliquez sur la fenêtre ou appuyez sur P pour reprendre", True, (180, 215, 255))
        self.window.blit(title, title.get_rect(center=(600, 315)))
        self.window.blit(sub, sub.get_rect(center=(600, 375)))

    def _draw_podium_and_list(self, center_x, podium_bottom_y, step_scale=1.0):
        """Dessine un podium visuel pour le Top 3 (2e à gauche, 1er au centre, 3e à droite) + liste 4e et 5e."""
        scores = list(self.game_state.highscores[:5])
        while len(scores) < 5:
            scores.append(0)

        step_w = 128
        gap = 14
        # Configuration : (index_score, rang, x_centre, hauteur, couleur_principale, couleur_fond)
        podium_steps = [
            (1, 2, center_x - step_w - gap, int(92 * step_scale),  (195, 210, 230), (45, 58, 88, 215)),   # 2e (Argent)
            (0, 1, center_x,                int(128 * step_scale), (255, 215, 55),  (75, 60, 20, 225)),   # 1er (Or)
            (2, 3, center_x + step_w + gap, int(68 * step_scale),  (230, 145, 85),  (70, 42, 28, 215)),   # 3e (Bronze)
        ]

        for idx, rank, cx, h, main_col, bg_col in podium_steps:
            step_rect = pygame.Rect(cx - step_w // 2, podium_bottom_y - h, step_w, h)

            # Colonne du podium
            step_surf = pygame.Surface((step_w, h), pygame.SRCALPHA)
            pygame.draw.rect(step_surf, bg_col, (0, 0, step_w, h), border_top_left_radius=12, border_top_right_radius=12)
            pygame.draw.rect(
                step_surf, main_col, (0, 0, step_w, h),
                width=3 if rank == 1 else 2,
                border_top_left_radius=12, border_top_right_radius=12
            )
            self.window.blit(step_surf, step_rect.topleft)

            # Médaille du rang (1, 2, 3) sur la marche
            medal_y = step_rect.top + 26
            pygame.draw.circle(self.window, (20, 26, 48), (cx, medal_y), 17)
            pygame.draw.circle(self.window, main_col, (cx, medal_y), 17, 2)
            rank_surf = self.font_podium_rank.render(str(rank), True, main_col)
            self.window.blit(rank_surf, rank_surf.get_rect(center=(cx, medal_y)))

            # Score affiché au-dessus de la marche
            score_txt = f"{scores[idx]} pts"
            score_surf = self.font_podium_score.render(score_txt, True, main_col if rank == 1 else (240, 245, 255))
            self.window.blit(score_surf, score_surf.get_rect(center=(cx, step_rect.top - 18)))

        # Socle lumineux sous le podium
        total_w = step_w * 3 + gap * 2 + 20
        pygame.draw.line(
            self.window, (120, 165, 240),
            (center_x - total_w // 2, podium_bottom_y),
            (center_x + total_w // 2, podium_bottom_y), 3
        )

        # Liste classique en dessous pour les 4e et 5e places
        list_start_y = podium_bottom_y + 20
        row_w = 380
        row_h = 38
        for idx in range(3, 5):
            y_pos = list_start_y + (idx - 3) * (row_h + 10)
            row_rect = pygame.Rect(center_x - row_w // 2, y_pos, row_w, row_h)

            row_surf = pygame.Surface((row_w, row_h), pygame.SRCALPHA)
            pygame.draw.rect(row_surf, (24, 32, 64, 195), (0, 0, row_w, row_h), border_radius=10)
            pygame.draw.rect(row_surf, (75, 105, 170), (0, 0, row_w, row_h), width=1, border_radius=10)
            self.window.blit(row_surf, row_rect.topleft)

            rank_lbl = self.font_sub.render(f"#{idx + 1}", True, (165, 190, 235))
            val_lbl = self.font_sub.render(f"{scores[idx]} pts", True, (240, 245, 255))
            self.window.blit(rank_lbl, rank_lbl.get_rect(midleft=(row_rect.left + 22, row_rect.centery)))
            self.window.blit(val_lbl, val_lbl.get_rect(midright=(row_rect.right - 22, row_rect.centery)))

    def highscores_visibles(self):
        self._draw_panel(290, 80, 620, 520, border_color=(255, 215, 90), bg_alpha=240)
        title = self.font_score_menu.render("MEILLEURS SCORES", True, (255, 215, 90))
        self.window.blit(title, title.get_rect(center=(600, 135)))

        self._draw_podium_and_list(center_x=600, podium_bottom_y=415, step_scale=1.0)

    def game_over_screen(self):
        self.red_screen.stop()
        self.game_state.red_screen_playing = False
        if not self.game_state.game_over_sound_played:
            self.game_over_sound.play()
            self.game_state.game_over_sound_played = True

        overlay = pygame.Surface(self.window_size, pygame.SRCALPHA)
        overlay.fill((8, 10, 24, 215))
        self.window.blit(overlay, (0, 0))

        self._draw_panel(290, 55, 620, 585, border_color=(255, 80, 60), bg_alpha=240)

        msg = self.font_end.render("GAME OVER", True, (255, 70, 50))
        self.window.blit(msg, msg.get_rect(center=(600, 110)))

        score_surf = self.font_score.render(f"Score final : {self.game_state.score}", True, (255, 255, 255))
        self.window.blit(score_surf, score_surf.get_rect(center=(600, 172)))

        self._draw_podium_and_list(center_x=600, podium_bottom_y=410, step_scale=0.9)