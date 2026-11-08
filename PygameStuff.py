import time
import pygame
from pygame_widgets.progressbar import ProgressBar

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
        self.font_score_menu = pygame.font.SysFont('nirmala ui', 42, bold=True)
        self.font_next_boule = pygame.font.SysFont('nirmala ui', 18, bold=True)
        self.font_end = pygame.font.SysFont('adlam display', 64)
        self.font_delete_boule = pygame.font.SysFont('nirmala ui', 16, bold=True)

        self.red_game_over = pygame.Surface(self.window_size)
        self.red_game_over.set_alpha(0)
        self.red_game_over.fill((255, 0, 0))

        # Barres de progression avec coût dynamique
        self.progressBar = ProgressBar(
            self.window, 930, 500, 190, 40,
            lambda: min(1.0, max(0.0, game_state.money_power / max(1, game_state.antigravity_cost))),
            completedColour=(0, 140, 255), incompletedColour=(35, 45, 75), curved=True
        )
        self.progressBar2 = ProgressBar(
            self.window, 930, 400, 190, 40,
            lambda: min(1.0, max(0.0, game_state.money_power / max(1, game_state.delete_cost))),
            completedColour=(140, 70, 255), incompletedColour=(35, 45, 75), curved=True
        )

        # Images mises en cache
        self.background_image = pygame.image.load("espace watermelon game (2).png").convert()
        self.quit_image = pygame.transform.smoothscale(pygame.image.load('exit-run.png').convert_alpha(), (34, 34))
        self.restart_image = pygame.transform.smoothscale(pygame.image.load('restart.png').convert_alpha(), (34, 34))
        self.podium_image = pygame.transform.smoothscale(pygame.image.load('podium.png').convert_alpha(), (34, 34))
        self.sound_image = pygame.transform.smoothscale(pygame.image.load('music_off.png').convert_alpha(), (34, 34))
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

    def affichage_image(self):
        # Les 3 lignes blanches d'origine de la cuve
        pygame.draw.line(self.window, (255, 255, 255), (400, 150), (400, 650), 7)
        pygame.draw.line(self.window, (255, 255, 255), (800, 150), (800, 650), 7)
        pygame.draw.line(self.window, (255, 255, 255), (400, 650), (800, 650), 7)

        # Cycle des planètes
        self.window.blit(self.image_boules_life_cycle, self.life_cycle_rect.topleft)

        # Panneau Score & Record (en haut à gauche)
        self._draw_panel(20, 80, 230, 88)
        score_surf = self.font_score.render(f"Score : {self.game_state.score}", True, (255, 255, 255))
        self.window.blit(score_surf, (35, 88))

        best_score = max([self.game_state.score] + self.game_state.highscores) if self.game_state.highscores else self.game_state.score
        best_surf = self.font_sub.render(f"Record : {best_score}", True, (255, 215, 80))
        self.window.blit(best_surf, (37, 134))

        # Texte "NEXT :" sur la soucoupe
        next_boule = self.font_next_boule.render("NEXT :", True, (0, 0, 0))
        rect_next_boule = next_boule.get_rect(center=(1037, 122))
        self.window.blit(next_boule, rect_next_boule)

    def draw_power_overlays(self):
        # Titres et compteurs par-dessus les barres de pouvoirs
        # 1. Trou Noir (y = 400)
        del_cost = self.game_state.delete_cost
        cur_pow = self.game_state.money_power
        lbl_del = self.font_sub.render("TROU NOIR", True, (210, 180, 255))
        self.window.blit(lbl_del, (935, 376))

        if self.game_state.can_delete_a_boule:
            txt_del = "CLIQUEZ SUR UNE BOULE"
            col_del = (255, 230, 100)
        elif cur_pow >= del_cost:
            txt_del = f"PRÊT ! ({del_cost} pts)"
            col_del = (120, 255, 160)
        else:
            txt_del = f"{cur_pow} / {del_cost} pts"
            col_del = (255, 255, 255)

        surf_del = self.font_sub.render(txt_del, True, col_del)
        self.window.blit(surf_del, surf_del.get_rect(center=(1025, 420)))

        # 2. Antigravité (y = 500)
        anti_cost = self.game_state.antigravity_cost
        lbl_anti = self.font_sub.render("ANTIGRAVITÉ", True, (160, 220, 255))
        self.window.blit(lbl_anti, (935, 476))

        if self.game_state.can_draw_the_gravity_line and self.game_state.time_without_gravity:
            rem = max(0.0, 3.0 - (time.time() - self.game_state.time_without_gravity))
            txt_anti = f"ACTIF : {rem:.1f}s"
            col_anti = (120, 255, 255)
        elif cur_pow >= anti_cost:
            txt_anti = f"PRÊT ! ({anti_cost} pts)"
            col_anti = (120, 255, 160)
        else:
            txt_anti = f"{cur_pow} / {anti_cost} pts"
            col_anti = (255, 255, 255)

        surf_anti = self.font_sub.render(txt_anti, True, col_anti)
        self.window.blit(surf_anti, surf_anti.get_rect(center=(1025, 520)))

    def delete_boule_message(self):
        self._draw_panel(855, 305, 325, 62, border_color=(180, 90, 255))
        msg1 = self.font_delete_boule.render("Ciblez une planète à supprimer", True, (255, 255, 255))
        msg2 = self.font_delete_boule.render("(Clic droit ou icône : Annuler)", True, (200, 180, 255))
        self.window.blit(msg1, msg1.get_rect(center=(1017, 325)))
        self.window.blit(msg2, msg2.get_rect(center=(1017, 348)))

    def highscores_visibles(self):
        self._draw_panel(320, 90, 560, 520, border_color=(255, 215, 90), bg_alpha=235)
        title = self.font_score_menu.render("MEILLEURS SCORES", True, (255, 215, 90))
        self.window.blit(title, title.get_rect(center=(600, 155)))

        colors = [(255, 215, 0), (210, 215, 225), (225, 145, 85), (255, 255, 255), (200, 200, 220)]
        for i, highscore in enumerate(self.game_state.highscores[:5]):
            c = colors[i] if i < len(colors) else (255, 255, 255)
            row_surf = self.font_score.render(f"#{i + 1}    {highscore} pts", True, c)
            self.window.blit(row_surf, row_surf.get_rect(center=(600, 245 + i * 65)))

    def game_over_screen(self):
        self.red_screen.stop()
        self.game_state.red_screen_playing = False
        if not self.game_state.game_over_sound_played:
            self.game_over_sound.play()
            self.game_state.game_over_sound_played = True

        overlay = pygame.Surface(self.window_size, pygame.SRCALPHA)
        overlay.fill((8, 10, 24, 215))
        self.window.blit(overlay, (0, 0))

        self._draw_panel(310, 70, 580, 570, border_color=(255, 80, 60), bg_alpha=235)

        msg = self.font_end.render("GAME OVER", True, (255, 70, 50))
        self.window.blit(msg, msg.get_rect(center=(600, 140)))

        score_surf = self.font_score.render(f"Score final : {self.game_state.score}", True, (255, 255, 255))
        self.window.blit(score_surf, score_surf.get_rect(center=(600, 215)))

        top_title = self.font_sub.render("TOP 5 MEILLEURS SCORES", True, (255, 215, 90))
        self.window.blit(top_title, top_title.get_rect(center=(600, 275)))

        for i, highscore in enumerate(self.game_state.highscores[:5]):
            hs_surf = self.font_sub.render(f"{i + 1}.   {highscore} pts", True, (220, 230, 255))
            self.window.blit(hs_surf, hs_surf.get_rect(center=(600, 320 + i * 42)))