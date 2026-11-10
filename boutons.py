import math
import time
import pygame

podium_visible = False

RESTART_GAMEOVER_RECT = pygame.Rect(490, 560, 220, 52)
RESTART_MENU_RECT = pygame.Rect(20, 20, 44, 44)
QUIT_MENU_RECT = pygame.Rect(80, 20, 44, 44)
PODIUM_MENU_RECT = pygame.Rect(140, 20, 44, 44)
SOUND_MENU_RECT = pygame.Rect(200, 20, 44, 44)

# Barres décalées à x=890 pour éviter tout faux clic près du bord droit de la cuve (x=800)
DELETE_CLICK_ZONE = pygame.Rect(890, 390, 280, 58)
ANTIGRAVITY_CLICK_ZONE = pygame.Rect(890, 475, 280, 58)

DELETE_BOULE_RECT = DELETE_CLICK_ZONE
ANTIGRAVITY_RECT = ANTIGRAVITY_CLICK_ZONE

_font_button = None
_font_bar_title = None
_font_bar_val = None

def _clamp(val):
    return max(0, min(255, int(val)))

def _init_fonts():
    global _font_button, _font_bar_title, _font_bar_val
    if _font_button is None:
        _font_button = pygame.font.SysFont('nirmala ui', 28, bold=True)
        _font_bar_title = pygame.font.SysFont('nirmala ui', 15, bold=True)
        _font_bar_val = pygame.font.SysFont('nirmala ui', 15, bold=True)

def _draw_styled_icon_btn(window, rect, image, active=False, muted=False):
    mouse_pos = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mouse_pos)

    bg_surf = pygame.Surface((rect.width + 8, rect.height + 8), pygame.SRCALPHA)
    if active:
        bg_color = (30, 120, 220, 225)
        border_color = (150, 230, 255)
    else:
        bg_color = (18, 24, 52, 195) if not hovered else (45, 60, 115, 235)
        border_color = (110, 170, 255) if hovered else (65, 90, 155)

    pygame.draw.rect(bg_surf, bg_color, bg_surf.get_rect(), border_radius=12)
    pygame.draw.rect(bg_surf, border_color, bg_surf.get_rect(), width=2, border_radius=12)
    window.blit(bg_surf, (rect.x - 4, rect.y - 4))

    image_rect = image.get_rect(center=rect.center)
    window.blit(image, image_rect)

    if muted:
        pygame.draw.line(window, (255, 75, 75), (rect.left + 7, rect.bottom - 7), (rect.right - 7, rect.top + 7), 3)

    return rect

def draw_integrated_power_bar(
    window, rect, icon_img, title, current_pts, cost_pts, theme_color,
    active=False, active_text="", armed=False
):
    """Barre de progression unique avec icône intégrée et état d'armement anti-missclick."""
    _init_fonts()
    t = time.time()
    mouse_pos = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mouse_pos)
    ratio = min(1.0, max(0.0, current_pts / max(1, cost_pts)))
    ready = (current_pts >= cost_pts) and not active

    surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    w, h = rect.width, rect.height
    radius = h // 2

    # 1. Fond uniforme de la capsule
    bg_alpha = 235 if hovered else 205
    pygame.draw.rect(surf, (14, 20, 44, bg_alpha), (0, 0, w, h), border_radius=radius)

    # 2. Remplissage unique dans la couleur du pouvoir
    if active or armed:
        fill_ratio = 1.0
        fill_col = (
            _clamp(theme_color[0] + 45),
            _clamp(theme_color[1] + 45),
            _clamp(theme_color[2] + 45),
            235
        )
    elif ready:
        fill_ratio = 1.0
        pulse = int(30 * math.sin(t * 7.0))
        fill_col = (
            _clamp(theme_color[0] + 25 + pulse),
            _clamp(theme_color[1] + 25 + pulse),
            _clamp(theme_color[2] + 25 + pulse),
            230
        )
    else:
        fill_ratio = ratio
        fill_col = (
            _clamp(theme_color[0]),
            _clamp(theme_color[1]),
            _clamp(theme_color[2]),
            200
        )

    if fill_ratio > 0.01:
        bar_start_x = radius
        max_bar_w = w - bar_start_x
        fill_w = max(radius, int(max_bar_w * fill_ratio))
        pygame.draw.rect(
            surf, fill_col,
            (bar_start_x, 0, fill_w, h),
            border_top_right_radius=radius,
            border_bottom_right_radius=radius
        )

    # 3. Bordure extérieure
    if active or armed:
        border_col = (255, 235, 110)
        border_w = 3
    elif ready:
        glow = int(45 + 40 * math.sin(t * 8.0))
        border_col = (
            _clamp(theme_color[0] + 70 + glow),
            _clamp(theme_color[1] + 70 + glow),
            _clamp(theme_color[2] + 70 + glow)
        )
        border_w = 3
    else:
        border_col = (
            _clamp(theme_color[0] + (55 if hovered else 15)),
            _clamp(theme_color[1] + (55 if hovered else 15)),
            _clamp(theme_color[2] + (55 if hovered else 15))
        )
        border_w = 2

    pygame.draw.rect(surf, border_col, (0, 0, w, h), width=border_w, border_radius=radius)

    # 4. Médaillon circulaire à gauche intégrant l'icône
    medallion_center = (radius, radius)
    medallion_bg = (
        _clamp(theme_color[0] * 0.35),
        _clamp(theme_color[1] * 0.35),
        _clamp(theme_color[2] * 0.45)
    )
    pygame.draw.circle(surf, medallion_bg, medallion_center, radius - 2)
    pygame.draw.circle(surf, border_col, medallion_center, radius - 2, 2)

    if active or ready or armed:
        angle = math.sin(t * (9.0 if armed else 5.0)) * 10.0
        icon_to_draw = pygame.transform.rotate(icon_img, angle)
    else:
        icon_to_draw = icon_img

    icon_rect = icon_to_draw.get_rect(center=medallion_center)
    surf.blit(icon_to_draw, icon_rect)

    # 5. Textes centrés dans la partie droite
    text_center_x = radius + (w - radius) // 2
    title_surf = _font_bar_title.render(title, True, (225, 235, 255))
    surf.blit(title_surf, title_surf.get_rect(center=(text_center_x, h // 2 - 11)))

    if active:
        status_txt = active_text if active_text else "ACTIF !"
        status_col = (255, 245, 130)
    elif armed:
        status_txt = "RECLIQUEZ POUR ACTIVER"
        status_col = (255, 240, 110)
    elif ready:
        status_txt = f"PRÊT ! ({cost_pts} pts)" if not hovered else "CLIQUER POUR ARMER"
        status_col = (255, 255, 190)
    else:
        status_txt = f"{int(current_pts)} / {cost_pts} pts"
        status_col = (255, 255, 255)

    val_surf = _font_bar_val.render(status_txt, True, status_col)
    surf.blit(val_surf, val_surf.get_rect(center=(text_center_x, h // 2 + 10)))

    window.blit(surf, rect.topleft)
    return rect

def draw_restart_button(window):
    _init_fonts()
    hovered = RESTART_GAMEOVER_RECT.collidepoint(pygame.mouse.get_pos())
    color = (50, 220, 110) if hovered else (30, 185, 85)
    pygame.draw.rect(window, color, RESTART_GAMEOVER_RECT, border_radius=12)
    pygame.draw.rect(window, (220, 255, 230), RESTART_GAMEOVER_RECT, width=2, border_radius=12)

    text = _font_button.render("Rejouer", True, (15, 25, 20))
    text_rect = text.get_rect(center=RESTART_GAMEOVER_RECT.center)
    window.blit(text, text_rect)
    return RESTART_GAMEOVER_RECT

def draw_quit_button_menu(window, quit_image):
    return _draw_styled_icon_btn(window, QUIT_MENU_RECT, quit_image)

def draw_restart_button_menu(window, restart_image):
    return _draw_styled_icon_btn(window, RESTART_MENU_RECT, restart_image)

def draw_podium_button_menu(window, podium_image):
    return _draw_styled_icon_btn(window, PODIUM_MENU_RECT, podium_image, active=podium_visible)

def draw_sound_button_menu(window, sound_image, music_info=True):
    return _draw_styled_icon_btn(window, SOUND_MENU_RECT, sound_image, muted=not music_info)

def toggle_podium():
    global podium_visible
    podium_visible = not podium_visible

def delete_antigravity_lines(space, forme_a_enlever):
    if forme_a_enlever in space.shapes:
        space.remove(forme_a_enlever)