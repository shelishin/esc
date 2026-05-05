import pygame
import random
import math
import os
import sys
import journal123

pygame.init()
pygame.mixer.init() 
WIDTH, HEIGHT      = 1024, 576  # Match start_echoSketch resolution
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
book_title_font = pygame.font.SysFont("brush script", 42, bold=True)
book_text_font = pygame.font.SysFont("brush script", 30)

# Start screen constants
WHITE = (255, 255, 255)
CYAN_GLOW = (140, 255, 255)
HOVER_COLOR = (200, 255, 255)

# Load Background
try:
    BACKGROUND = pygame.image.load("bg start.png")
    BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
except:
    print("Error: 'bg start.png' not found. Using black background.")
    BACKGROUND = pygame.Surface((WIDTH, HEIGHT))
    BACKGROUND.fill((10, 10, 25))

# Font for start screen buttons
font_path = pygame.font.match_font('verdana', 'arial')
button_font = pygame.font.Font(font_path, 60)

# Load Journal assets
try:
    JOURNAL_BG = pygame.image.load("bg start.png")
    JOURNAL_BG = pygame.transform.scale(JOURNAL_BG, (WIDTH, HEIGHT))
except:
    print("Error: 'bg start.png' not found for journal.")
    JOURNAL_BG = pygame.Surface((WIDTH, HEIGHT))
    JOURNAL_BG.fill((10, 10, 25))

try:
    BOOK_IMG = pygame.image.load("color-de-papel.png")
    BOOK_IMG = pygame.transform.scale(BOOK_IMG, (700, 450))
except:
    print("Error: 'color-de-papel.png' not found. Using placeholder.")
    BOOK_IMG = pygame.Surface((700, 450))
    BOOK_IMG.fill((240, 220, 180))

# Journal variables
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

def wrap_text(text, max_chars):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        test = current + word + " "
        if len(test) <= max_chars:
            current = test
        else:
            lines.append(current)
            current = word + " "
    lines.append(current)
    return lines

def draw_button(text, y_pos, mouse_pos):
    """Draws a glass-style button with hover effects"""
    rect_width, rect_height = 450, 120
    rect_x = (WIDTH // 2) - (rect_width // 2)
    button_rect = pygame.Rect(rect_x, y_pos, rect_width, rect_height)
    
    # Check for hover
    is_hovered = button_rect.collidepoint(mouse_pos)
    color = HOVER_COLOR if is_hovered else CYAN_GLOW
    border_thickness = 4 if is_hovered else 2

    # Draw Button Border (Rounded)
    pygame.draw.rect(screen, color, button_rect, border_thickness, border_radius=20)
    
    # Subtle "Glass" Overlay
    glass_surf = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    glass_surf.fill((255, 255, 255, 20))
    screen.blit(glass_surf, (rect_x, y_pos))

    # Render Text
    text_surf = button_font.render(text, True, color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

    return button_rect

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

CONSTELLATION_LINE_COLOR = (180, 180, 255, 255)
CONSTELLATION_STAR_COLOR = (255, 255, 180, 255)
CONSTELLATION_STAR_RADIUS = 18   

JOURNAL_MESSAGES = ["A spark of energy...", "Movement is life...", "Capturing the flow...", "Clarity in speed..."]
s
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

    def draw(self, surface, scroll_x, scroll_y):
        if not self.active: return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
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
    global score, journal_msg, journal_timer, journal_triggered
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
    journal_triggered = False

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
for _ in range(15):
    pygame.draw.circle(bg_tile, (60, 60, 90), (random.randint(0,400), random.randint(0,400)), 1)

reset_game()
game_state = "MENU"
journal_active = False
journal_triggered = False
scroll_x = scroll_y = 0

middle_box = pygame.Rect(200, 150, 600, 300)
back_btn_rect   = pygame.Rect(180, 480, 300, 70)
play_btn_rect   = pygame.Rect(520, 480, 300, 70)

running = True
while running:
    mx, my = pygame.mouse.get_pos()
    tick_count = pygame.time.get_ticks()
    mouse_clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True
        elif event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                if event.key == pygame.K_SPACE:
                    game_state = "PLAYING"
                elif event.key == pygame.K_r:
                    reset_game()
                    game_state = "MENU"
            elif game_state == "PLAYING":
                if event.key == pygame.K_e:
                    game_state = "SUMMARY"
                elif event.key == pygame.K_s:
                    pygame.image.save(screen, "high_energy_journey.png")
            elif game_state == "JOURNAL":
                if event.key == pygame.K_BACKSPACE:
                    journal_user_text = journal_user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    journal_user_text += " "
                elif event.key == pygame.K_ESCAPE:
                    game_state = "MENU"
                else:
                    journal_user_text += event.unicode
            elif game_state == "CODE_EDITOR":
                if event.key == pygame.K_BACKSPACE:
                    code_text = code_text[:-1]
                elif event.key == pygame.K_RETURN:
                    code_text += '\n'
                elif event.key == pygame.K_ESCAPE:
                    game_state = "MENU"
                elif event.key == pygame.K_TAB:
                    code_text += '    '
                else:
                    code_text += event.unicode

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
            if a.active and wrapping_dist(player.x, player.y, a.x, a.y) < a.radius + player.radius:
                a.active = False
                if SND_ASTEROID: SND_ASTEROID.play()
                for _ in range(6): splashes.append(SplashParticle(a.x, a.y, (150, 150, 140)))

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
                    journal_msg, journal_timer = random.choice(JOURNAL_MESSAGES), 120
                elif sym.type == "note":
                    if SND_NOTE: SND_NOTE.play()

        for orb in orbs:
            orb.update()
            if not orb.collected and wrapping_dist(player.x, player.y, orb.x, orb.y) < 45:
                orb.collected = True
                player.boost_timer, score = 200, score + 10
                if SND_ORB: SND_ORB.play()

        # Transition to journal when all orbs collected
        if game_state == "PLAYING" and all(o.collected for o in orbs):
            game_state = "JOURNAL"
            journal_user_text = ""

        for s in splashes[:]:
            s.update()
            if s.lifetime <= 0: splashes.remove(s)
        if journal_timer > 0: journal_timer -= 1

    screen.fill(COL_BG)

    ox, oy = int(-(scroll_x * PARALLAX_FACTOR) % 400), int(-(scroll_y * PARALLAX_FACTOR) % 400)
    for tx in range(-1, (WIDTH // 400) + 2):
        for ty in range(-1, (HEIGHT // 400) + 2):
            screen.blit(bg_tile, (tx * 400 + ox, ty * 400 + oy))

    if game_state != "SUMMARY":
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
        if journal_timer > 0: draw_text_centered(journal_msg, font_medium, COL_WHITE, HEIGHT - 120)
    
    elif game_state == "SUMMARY":
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        title_rect = pygame.Rect(WIDTH//2 - 250, 40, 500, 70)
        draw_glow_rect(screen, title_rect, CYAN, 25, 3)
        txt_surf = title_font.render("MISSION SUMMARY", True, CYAN)
        screen.blit(txt_surf, txt_surf.get_rect(center=title_rect.center))

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
        screen.blit(JOURNAL_BG, (0, 0))
        screen.blit(BOOK_IMG, (journal_book_x, journal_book_y))

        # Title
        title_surf = book_title_font.render("My Diary", True, WHITE)
        screen.blit(title_surf, (540, 50))

        # Wrap and render text
        lines = wrap_text(journal_user_text, journal_max_chars)

        # Left page
        y = journal_start_y
        for i in range(min(len(lines), journal_max_lines_left)):
            txt = book_text_font.render(lines[i], True, (0, 0, 0))
            screen.blit(txt, (journal_left_x, y))
            y += journal_line_spacing

        # Right page
        y = journal_start_y
        for i in range(journal_max_lines_left, min(len(lines), journal_max_lines_left + journal_max_lines_right)):
            txt = book_text_font.render(lines[i], True, (0, 0, 0))
            screen.blit(txt, (journal_right_x, y))
            y += journal_line_spacing

    elif game_state == "MENU":
        # Draw background
        screen.blit(BACKGROUND, (0, 0))
        
        # Draw buttons
        play_btn = draw_button("play", 200, (mx, my))
        options_btn = draw_button("options", 350, (mx, my))
        
        # Handle button clicks
        if mouse_clicked:
            if play_btn.collidepoint(mx, my):
                game_state = "PLAYING"
            if options_btn.collidepoint(mx, my):
                game_state = "JOURNAL"
                journal_user_text = ""  # Clear previous text

    pygame.display.flip()
    clock.tick(60)

pygame.quit()