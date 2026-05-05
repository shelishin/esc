import pygame
import random
import math
import os
import sys

pygame.init()
pygame.mixer.init() 
WIDTH, HEIGHT      = 1000, 700
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

title_font = pygame.font.SysFont("arial", 45, bold=True)
btn_font   = pygame.font.SysFont("arial", 26, bold=True)

def load_animation_frames(folder, base_name, count, size):
    frames = []
    if os.path.exists(folder):
        for i in range(1, count + 1):
            path = os.path.join(folder, f"{base_name}{i}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, size)
                frames.append(img)
            except:
                print(f"Could not load {path}")
    return frames

NOTE_SPRITES    = load_animation_frames("notes", "note", 4, (80, 80))
JOURNAL_SPRITES = load_animation_frames("journals", "journal", 4, (80, 80))
ORB_SPRITES     = load_animation_frames("orbs", "orb", 4, (70, 70))
CLOUD_SPRITES_1 = load_animation_frames("cloud_type1", "cloud", 4, (250, 160))
CLOUD_SPRITES_2 = load_animation_frames("cloud_type2", "cloud", 4, (250, 160))

asteroid_image = None
try:
    raw_ast = pygame.image.load("asteriod.png").convert_alpha()
    asteroid_image = pygame.transform.scale(raw_ast, (70, 70))
except:
    print("Could not load asteroid image")

def load_sound(name):
    try: return pygame.mixer.Sound(name)
    except: return None

SND_NOTE     = load_sound("note.wav")
SND_JOURNAL  = load_sound("journal.wav")
SND_ORB      = load_sound("orb.wav")
SND_CLOUD    = load_sound("cloud.wav")
SND_ASTEROID = load_sound("asteroid.wav")

if SND_NOTE: SND_NOTE.set_volume(0.4)
if SND_JOURNAL: SND_JOURNAL.set_volume(0.5)
if SND_ORB: SND_ORB.set_volume(0.6)
if SND_CLOUD: SND_CLOUD.set_volume(0.3)
if SND_ASTEROID: SND_ASTEROID.set_volume(0.5)

COL_BG       = (10,  10,  25)
COL_WHITE    = (255, 255, 255)
COL_PINK     = (255, 100, 200)
COL_BLUE     = (100, 180, 255)
COL_YELLOW   = (255, 230, 100)
COL_TEAL     = (60,  220, 200)
CYAN         = (120, 255, 255)
COL_STAR     = (255, 255, 200)
BLACK        = (0, 0, 0)

CONSTELLATION_LINE_COLOR = (180, 180, 255, 255)
CONSTELLATION_STAR_COLOR = (255, 255, 180, 255)
CONSTELLATION_STAR_RADIUS = 18   

JOURNAL_MESSAGES = [
    "A spark of energy...", "Movement is life...", 
    "Capturing the flow...", "Clarity in speed..."
]

COLLECTION_QUOTES = [
    "Your journey is your own masterpiece.",
    "Every step forward is a victory.",
    "Courage is the fuel of the brave.",
    "The path reveals itself as you walk it.",
    "You are stronger than you know.",
    "Doubt kills more dreams than failure ever will.",
    "Keep going. You're closer than you think.",
    "Small steps still move mountains.",
    "Believe in the spark within you.",
    "You don't have to be perfect, just persistent."
]

END_QUOTES = [
    "You've completed the journey. Every step mattered.",
    "Keep moving forward, your path is still unfolding.",
    "The universe rewards those who dare to explore.",
    "You painted the void with courage. Remember this light.",
    "Every ending is a new constellation waiting to form.",
    "The spark within you never fades, it only grows.",
    "You turned chaos into beauty. Carry that with you.",
    "Momentum is proof: you were never meant to stand still."
]
selected_quote = ""
journal_fade_alpha = 255
journal_fading_out = False

CHALLENGE_TIMES = {"EASY": 180, "MEDIUM": 120, "HARD": 60}
is_challenge_mode = False
challenge_difficulty = "EASY"
time_remaining = 0
challenge_active = False

class SplashParticle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(4, 9)
        self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed
        self.color = color
        self.lifetime = 255
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 12
        self.size *= 0.94

    def draw(self, surface, scroll_x, scroll_y):
        if self.lifetime <= 0: return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        r = max(1, int(self.size))
        s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, max(0, self.lifetime)), (r, r), r)
        surface.blit(s, (int(sx - r), int(sy - r)))

class Cloud:
    def __init__(self, type_id):
        self.x = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.y = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.type_id = type_id
        if type_id == 1:
            self.frames = CLOUD_SPRITES_1
            self.color = COL_BLUE
        else:
            self.frames = CLOUD_SPRITES_2
            self.color = COL_PINK
        
        self.frame_index = random.uniform(0, 3)
        self.anim_speed = 0.05

    def update(self):
        if self.frames:
            self.frame_index = (self.frame_index + self.anim_speed) % len(self.frames)

    def draw(self, surface, scroll_x, scroll_y):
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        if self.frames:
            img = self.frames[int(self.frame_index)]
            rect = img.get_rect(center=(int(sx), int(sy)))
            surface.blit(img, rect)
        else:
            pygame.draw.circle(surface, (*self.color, 70), (int(sx), int(sy)), 80)

class InspirationSymbol:
    def __init__(self, sym_type):
        self.x, self.y = random.randint(0, VIRTUAL_WORLD_SIZE), random.randint(0, VIRTUAL_WORLD_SIZE)
        self.type = sym_type
        self.collected = False
        self.frame_index = random.uniform(0, 3)
        self.anim_speed = 0.12 

    def update(self): 
        frames = NOTE_SPRITES if self.type == "note" else JOURNAL_SPRITES
        if frames:
            self.frame_index = (self.frame_index + self.anim_speed) % len(frames)

    def draw(self, surface, scroll_x, scroll_y):
        if self.collected: return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        
        frames = NOTE_SPRITES if self.type == "note" else JOURNAL_SPRITES
        if frames:
            img = frames[int(self.frame_index)]
            rect = img.get_rect(center=(int(sx), int(sy)))
            surface.blit(img, rect)
        else:
            col = COL_PINK if self.type == "note" else COL_YELLOW
            pygame.draw.circle(surface, col, (int(sx), int(sy)), 30)

class SupportOrb:
    def __init__(self):
        self.x, self.y = random.randint(0, VIRTUAL_WORLD_SIZE), random.randint(0, VIRTUAL_WORLD_SIZE)
        self.collected = False
        self.frame_index = random.uniform(0, 3)
        self.anim_speed = 0.15

    def update(self): 
        if ORB_SPRITES:
            self.frame_index = (self.frame_index + self.anim_speed) % len(ORB_SPRITES)

    def draw(self, surface, scroll_x, scroll_y):
        if self.collected: return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        if ORB_SPRITES:
            img = ORB_SPRITES[int(self.frame_index)]
            rect = img.get_rect(center=(int(sx), int(sy)))
            surface.blit(img, rect)
        else:
            pygame.draw.circle(surface, COL_YELLOW, (int(sx), int(sy)), 25)

class Asteroid:
    def __init__(self):
        self.x, self.y = random.randint(0, VIRTUAL_WORLD_SIZE), random.randint(0, VIRTUAL_WORLD_SIZE)
        self.radius = random.randint(18, 35)
        self.active = True

    def update(self):
        pass

    def draw(self, surface, scroll_x, scroll_y):
        if not self.active: return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        if asteroid_image:
            rect = asteroid_image.get_rect(center=(int(sx), int(sy)))
            surface.blit(asteroid_image, rect)
        else:
            pygame.draw.circle(surface, (130, 120, 110), (int(sx), int(sy)), self.radius)
            pygame.draw.circle(surface, (90, 85, 80), (int(sx), int(sy)), self.radius, 2)

class TinyPlanet:
    def __init__(self, color):
        self.x = self.y = VIRTUAL_WORLD_SIZE // 2
        self.color = list(color)
        self.target_color = list(color)
        self.radius = 14
        self.extra_radius = 0
        self.boost_timer = 0

    def update(self, target_wx, target_wy):
        prev_x, prev_y = self.x, self.y
        self.x += (target_wx - self.x) * 0.06
        self.y += (target_wy - self.y) * 0.06
        self.x %= VIRTUAL_WORLD_SIZE
        self.y %= VIRTUAL_WORLD_SIZE

        for i in range(3):
            self.color[i] += (self.target_color[i] - self.color[i]) * 0.07
        
        if self.boost_timer > 0:
            self.boost_timer -= 1
            self.extra_radius = 12
        else:
            self.extra_radius = max(0, self.extra_radius - 0.6)

        if abs(self.x - prev_x) < 400 and abs(self.y - prev_y) < 400:
            brush_color = (*[int(c) for c in self.color], TRAIL_ALPHA)
            thickness = int((self.radius + self.extra_radius) * 1.8)
            pygame.draw.line(canvas, brush_color, (prev_x, prev_y), (self.x, self.y), thickness)
            pygame.draw.circle(canvas, brush_color, (int(self.x), int(self.y)), thickness // 2)

    def draw(self, surface, scroll_x, scroll_y):
        bx, by = screen_pos(self.x, self.y, scroll_x, scroll_y)
        pygame.draw.circle(surface, [int(c) for c in self.color], (int(bx), int(by)), self.radius)
        pygame.draw.circle(surface, COL_WHITE, (int(bx), int(by)), self.radius, 2)

def wrapping_dist(ax, ay, bx, by):
    dx, dy = ax - bx, ay - by
    if dx >  VIRTUAL_WORLD_SIZE / 2: dx -= VIRTUAL_WORLD_SIZE
    if dx < -VIRTUAL_WORLD_SIZE / 2: dx += VIRTUAL_WORLD_SIZE
    if dy >  VIRTUAL_WORLD_SIZE / 2: dy -= VIRTUAL_WORLD_SIZE
    if dy < -VIRTUAL_WORLD_SIZE / 2: dy += VIRTUAL_WORLD_SIZE
    return math.hypot(dx, dy)

def screen_pos(wx, wy, scroll_x, scroll_y):
    sx = (wx - scroll_x) % VIRTUAL_WORLD_SIZE
    sy = (wy - scroll_y) % VIRTUAL_WORLD_SIZE
    if sx > WIDTH  + 300: sx -= VIRTUAL_WORLD_SIZE
    if sy > HEIGHT + 300: sy -= VIRTUAL_WORLD_SIZE
    return sx, sy

def draw_text_centered(text, font, color, y_center):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y_center))
    screen.blit(surf, rect)
    return rect

def draw_glow_rect(surface, rect, color, radius=20, border=3):
    glow = pygame.Surface((rect.width + 40, rect.height + 40), pygame.SRCALPHA)
    for i in range(8):
        pygame.draw.rect(glow, (*color, 15), (20 - i, 20 - i, rect.width + i * 2, rect.height + i * 2), border_radius=radius)
    pygame.draw.rect(glow, (*color, 180), (20, 20, rect.width, rect.height), width=border, border_radius=radius)
    surface.blit(glow, (rect.x - 20, rect.y - 20))

def _draw_star_on_canvas(x, y):
    cx, cy = int(x), int(y)
    pygame.draw.circle(canvas, (120, 120, 255, 180), (cx, cy), 40)
    pygame.draw.circle(canvas, (200, 200, 255, 220), (cx, cy), 26)
    pygame.draw.circle(canvas, (255, 255, 220, 255), (cx, cy), CONSTELLATION_STAR_RADIUS)

def draw_constellation_on_canvas(positions):
    if len(positions) < 2:
        return
    p1 = positions[-2]
    p2 = positions[-1]
    pygame.draw.line(canvas, CONSTELLATION_LINE_COLOR,
                     (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), 20)
    _draw_star_on_canvas(p2[0], p2[1])
    if len(positions) == 2:
        _draw_star_on_canvas(p1[0], p1[1])

def draw_first_constellation_star(x, y):
    _draw_star_on_canvas(x, y)

def reset_game():
    global player, asteroids, clouds, notes, journals, all_symbols, orbs, splashes, constellation_positions
    global score, journal_msg, journal_timer, journal_fade_alpha, journal_fading_out
    global is_challenge_mode, challenge_difficulty, time_remaining, challenge_active
    global shake_intensity
    canvas.fill((0, 0, 0, 0)) 
    player = TinyPlanet(COL_YELLOW)
    asteroids = [Asteroid() for _ in range(50)]
    clouds = [Cloud(random.choice([1, 2])) for _ in range(30)]
    notes = [InspirationSymbol("note") for _ in range(12)]
    journals = [InspirationSymbol("journal") for _ in range(5)]
    all_symbols = notes + journals
    orbs = [SupportOrb() for _ in range(7)]
    splashes = []
    constellation_positions = []
    score = 0
    journal_msg = ""
    journal_timer = 0
    journal_fade_alpha = 255
    journal_fading_out = False
    time_remaining = 0
    challenge_active = False
    is_challenge_mode = False
    shake_intensity = 0

def draw_ui(orb_count):
    zone_y = HEIGHT - 70
    s = pygame.Surface((WIDTH, 70), pygame.SRCALPHA)
    s.fill((0, 0, 0, 190))
    screen.blit(s, (0, zone_y))
    info = font_tiny.render(f"ENERGY: HIGH | ORBS: {orb_count} | S: SAVE | R: RESET | E: END", True, COL_YELLOW)
    screen.blit(info, (20, zone_y + 25))
    pct = min(score / 250, 1.0)
    pygame.draw.rect(screen, (40, 40, 60), (WIDTH-320, zone_y+30, 300, 10))
    pygame.draw.rect(screen, COL_YELLOW, (WIDTH-320, zone_y+30, int(300*pct), 10))

bg_tile = pygame.Surface((400, 400))
bg_tile.fill((10, 10, 20))
star_sprite = pygame.Surface((8, 8), pygame.SRCALPHA)
pygame.draw.circle(star_sprite, (80, 80, 110, 200), (4, 4), 4)
for _ in range(15):
    bx, by = random.randint(0, 400), random.randint(0, 400)
    bg_tile.blit(star_sprite, (bx - 4, by - 4))

# ---------------- JOURNAL / DIARY SETUP ----------------
journal_background = pygame.image.load("bg start.png")
journal_background = pygame.transform.scale(journal_background, (WIDTH, HEIGHT))

book_image = pygame.image.load("book.png")
book_image = pygame.transform.scale(book_image, (700, 450))

journal_font_title = pygame.font.SysFont("brush script", 42, True)
journal_font_text = pygame.font.SysFont("brush script", 30)
journal_user_text = ""

journal_book_x = WIDTH // 2 - 350
journal_book_y = HEIGHT // 2 - 225

journal_left_x = journal_book_x + 55
journal_right_x = journal_book_x + 375
journal_start_y = journal_book_y + 70
journal_line_spacing = 30
journal_max_chars = 22
journal_max_lines_left = 9
journal_max_lines_right = 9

def journal_wrap_text(text):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        test = current + word + " "
        if len(test) <= journal_max_chars:
            current = test
        else:
            lines.append(current)
            current = word + " "
    lines.append(current)
    return lines

def draw_journal_screen():
    screen.blit(journal_background, (0, 0))
    screen.blit(book_image, (journal_book_x, journal_book_y))
    
    title = journal_font_title.render("My Diary", True, (80, 60, 50))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    
    lines = journal_wrap_text(journal_user_text)
    
    y = journal_start_y
    for i in range(min(len(lines), journal_max_lines_left)):
        txt = journal_font_text.render(lines[i], True, BLACK)
        screen.blit(txt, (journal_left_x, y))
        y += journal_line_spacing
    
    y = journal_start_y
    for i in range(journal_max_lines_left, min(len(lines), journal_max_lines_left + journal_max_lines_right)):
        txt = journal_font_text.render(lines[i], True, BLACK)
        screen.blit(txt, (journal_right_x, y))
        y += journal_line_spacing
    
    close_btn = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 80, 160, 50)
    draw_glow_rect(screen, close_btn, COL_TEAL, 15, 2)
    close_txt = btn_font.render("CLOSE", True, COL_WHITE)
    screen.blit(close_txt, close_txt.get_rect(center=close_btn.center))
    
    return close_btn

reset_game()
game_state = "MENU"
scroll_x = scroll_y = 0
shake_intensity = 0

middle_box = pygame.Rect(200, 150, 600, 300)
back_btn_rect   = pygame.Rect(180, 550, 300, 70)
play_btn_rect   = pygame.Rect(520, 550, 300, 70)

challenge_btn_rect = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 + 100, 260, 55)
diff_box = pygame.Rect(WIDTH // 2 - 280, HEIGHT // 2 - 60, 180, 70)
diff_medium = pygame.Rect(WIDTH // 2 - 90, HEIGHT // 2 - 60, 180, 70)
diff_hard = pygame.Rect(WIDTH // 2 + 100, HEIGHT // 2 - 60, 180, 70)
diff_back_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 55)

running = True
while running:
    mx, my = pygame.mouse.get_pos()
    tick_count = pygame.time.get_ticks()
    mouse_clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN: mouse_clicked = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == "MENU": game_state = "PLAYING"
            if event.key == pygame.K_r: reset_game(); game_state = "MENU"
            if event.key == pygame.K_e and game_state == "PLAYING": game_state = "SUMMARY"
            if event.key == pygame.K_s:
                pygame.image.save(screen, "high_energy_journey.png")

            if game_state == "JOURNAL":
                if event.key == pygame.K_BACKSPACE:
                    journal_user_text = journal_user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    journal_user_text += " "
                else:
                    journal_user_text += event.unicode

    if game_state == "PLAYING":
        player.update(mx + scroll_x, my + scroll_y)
        scroll_x, scroll_y = player.x - WIDTH // 2, player.y - HEIGHT // 2

        for c in clouds:
            c.update()
            if wrapping_dist(player.x, player.y, c.x, c.y) < 100:
                if player.target_color != list(c.color):
                    player.target_color = list(c.color)
                    if SND_CLOUD: SND_CLOUD.play()

        for a in asteroids:
            a.update()
            if a.active and wrapping_dist(player.x, player.y, a.x, a.y) < a.radius + player.radius:
                a.active = False
                if SND_ASTEROID: SND_ASTEROID.play()
                for _ in range(6): splashes.append(SplashParticle(a.x, a.y, (150, 150, 140)))
                shake_intensity = 12

        for sym in all_symbols:
            sym.update() 
            if not sym.collected and wrapping_dist(player.x, player.y, sym.x, sym.y) < 50:
                sym.collected = True
                if len(constellation_positions) == 0:
                    draw_first_constellation_star(sym.x, sym.y)

                constellation_positions.append((sym.x, sym.y))

                if len(constellation_positions) >= 2:
                    draw_constellation_on_canvas(constellation_positions)
                score += 15
                if sym.type == "journal":
                    if SND_JOURNAL: SND_JOURNAL.play()
                    journal_msg, journal_timer = random.choice(COLLECTION_QUOTES), 120
                elif sym.type == "note":
                    if SND_NOTE: SND_NOTE.play()

        for orb in orbs:
            orb.update()
            if not orb.collected and wrapping_dist(player.x, player.y, orb.x, orb.y) < 45:
                orb.collected = True
                player.boost_timer, score = 200, score + 10
                if SND_ORB: SND_ORB.play()

        if all(o.collected for o in orbs):
            if is_challenge_mode:
                game_state = "SUMMARY"
            else:
                selected_quote = random.choice(END_QUOTES)
                game_state = "END_QUOTE"

        for s in splashes[:]:
            s.update()
            if s.lifetime <= 0: splashes.remove(s)
        if journal_timer > 0: journal_timer -= 1
        if is_challenge_mode and challenge_active:
            time_remaining -= 1 / 60
            if time_remaining <= 0:
                time_remaining = 0
                challenge_active = False
                game_state = "SUMMARY"

    shake_offset_x = 0
    shake_offset_y = 0
    if game_state == "PLAYING" and shake_intensity > 0:
        shake_offset_x = random.randint(-int(shake_intensity), int(shake_intensity))
        shake_offset_y = random.randint(-int(shake_intensity), int(shake_intensity))
        scroll_x += shake_offset_x
        scroll_y += shake_offset_y
        shake_intensity = max(0, shake_intensity - 1.2)

    screen.fill(COL_BG)

    ox, oy = int(-(scroll_x * PARALLAX_FACTOR) % 400), int(-(scroll_y * PARALLAX_FACTOR) % 400)
    for tx in range(-1, (WIDTH // 400) + 2):
        for ty in range(-1, (HEIGHT // 400) + 2):
            screen.blit(bg_tile, (tx * 400 + ox, ty * 400 + oy))

    if game_state not in ("SUMMARY", "JOURNAL"):
        cx, cy = screen_pos(0, 0, scroll_x, scroll_y)
        for off_x in [0, -VIRTUAL_WORLD_SIZE]:
            for off_y in [0, -VIRTUAL_WORLD_SIZE]:
                screen.blit(canvas, (cx + off_x, cy + off_y))

    if game_state == "PLAYING":
        for a in asteroids: a.draw(screen, scroll_x, scroll_y)
        for c in clouds: c.draw(screen, scroll_x, scroll_y)
        for sym in all_symbols: sym.draw(screen, scroll_x, scroll_y)
        for orb in orbs: orb.draw(screen, scroll_x, scroll_y)
        for s in splashes: s.draw(screen, scroll_x, scroll_y)
        player.draw(screen, scroll_x, scroll_y)
        draw_ui(len([o for o in orbs if o.collected]))
        if is_challenge_mode and challenge_active:
            mins = int(time_remaining) // 60
            secs = int(time_remaining) % 60
            timer_col = COL_PINK if time_remaining < 15 else COL_TEAL
            timer_surf = font_medium.render(f"TIME: {mins}:{secs:02d}", True, timer_col)
            screen.blit(timer_surf, (WIDTH - timer_surf.get_width() - 30, 20))
        if journal_timer > 0: draw_text_centered(journal_msg, font_medium, COL_WHITE, HEIGHT - 120)
    
    elif game_state == "SUMMARY":
        screen.blit(journal_background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        offset_y = 0
        if is_challenge_mode:
            orbs_collected = sum(1 for o in orbs if o.collected)
            won = orbs_collected == len(orbs)
            title_text = "CHALLENGE COMPLETE!" if won else "TIME'S UP!"
            title_color = COL_TEAL if won else COL_PINK
            draw_text_centered(title_text, font_large, title_color, 60)
            draw_text_centered(f"Orbs collected: {orbs_collected} / {len(orbs)}", font_medium, COL_WHITE, 100)
            offset_y = 55
        else:
            title_rect = pygame.Rect(WIDTH//2 - 250, 40, 500, 70)
            draw_glow_rect(screen, title_rect, CYAN, 25, 3)
            txt_surf = title_font.render("MISSION SUMMARY", True, CYAN)
            screen.blit(txt_surf, txt_surf.get_rect(center=title_rect.center))

        middle_box.y = 120 + offset_y

        draw_glow_rect(screen, middle_box, CYAN, 25, 3)

        canvas_w = middle_box.width - 20
        canvas_h = middle_box.height - 20
        preview_surf = pygame.Surface((canvas_w, canvas_h))
        preview_surf.fill((8, 8, 20))
        rng = random.Random(42)  
        for _ in range(120):
            sx2 = rng.randint(0, canvas_w - 1)
            sy2 = rng.randint(0, canvas_h - 1)
            bright = rng.randint(60, 160)
            preview_surf.set_at((sx2, sy2), (bright, bright, bright))

        mini_canvas = pygame.transform.smoothscale(canvas, (canvas_w, canvas_h))
        preview_surf.blit(mini_canvas, (0, 0))

        screen.blit(preview_surf, (middle_box.x + 10, middle_box.y + 10))

        btn_y = middle_box.y + middle_box.height + 20
        back_btn_rect = pygame.Rect(180, btn_y, 300, 70)
        play_btn_rect = pygame.Rect(520, btn_y, 300, 70)

        draw_glow_rect(screen, back_btn_rect, CYAN, 20, 2)
        bt_txt = btn_font.render("BACK TO MENU", True, CYAN)
        screen.blit(bt_txt, bt_txt.get_rect(center=back_btn_rect.center))

        draw_glow_rect(screen, play_btn_rect, COL_PINK, 20, 2)
        pa_txt = btn_font.render("PLAY AGAIN", True, COL_PINK)
        screen.blit(pa_txt, pa_txt.get_rect(center=play_btn_rect.center))

        if mouse_clicked:
            if back_btn_rect.collidepoint(mx, my):
                reset_game()
                game_state = "MENU"
            if play_btn_rect.collidepoint(mx, my):
                reset_game()
                game_state = "PLAYING"

    elif game_state == "JOURNAL":
        close_btn = draw_journal_screen()
        
        if journal_fading_out:
            journal_fade_alpha -= 8
            if journal_fade_alpha <= 0:
                game_state = "SUMMARY"
                journal_fade_alpha = 0
                journal_fading_out = False
        
        if mouse_clicked and close_btn.collidepoint(mx, my) and not journal_fading_out:
            journal_fading_out = True
        
        if journal_fade_alpha < 255:
            fade_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            fade_overlay.fill((0, 0, 0, 255 - journal_fade_alpha))
            screen.blit(fade_overlay, (0, 0))

    elif game_state == "END_QUOTE":
        screen.blit(journal_background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        quote_box = pygame.Rect(WIDTH//2 - 340, HEIGHT//2 - 140, 680, 280)
        draw_glow_rect(screen, quote_box, COL_YELLOW, 30, 3)

        words = selected_quote.split()
        lines = []
        current = ""
        for word in words:
            test = current + word + " "
            if len(test) <= 38:
                current = test
            else:
                lines.append(current)
                current = word + " "
        lines.append(current)

        line_height = 42
        total_text_h = len(lines) * line_height
        y_start = quote_box.y + (quote_box.height - total_text_h) // 2 + 20
        for i, line in enumerate(lines):
            surf = font_medium.render(line.strip(), True, COL_WHITE)
            rect = surf.get_rect(center=(WIDTH // 2, y_start + line_height * i))
            screen.blit(surf, rect)

        continue_txt = font_small.render("Click anywhere to continue...", True, (150, 150, 200))
        pulse = int(150 + 50 * math.sin(tick_count * 0.004))
        continue_txt = font_small.render("Click anywhere to continue...", True, (pulse, pulse, 200))
        screen.blit(continue_txt, continue_txt.get_rect(center=(WIDTH//2, HEIGHT - 100)))

        if mouse_clicked:
            game_state = "JOURNAL"
    
    elif game_state == "MENU":
        screen.blit(journal_background, (0, 0))
        
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 185))
        screen.blit(ov, (0, 0))
        
        draw_text_centered("ECHO SKETCH: ENERGETIC FLOW", font_large, COL_PINK, HEIGHT//2 - 120)
        draw_text_centered("Guide the spark. Paint the void.", font_small, COL_WHITE, HEIGHT//2 - 60)
        draw_text_centered("Touch Clouds to shift colors.", font_tiny, (200, 200, 255), HEIGHT//2 - 10)
        draw_text_centered("Collect symbols to map constellations.", font_tiny, (200, 200, 255), HEIGHT//2 + 20)
        
        btn_rect = pygame.Rect(0, 0, 260, 70)
        btn_rect.center = (WIDTH // 2, HEIGHT // 2 + 100)
        is_hover = btn_rect.collidepoint(mx, my)
        pulse = (math.sin(tick_count * 0.005) + 1) / 2
        btn_col = COL_TEAL if is_hover else (int(60 + 40*pulse), int(180 + 40*pulse), int(160 + 40*pulse))
        
        pygame.draw.rect(screen, btn_col, btn_rect, border_radius=15)
        pygame.draw.rect(screen, COL_WHITE, btn_rect, 3, border_radius=15)
        draw_text_centered("PLAY", font_medium, COL_BG, HEIGHT // 2 + 100)
        
        if is_hover and mouse_clicked:
            game_state = "PLAYING"

        challenge_btn_rect = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 + 185, 260, 55)
        chov = challenge_btn_rect.collidepoint(mx, my)
        ch_col = COL_PINK if chov else (int(150 + 50 * math.sin(tick_count * 0.005)), 100, 150)
        pygame.draw.rect(screen, ch_col, challenge_btn_rect, border_radius=12)
        pygame.draw.rect(screen, COL_WHITE, challenge_btn_rect, 2, border_radius=12)
        draw_text_centered("CHALLENGE", font_medium, COL_WHITE, HEIGHT // 2 + 213)
        if chov and mouse_clicked:
            game_state = "CHALLENGE_SELECT"

    elif game_state == "CHALLENGE_SELECT":
        screen.blit(journal_background, (0, 0))
        overlay_sel = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay_sel.fill((0, 0, 0, 200))
        screen.blit(overlay_sel, (0, 0))

        sel_title = title_font.render("SELECT DIFFICULTY", True, COL_YELLOW)
        screen.blit(sel_title, sel_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 160)))

        for diff, rect, col in [("EASY", diff_box, COL_TEAL), ("MEDIUM", diff_medium, COL_BLUE), ("HARD", diff_hard, COL_PINK)]:
            hov = rect.collidepoint(mx, my)
            c = tuple(min(255, x + 40) for x in col) if hov else col
            draw_glow_rect(screen, rect, c, 18, 2)
            txt = font_medium.render(diff, True, COL_WHITE)
            screen.blit(txt, txt.get_rect(center=rect.center))
            sub = font_tiny.render(f"{CHALLENGE_TIMES[diff]}s", True, (200, 200, 200))
            screen.blit(sub, sub.get_rect(center=(rect.centerx, rect.y + 50)))

            if hov and mouse_clicked:
                challenge_difficulty = diff
                time_remaining = CHALLENGE_TIMES[diff]
                is_challenge_mode = True
                challenge_active = True
                reset_game()
                is_challenge_mode = True
                challenge_difficulty = diff
                time_remaining = CHALLENGE_TIMES[diff]
                challenge_active = True
                game_state = "PLAYING"

        draw_glow_rect(screen, diff_back_btn, (100, 100, 120), 15, 2)
        back_txt = font_medium.render("BACK", True, COL_WHITE)
        screen.blit(back_txt, back_txt.get_rect(center=diff_back_btn.center))
        if diff_back_btn.collidepoint(mx, my) and mouse_clicked:
            game_state = "MENU"

    if shake_offset_x != 0:
        scroll_x -= shake_offset_x
        scroll_y -= shake_offset_y

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
