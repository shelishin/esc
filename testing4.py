import pygame
import random
import math
import os
import sys
import journal123

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1024, 576
VIRTUAL_WORLD_SIZE = 5000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Echo Sketch: Energetic Flow")
clock = pygame.time.Clock()

canvas = pygame.Surface((VIRTUAL_WORLD_SIZE, VIRTUAL_WORLD_SIZE), pygame.SRCALPHA)
canvas.fill((0, 0, 0, 0))

PARALLAX_FACTOR = 0.3
TRAIL_ALPHA = 160

font_large  = pygame.font.SysFont("Courier New", 48, bold=True)
font_medium = pygame.font.SysFont("Courier New", 30, bold=True)
font_small  = pygame.font.SysFont("Courier New", 22)
font_tiny   = pygame.font.SysFont("Courier New", 18)

# ---------------- COLORS ----------------
COL_BG = (10, 10, 25)
COL_WHITE = (255, 255, 255)
COL_PINK = (255, 100, 200)
COL_BLUE = (100, 180, 255)
COL_YELLOW = (255, 230, 100)
CYAN = (120, 255, 255)

JOURNAL_MESSAGES = ["A spark of energy...", "Movement is life...", "Capturing the flow...", "Clarity in speed..."]

# ---------------- HELPERS ----------------
def wrapping_dist(ax, ay, bx, by):
    dx, dy = ax - bx, ay - by
    if dx > VIRTUAL_WORLD_SIZE / 2: dx -= VIRTUAL_WORLD_SIZE
    if dx < -VIRTUAL_WORLD_SIZE / 2: dx += VIRTUAL_WORLD_SIZE
    if dy > VIRTUAL_WORLD_SIZE / 2: dy -= VIRTUAL_WORLD_SIZE
    if dy < -VIRTUAL_WORLD_SIZE / 2: dy += VIRTUAL_WORLD_SIZE
    return math.hypot(dx, dy)


def screen_pos(wx, wy, scroll_x, scroll_y):
    sx = (wx - scroll_x) % VIRTUAL_WORLD_SIZE
    sy = (wy - scroll_y) % VIRTUAL_WORLD_SIZE
    return sx, sy


# ---------------- CLASSES (UNCHANGED) ----------------
class TinyPlanet:
    def __init__(self, color):
        self.x = self.y = VIRTUAL_WORLD_SIZE // 2
        self.color = list(color)
        self.target_color = list(color)
        self.radius = 14
        self.extra_radius = 0
        self.boost_timer = 0

    def update(self, target_wx, target_wy):
        self.x += (target_wx - self.x) * 0.06
        self.y += (target_wy - self.y) * 0.06

    def draw(self, surface, scroll_x, scroll_y):
        bx, by = screen_pos(self.x, self.y, scroll_x, scroll_y)
        pygame.draw.circle(surface, self.color, (int(bx), int(by)), self.radius)


class Cloud:
    def __init__(self, type_id):
        self.x = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.y = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.type_id = type_id
        self.color = COL_BLUE if type_id == 1 else COL_PINK

    def update(self):
        pass

    def draw(self, surface, scroll_x, scroll_y):
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        pygame.draw.circle(surface, self.color, (int(sx), int(sy)), 40)


class Asteroid:
    def __init__(self):
        self.x = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.y = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.radius = random.randint(18, 35)
        self.active = True

    def draw(self, surface, scroll_x, scroll_y):
        if not self.active:
            return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        pygame.draw.circle(surface, (130, 120, 110), (int(sx), int(sy)), self.radius)


class InspirationSymbol:
    def __init__(self, sym_type):
        self.x = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.y = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.type = sym_type
        self.collected = False

    def update(self):
        pass

    def draw(self, surface, scroll_x, scroll_y):
        if self.collected:
            return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        col = COL_PINK if self.type == "note" else COL_YELLOW
        pygame.draw.circle(surface, col, (int(sx), int(sy)), 20)


# ---------------- RESET ----------------
def reset_game():
    global player, asteroids, clouds, notes, journals, all_symbols
    global scroll_x, scroll_y, score, journal_text, constellation_positions
    global journal_msg, journal_timer

    canvas.fill((0, 0, 0, 0))

    player = TinyPlanet(COL_YELLOW)
    asteroids = [Asteroid() for _ in range(50)]
    clouds = [Cloud(random.choice([1, 2])) for _ in range(30)]
    notes = [InspirationSymbol("note") for _ in range(12)]
    journals = [InspirationSymbol("journal") for _ in range(5)]
    all_symbols = notes + journals

    for s in all_symbols:
        s.collected = False    

    scroll_x = scroll_y = 0
    score = 0
    journal_text = ""
    constellation_positions = []
    journal_msg = ""
    journal_timer = 0
    game_state = "MENU"

reset_game()
# game_state = "MENU"
global journal_locked
journal_locked = False
running = True
# /JOURNAL
# ================= MAIN LOOP =================
while running:

    mx, my = pygame.mouse.get_pos()
    mouse_clicked = False

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True

        elif event.type == pygame.KEYDOWN:

            if game_state == "MENU" and event.key == pygame.K_SPACE:
                game_state = "PLAYING"

            elif event.key == pygame.K_r:
                reset_game()
                game_state = "MENU"
# scroll_x
            elif event.key == pygame.K_e and game_state == "PLAYING":
                game_state = "SUMMARY"

            elif game_state == "JOURNAL":
                if event.key == pygame.K_BACKSPACE:
                    journal_text = journal_text[:-1]
                elif event.key == pygame.K_RETURN:
                    game_state = "SUMMARY"
                else:
                    journal_text += event.unicode

    # -------- PLAYING UPDATE (FIXED LOCATION) --------
    if game_state == "PLAYING":

        player.update(mx + scroll_x, my + scroll_y)
        scroll_x, scroll_y = player.x - WIDTH // 2, player.y - HEIGHT // 2

        for c in clouds:
            c.update()
            if wrapping_dist(player.x, player.y, c.x, c.y) < 100:
                player.target_color = list(c.color)

        for a in asteroids:
            if a.active and wrapping_dist(player.x, player.y, a.x, a.y) < a.radius + player.radius:
                a.active = False

        for sym in all_symbols:
            sym.update()

            if not sym.collected and wrapping_dist(player.x, player.y, sym.x, sym.y) < 50:
                sym.collected = True
                score += 15

                if not journal_locked and all(s.collected for s in all_symbols):
                    journal_locked = True
                    game_state = "JOURNAL"

                # if all(s.collected for s in all_symbols):
                #     game_state = "JOURNAL"
                # reset_game
            
    # -------- JOURNAL STATE (FIXED POSITION) --------
    elif game_state == "JOURNAL":
        result = journal123.run(screen, WIDTH, HEIGHT, journal_text)

        if result == "SUMMARY":
            game_state = "SUMMARY"

        elif result == "BACK":
            game_state = "PLAYING"

    # -------- DRAW --------
    screen.fill(COL_BG)
# /reset_game
    if game_state == "PLAYING":

        for c in clouds:
            c.draw(screen, scroll_x, scroll_y)

        for a in asteroids:
            a.draw(screen, scroll_x, scroll_y)

        for sym in all_symbols:
            sym.draw(screen, scroll_x, scroll_y)

        player.draw(screen, scroll_x, scroll_y)

    elif game_state == "JOURNAL":
        screen.fill((20, 20, 40))

    elif game_state == "MENU":
        screen.fill((0, 0, 0))

    elif game_state == "SUMMARY":
        screen.fill((30, 30, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()