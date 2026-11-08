import pygame

podium_visible = False

RESTART_GAMEOVER_RECT = pygame.Rect(490, 560, 220, 52)
RESTART_MENU_RECT = pygame.Rect(20, 20, 44, 44)
QUIT_MENU_RECT = pygame.Rect(80, 20, 44, 44)
PODIUM_MENU_RECT = pygame.Rect(140, 20, 44, 44)
SOUND_MENU_RECT = pygame.Rect(200, 20, 44, 44)

DELETE_BOULE_RECT = pygame.Rect(880, 400, 40, 40)
ANTIGRAVITY_RECT = pygame.Rect(880, 500, 40, 40)

DELETE_CLICK_ZONE = pygame.Rect(880, 400, 220, 40)
ANTIGRAVITY_CLICK_ZONE = pygame.Rect(880, 500, 220, 40)

_font_button = None

def _draw_styled_icon_btn(window, rect, image, active=False, ready=False, muted=False):
    mouse_pos = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mouse_pos)

    bg_surf = pygame.Surface((rect.width + 8, rect.height + 8), pygame.SRCALPHA)
    if active:
        bg_color = (160, 60, 255, 210)
        border_color = (230, 180, 255)
    elif ready:
        bg_color = (20, 160, 110, 190) if not hovered else (40, 200, 140, 230)
        border_color = (100, 255, 180)
    else:
        bg_color = (25, 30, 55, 180) if not hovered else (55, 65, 110, 220)
        border_color = (120, 140, 200) if hovered else (70, 85, 130)

    pygame.draw.rect(bg_surf, bg_color, bg_surf.get_rect(), border_radius=10)
    pygame.draw.rect(bg_surf, border_color, bg_surf.get_rect(), width=2, border_radius=10)
    window.blit(bg_surf, (rect.x - 4, rect.y - 4))

    image_rect = image.get_rect(center=rect.center)
    window.blit(image, image_rect)

    # Trait rouge si le son est coupé
    if muted:
        pygame.draw.line(window, (255, 70, 70), (rect.left + 6, rect.bottom - 6), (rect.right - 6, rect.top + 6), 3)

    return rect

def draw_restart_button(window):
    global _font_button
    if _font_button is None:
        _font_button = pygame.font.SysFont('nirmala ui', 28, bold=True)

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

def draw_antigravity_button(window, antigravity_image, ready=False, active=False):
    return _draw_styled_icon_btn(window, ANTIGRAVITY_RECT, antigravity_image, active=active, ready=ready)

def draw_delete_boules(window, delete_boule_image, ready=False, active=False):
    return _draw_styled_icon_btn(window, DELETE_BOULE_RECT, delete_boule_image, active=active, ready=ready)

def toggle_podium():
    global podium_visible
    podium_visible = not podium_visible

def delete_antigravity_lines(space, forme_a_enlever):
    if forme_a_enlever in space.shapes:
        space.remove(forme_a_enlever)