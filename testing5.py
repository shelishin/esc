import pygame
import random
import math
import os
import sys
import time

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

NOTE_SPRITES    = load_animation_frames("notes", "note", 4, (100, 100))
JOURNAL_SPRITES = load_animation_frames("journals", "journal", 4, (100, 100))
ORB_SPRITES     = load_animation_frames("orbs", "orb", 4, (90, 90))
CLOUD_SPRITES_1 = load_animation_frames("cloud_type1", "cloud", 4, (320, 200))
CLOUD_SPRITES_2 = load_animation_frames("cloud_type2", "cloud", 4, (320, 200))

asteroid_image = None
try:
    raw_ast = pygame.image.load("asteriod.png").convert_alpha()
    asteroid_image = pygame.transform.scale(raw_ast, (90, 90))
except:
    print("Could not load asteroid image")

moon_image = None
try:
    raw_moon = pygame.image.load("moon.png").convert_alpha()
    moon_image = pygame.transform.scale(raw_moon, (50, 50))
except:
    print("Could not load moon.png")

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

try:
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
except:
    print("Could not load bg_music.mp3")

COL_BG       = (10,  10,  25)
COL_WHITE    = (255, 255, 255)
COL_PINK     = (255, 100, 200)

GALLERY_DIR = "gallery"
if os.path.exists(GALLERY_DIR):
    for f in os.listdir(GALLERY_DIR):
        if f.endswith('.png'):
            os.remove(os.path.join(GALLERY_DIR, f))
else:
    os.makedirs(GALLERY_DIR)

def load_gallery_images():
    images = []
    if os.path.exists(GALLERY_DIR):
        
        files = [f for f in os.listdir(GALLERY_DIR) if f.endswith('.png')]
        files.sort()
        for f in files:
            try:
                img = pygame.image.load(os.path.join(GALLERY_DIR, f)).convert_alpha()
                images.append(img)
            except:
                pass
    return images

saved_journeys = load_gallery_images()
COL_BLUE     = (100, 180, 255)
COL_YELLOW   = (255, 230, 100)
COL_TEAL     = (60,  220, 200)
CYAN         = (120, 255, 255)
COL_STAR     = (255, 255, 200)
BLACK        = (0, 0, 0)
COL_SKY_BLUE = (135, 206, 250)

CONSTELLATION_LINE_COLOR = (180, 180, 255, 255)
CONSTELLATION_STAR_COLOR = (255, 255, 180, 255)
CONSTELLATION_STAR_RADIUS = 18   

JOURNAL_MESSAGES = [
    "A spark of energy...", "Movement is life...", 
    "Capturing the flow...", "Clarity in speed..."
]

COLLECTION_QUOTES = [
    "Your feelings are valid. Take time to process them.",
    "Healing isn't linear. Every small step counts.",
    "It's okay to rest. You don't have to earn it.",
    "Asking for help is a sign of strength, not weakness.",
    "You don't have to carry everything alone.",
    "Progress isn't always visible. Trust the process.",
    "Your worth isn't tied to your productivity.",
    "It's okay to set boundaries. Protect your peace.",
    "You are enough, exactly as you are right now.",
    "Breathe. You've survived 100% of your worst days.",
    "Give yourself grace today. You're doing better than you think.",
    "It's okay to feel overwhelmed. Sit with it, then let it pass.",
    "Your mental health matters just as much as your physical health.",
    "You don't owe anyone your silence. Speak your truth.",
    "Take the next right step, not the whole staircase.",
    "Self-care isn't selfish. You can't pour from an empty cup.",
    "You're not broken. You're becoming.",
    "It's okay to say no. You don't have to explain yourself.",
    "Your struggles don't define you. Your resilience does.",
    "Some days just getting out of bed is a victory. Celebrate it.",
    "Don't let the noise of others drown out your inner voice.",
    "You are allowed to take up space. You are allowed to be seen.",
    "The way you talk to yourself matters. Be kind inside.",
    "Not all storms come to disrupt your life. Some come to clear your path.",
    "You are not your past. You are the sum of your choices today.",
    "It's okay to grieve what you thought your life would be.",
    "You deserve the same compassion you give to others.",
    "Growth is uncomfortable because you've never been this version of you before.",
    "Your pace is perfect for you. Don't compare your chapter one to someone else's chapter twenty.",
    "You don't have to be positive all the time. Real emotions are okay."
]

END_QUOTES = [
    "Mental health is not a destination, but a journey. Keep going.",
    "You've done enough today. That's more than enough.",
    "Rest is not a reward. It's a requirement.",
    "It's okay to not be okay. What matters is that you're still here.",
    "Healing takes time, and you're allowed to take all the time you need.",
    "You don't have to have everything figured out to move forward.",
    "Be gentle with yourself. You're doing the best you can.",
    "Your mind deserves the same care you give to others.",
    "This is just one chapter. The story continues to unfold.",
    "You've proven your strength today. Carry that with you.",
    "Sometimes the bravest thing is just showing up. You showed up.",
    "Every day is a fresh start. You get to try again tomorrow.",
    "You're not behind. You're exactly where you need to be.",
    "Your journey isn't over. This is just a moment of reflection.",
    "Celebrate how far you've come. The rest will follow.",
    "You've navigated the dark before. You'll find your way again.",
    "Progress is rarely a straight line. You're moving forward anyway.",
    "The world is better with you in it. Remember that always."
]
selected_quote = ""
journal_fade_alpha = 255
journal_fading_out = False

CHALLENGE_TIMES = {"EASY": 180, "MEDIUM": 120, "HARD": 60}
ASTEROID_SPEED_MULT = {"EASY": 1.0, "MEDIUM": 1.5, "HARD": 2.5}
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
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.x %= VIRTUAL_WORLD_SIZE
        self.y %= VIRTUAL_WORLD_SIZE
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
        self.is_collecting = False
        self.pop_scale = 1.0
        self.pop_alpha = 255
        self.frame_index = random.uniform(0, 3)
        self.anim_speed = 0.12 

    def start_collect(self):
        self.is_collecting = True
        self.pop_scale = 1.0
        self.pop_alpha = 255

    def update(self): 
        frames = NOTE_SPRITES if self.type == "note" else JOURNAL_SPRITES
        if frames:
            self.frame_index = (self.frame_index + self.anim_speed) % len(frames)
        
        if self.is_collecting:
            self.pop_scale += 0.06
            self.pop_alpha -= 8
            if self.pop_alpha <= 0:
                self.collected = True

    def draw(self, surface, scroll_x, scroll_y):
        if self.collected: return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        
        frames = NOTE_SPRITES if self.type == "note" else JOURNAL_SPRITES
        if frames:
            img = frames[int(self.frame_index)]
            if self.is_collecting:
                new_w = int(img.get_width() * self.pop_scale)
                new_h = int(img.get_height() * self.pop_scale)
                if new_w > 0 and new_h > 0:
                    scaled_img = pygame.transform.scale(img, (new_w, new_h))
                    img_copy = scaled_img.copy()
                    img_copy.set_alpha(max(0, int(self.pop_alpha)))
                    rect = img_copy.get_rect(center=(int(sx), int(sy)))
                    surface.blit(img_copy, rect)
                return

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
    def __init__(self, speed_mult=1.0):
        self.x, self.y = random.randint(0, VIRTUAL_WORLD_SIZE), random.randint(0, VIRTUAL_WORLD_SIZE)
        self.radius = random.randint(18, 35)
        self.active = True
        self.vx = random.uniform(-1.5, 1.5) * speed_mult
        self.vy = random.uniform(-1.5, 1.5) * speed_mult

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.x %= VIRTUAL_WORLD_SIZE
        self.y %= VIRTUAL_WORLD_SIZE

    def draw(self, surface, scroll_x, scroll_y):
        if not self.active: return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        if asteroid_image:
            rect = asteroid_image.get_rect(center=(int(sx), int(sy)))
            surface.blit(asteroid_image, rect)
        else:
            pygame.draw.circle(surface, (130, 120, 110), (int(sx), int(sy)), self.radius)
            pygame.draw.circle(surface, (90, 85, 80), (int(sx), int(sy)), self.radius, 2)

asteroid_shards = []

def create_asteroid_explosion(x, y):
    global asteroid_shards
    colors = [(130, 120, 110), (150, 140, 130), (100, 90, 80), (170, 160, 150)]
    for _ in range(16):
        asteroid_shards.append(AsteroidShard(x, y, random.choice(colors)))

class AsteroidShard:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(3, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.lifetime = 255
        self.size = random.randint(4, 10)
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-15, 15)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.96
        self.vy *= 0.96
        self.lifetime -= 8
        self.rotation += self.rot_speed

    def draw(self, surface, scroll_x, scroll_y):
        if self.lifetime <= 0: return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        a = max(0, int(self.lifetime))
        pygame.draw.polygon(s, (*self.color, a), [
            (self.size, 0),
            (self.size * 2, self.size),
            (self.size, self.size * 2),
            (0, self.size)
        ])
        rotated = pygame.transform.rotate(s, self.rotation)
        surface.blit(rotated, (int(sx - rotated.get_width() // 2), int(sy - rotated.get_height() // 2)))

class TinyPlanet:
    def __init__(self, color):
        self.x = self.y = VIRTUAL_WORLD_SIZE // 2
        self.color = list(color)
        self.target_color = list(color)
        self.saved_target_color = list(color)
        self.restore_color = False
        self.radius = 14
        self.extra_radius = 0
        self.boost_timer = 0
        self.neon_colors = [
            (0, 255, 255),  
            (180, 0, 255),   
            (0, 255, 100),   
            (255, 100, 255), 
            (255, 255, 0)    
        ]

    def update(self, target_wx, target_wy):
        prev_x, prev_y = self.x, self.y
        
        speed = 0.06
        if self.boost_timer > 0:
            self.boost_timer -= 1
            self.extra_radius = 12
            speed = 0.15
            
            t = self.boost_timer / 60.0
            index_f = (1 - t) * 5.0
            idx1 = int(index_f) % 5
            idx2 = (idx1 + 1) % 5
            frac = index_f - int(index_f)
            
            c1 = self.neon_colors[idx1]
            c2 = self.neon_colors[idx2]
            
            self.target_color = [
                c1[0] * (1-frac) + c2[0] * frac,
                c1[1] * (1-frac) + c2[1] * frac,
                c1[2] * (1-frac) + c2[2] * frac
            ]
            
            if self.boost_timer == 0:
                self.restore_color = True
        else:
            self.extra_radius = max(0, self.extra_radius - 0.6)
            if self.restore_color:
                self.target_color = list(self.saved_target_color)
                self.restore_color = False

        self.x += (target_wx - self.x) * speed
        self.y += (target_wy - self.y) * speed
        self.x %= VIRTUAL_WORLD_SIZE
        self.y %= VIRTUAL_WORLD_SIZE

        for i in range(3):
            self.color[i] += (self.target_color[i] - self.color[i]) * 0.07

        if abs(self.x - prev_x) < 400 and abs(self.y - prev_y) < 400:
            brush_color = (*[int(c) for c in self.color], TRAIL_ALPHA)
            thickness = int((self.radius + self.extra_radius) * 1.8)
            pygame.draw.line(canvas, brush_color, (prev_x, prev_y), (self.x, self.y), thickness)
            pygame.draw.circle(canvas, brush_color, (int(self.x), int(self.y)), thickness // 2)

    def draw(self, surface, scroll_x, scroll_y):
        bx, by = screen_pos(self.x, self.y, scroll_x, scroll_y)
        if moon_image:
            rect = moon_image.get_rect(center=(int(bx), int(by)))
            surface.blit(moon_image, rect)
        else:
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
    global asteroid_shards
    canvas.fill((0, 0, 0, 0)) 
    player = TinyPlanet(COL_YELLOW)
    
    speed_mult = ASTEROID_SPEED_MULT.get(challenge_difficulty, 1.0) if is_challenge_mode else 1.0
    asteroids = [Asteroid(speed_mult) for _ in range(50)]
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
    asteroid_shards = []
flash_alpha = 0

def draw_ui(orb_count):
    zone_y = HEIGHT - 70
    s = pygame.Surface((WIDTH, 70), pygame.SRCALPHA)
    s.fill((0, 0, 0, 190))
    screen.blit(s, (0, zone_y))
    info = font_tiny.render(f"ENERGY: HIGH | PROGRESS: {int(orb_count / 7 * 100)}% | S: SAVE | R: RESET | E: END", True, COL_YELLOW)
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

# JOURNAL
journal_background = pygame.image.load("bg start.png")
journal_background = pygame.transform.scale(journal_background, (WIDTH, HEIGHT))

book_image = pygame.image.load("buk.png")
book_image = pygame.transform.scale(book_image, (700, 450))

journal_font_title = pygame.font.SysFont("Roman", 42)
journal_font_text = pygame.font.SysFont("Times New Roman", 26)
journal_user_text = ""

journal_book_x = WIDTH // 2 - 350
journal_book_y = HEIGHT // 2 - 225

journal_left_x = journal_book_x + 60
journal_right_x = journal_book_x + 380
journal_start_y = journal_book_y + 90
journal_line_spacing = 26
journal_max_chars = 24
journal_max_lines_left = 10
journal_max_lines_right = 10

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
    
    title = journal_font_title.render("My Diary", True, COL_WHITE)
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
gallery_idx = 0

middle_box = pygame.Rect(200, 150, 600, 300)

diff_btn_w, diff_btn_h = 180, 75
diff_gap = 30
diff_total_w = diff_btn_w * 3 + diff_gap * 2
diff_start_x = (WIDTH - diff_total_w) // 2
diff_btn_y = HEIGHT // 2 - 50
diff_box = pygame.Rect(diff_start_x, diff_btn_y, diff_btn_w, diff_btn_h)
diff_medium = pygame.Rect(diff_start_x + diff_btn_w + diff_gap, diff_btn_y, diff_btn_w, diff_btn_h)
diff_hard = pygame.Rect(diff_start_x + (diff_btn_w + diff_gap) * 2, diff_btn_y, diff_btn_w, diff_btn_h)
diff_back_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 55)

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
                filename = f"{GALLERY_DIR}/journey_{int(time.time())}.png"
                pygame.image.save(canvas, filename)
                saved_journeys = load_gallery_images()

            if game_state == "JOURNAL":
                if event.key == pygame.K_BACKSPACE:
                    journal_user_text = journal_user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    journal_user_text += " "
                elif len(event.unicode) == 1:
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
                create_asteroid_explosion(a.x, a.y)
                if SND_ASTEROID: SND_ASTEROID.play()
                for _ in range(6): splashes.append(SplashParticle(a.x, a.y, (150, 150, 140)))
                shake_intensity = 12

                if is_challenge_mode:
                    score = max(0, score - 25)
                    for orb in orbs:
                        if orb.collected:
                            orb.collected = False
                            break

        for sym in all_symbols:
            sym.update() 
            if not sym.collected and not sym.is_collecting and wrapping_dist(player.x, player.y, sym.x, sym.y) < 50:
                sym.start_collect()
                if len(constellation_positions) == 0:
                    draw_first_constellation_star(sym.x, sym.y)

                constellation_positions.append((sym.x, sym.y))

                if len(constellation_positions) >= 2:
                    draw_constellation_on_canvas(constellation_positions)
                score += 15
                if sym.type == "journal":
                    if SND_JOURNAL: SND_JOURNAL.play()  
                    journal_msg, journal_timer = random.choice(COLLECTION_QUOTES), 300  # DURATION NG QUOTES
                elif sym.type == "note":
                    if SND_NOTE: SND_NOTE.play()

        for orb in orbs:
            orb.update()
            if not orb.collected and wrapping_dist(player.x, player.y, orb.x, orb.y) < 45:
                orb.collected = True
                player.boost_timer, score = 60, score + 10
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
        for sh in asteroid_shards[:]:
            sh.update()
            if sh.lifetime <= 0: asteroid_shards.remove(sh)
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
        for sh in asteroid_shards: sh.draw(screen, scroll_x, scroll_y)
        player.draw(screen, scroll_x, scroll_y)
        draw_ui(len([o for o in orbs if o.collected]))
        if is_challenge_mode and challenge_active:
            mins = int(time_remaining) // 60
            secs = int(time_remaining) % 60
            timer_col = COL_PINK if time_remaining < 15 else COL_TEAL
            timer_surf = font_medium.render(f"TIME: {mins}:{secs:02d}", True, timer_col)
            screen.blit(timer_surf, (WIDTH - timer_surf.get_width() - 30, 20))
        if journal_timer > 0:
            words = journal_msg.split()
            jq_lines = []
            current = ""
            for word in words:
                test = current + word + " "
                if font_small.size(test)[0] <= 520:
                    current = test
                else:
                    jq_lines.append(current)
                    current = word + " "
            jq_lines.append(current)

            j_line_h = 28
            jq_total_h = len(jq_lines) * j_line_h
            jq_box_h = jq_total_h + 30
            jq_box_w = 560
            jq_box_x = (WIDTH - jq_box_w) // 2
            jq_box_y = HEIGHT - jq_box_h - 110

            jq_surf = pygame.Surface((jq_box_w, jq_box_h), pygame.SRCALPHA)
            pygame.draw.rect(jq_surf, (135, 206, 250, 210), (0, 0, jq_box_w, jq_box_h), border_radius=12)
            screen.blit(jq_surf, (jq_box_x, jq_box_y))

            jq_start_y = jq_box_y + (jq_box_h - jq_total_h) // 2 + 5
            for j, jline in enumerate(jq_lines):
                jsurf = font_small.render(jline.strip(), True, (20, 30, 50))
                screen.blit(jsurf, jsurf.get_rect(center=(WIDTH // 2, jq_start_y + j_line_h * j)))
    
    elif game_state == "SUMMARY":
        screen.blit(journal_background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        orbs_collected = sum(1 for o in orbs if o.collected)
        title_text = "MISSION SUMMARY"
        title_color = CYAN
        if is_challenge_mode:
            won = orbs_collected == len(orbs)
            title_text = "CHALLENGE COMPLETE!" if won else "TIME'S UP!"
            title_color = COL_TEAL if won else COL_PINK

        layout_items = []
        title_h = 60
        box_h = middle_box.height
        btn_h = 65
        gap = 25

        if is_challenge_mode:
            score_h = 40
            total_h = title_h + gap + box_h + gap + score_h + gap + btn_h
            start_y = (HEIGHT - total_h) // 2
            title_y = start_y + title_h // 2
            box_y = start_y + title_h + gap
            score_y = box_y + box_h + gap + score_h // 2
            btn_y = score_y + score_h // 2 + gap
        else:
            total_h = title_h + gap + box_h + gap + btn_h
            start_y = (HEIGHT - total_h) // 2
            title_y = start_y + title_h // 2
            box_y = start_y + title_h + gap
            btn_y = box_y + box_h + gap

        draw_text_centered(title_text, font_large, title_color, title_y)

        middle_box.x = (WIDTH - middle_box.width) // 2
        middle_box.y = box_y
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

        if is_challenge_mode:
            pct = int(orbs_collected / len(orbs) * 100) if len(orbs) > 0 else 0
            pct_text = font_large.render(f"SCORE: {pct}%", True, COL_YELLOW)
            screen.blit(pct_text, pct_text.get_rect(center=(WIDTH // 2, score_y)))

        btn_w = 280
        total_btn_w = btn_w * 2 + 30
        btn_start_x = (WIDTH - total_btn_w) // 2

        back_btn_rect = pygame.Rect(btn_start_x, btn_y, btn_w, btn_h)
        play_btn_rect = pygame.Rect(btn_start_x + btn_w + 30, btn_y, btn_w, btn_h)

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
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))

        quote_font = pygame.font.SysFont("segoe ui", 28)
        max_width = 600
        
        words = selected_quote.split()
        lines = []
        current = ""
        for word in words:
            test = current + word + " "
            if quote_font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = word + " "
        lines.append(current)

        line_height = 40
        total_text_h = len(lines) * line_height
        box_pad = 50
        box_h = max(220, total_text_h + box_pad * 2)
        box_h = min(box_h, HEIGHT - 220)
        box_w = 700
        box_x = (WIDTH - box_w) // 2
        box_y = (HEIGHT - box_h) // 2
        
        quote_box = pygame.Rect(box_x, box_y, box_w, box_h)
        box_bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        pygame.draw.rect(box_bg, (240, 220, 120, 240), (0, 0, box_w, box_h), border_radius=30)
        screen.blit(box_bg, (box_x, box_y))
        draw_glow_rect(screen, quote_box, COL_YELLOW, 30, 4)

        text_center_y = box_y + box_h // 2
        text_total_h = (len(lines) - 1) * line_height
        first_line_y = text_center_y - text_total_h // 2

        for i, line in enumerate(lines):
            surf = quote_font.render(line.strip(), True, (25, 25, 25))
            screen.blit(surf, surf.get_rect(center=(WIDTH // 2, first_line_y + line_height * i)))

        continue_txt = font_medium.render("Click anywhere to continue...", True, (150, 150, 200))
        pulse = int(150 + 50 * math.sin(tick_count * 0.004))
        continue_txt = font_medium.render("Click anywhere to continue...", True, (pulse, pulse, 200))
        screen.blit(continue_txt, continue_txt.get_rect(center=(WIDTH//2, HEIGHT - 100)))

        if mouse_clicked:
            game_state = "JOURNAL"
    
    elif game_state == "MENU":
        screen.blit(journal_background, (0, 0))
        
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 185))
        screen.blit(ov, (0, 0))
        
        draw_text_centered("ECHO SKETCH: ENERGETIC FLOW", font_large, COL_PINK, HEIGHT//2 - 140)
        draw_text_centered("Guide the spark. Paint the void.", font_small, COL_WHITE, HEIGHT//2 - 80)
        draw_text_centered("Touch Clouds to shift colors.", font_tiny, (200, 200, 255), HEIGHT//2 - 30)
        draw_text_centered("Collect symbols to map constellations.", font_tiny, (200, 200, 255), HEIGHT//2)
        
        btn_rect = pygame.Rect(0, 0, 280, 70)
        btn_rect.center = (WIDTH // 2, HEIGHT // 2 + 70)
        is_hover = btn_rect.collidepoint(mx, my)
        pulse = (math.sin(tick_count * 0.005) + 1) / 2
        btn_col = COL_TEAL if is_hover else (int(60 + 40*pulse), int(180 + 40*pulse), int(160 + 40*pulse))
        
        pygame.draw.rect(screen, btn_col, btn_rect, border_radius=15)
        pygame.draw.rect(screen, COL_WHITE, btn_rect, 3, border_radius=15)
        draw_text_centered("PLAY", font_medium, COL_BG, HEIGHT // 2 + 70)
        
        if is_hover and mouse_clicked:
            game_state = "PLAYING"

        options_btn_rect = pygame.Rect(0, 0, 280, 70)
        options_btn_rect.center = (WIDTH // 2, HEIGHT // 2 + 170)
        op_hov = options_btn_rect.collidepoint(mx, my)
        op_col = COL_YELLOW if op_hov else (int(150 + 50 * math.sin(tick_count * 0.005)), 200, 100)
        
        pygame.draw.rect(screen, op_col, options_btn_rect, border_radius=15)
        pygame.draw.rect(screen, COL_WHITE, options_btn_rect, 3, border_radius=15)
        draw_text_centered("OPTIONS", font_medium, COL_BG, HEIGHT // 2 + 170)
        
        if op_hov and mouse_clicked:
            game_state = "OPTIONS"

    elif game_state == "OPTIONS":
        screen.blit(journal_background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        box_rect = pygame.Rect(WIDTH // 2 - 160, HEIGHT // 2 - 150, 320, 340)
        pygame.draw.rect(screen, (20, 30, 50), box_rect, border_radius=25)
        pygame.draw.rect(screen, COL_TEAL, box_rect, 4, border_radius=25)

        draw_text_centered("OPTIONS", title_font, COL_YELLOW, HEIGHT // 2 - 105)

        chal_opt_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 55)
        gal_opt_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 35, 200, 55)
        back_opt_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 110, 200, 55)

        for btn, txt, col in [(chal_opt_btn, "CHALLENGE", COL_PINK), (gal_opt_btn, "GALLERY", COL_BLUE), (back_opt_btn, "BACK", COL_TEAL)]:
            hov = btn.collidepoint(mx, my)
            c = tuple(min(255, x + 50) for x in col) if hov else col
            pygame.draw.rect(screen, c, btn, border_radius=12)
            pygame.draw.rect(screen, COL_WHITE, btn, 2, border_radius=12)
            draw_text_centered(txt, font_medium, COL_WHITE, btn.centery)

            if hov and mouse_clicked:
                if btn == chal_opt_btn:
                    game_state = "CHALLENGE_SELECT"
                elif btn == gal_opt_btn:
                    saved_journeys = load_gallery_images()
                    game_state = "GALLERY"
                elif btn == back_opt_btn:
                    game_state = "MENU"

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
            screen.blit(txt, txt.get_rect(center=(rect.centerx, rect.centery - 10)))
            sub = font_tiny.render(f"{CHALLENGE_TIMES[diff]}s", True, (200, 200, 200))
            screen.blit(sub, sub.get_rect(center=(rect.centerx, rect.centery + 15)))

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

    elif game_state == "GALLERY":
        screen.blit(journal_background, (0, 0))
        overlay_gal = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay_gal.fill((0, 0, 0, 220))
        screen.blit(overlay_gal, (0, 0))

        draw_text_centered("CANVAS GALLERY", title_font, COL_YELLOW, 60)

        if len(saved_journeys) > 0:
            img = saved_journeys[gallery_idx]
            
            box_w, box_h = 800, 450
            gallery_box = pygame.Rect((WIDTH - box_w) // 2, (HEIGHT - box_h) // 2, box_w, box_h)
            
            box_bg = pygame.Surface((box_w, box_h))
            box_bg.fill((8, 8, 20))
            screen.blit(box_bg, (gallery_box.x, gallery_box.y))
            
            draw_glow_rect(screen, gallery_box, CYAN, 25, 3)
            
            aspect = img.get_width() / img.get_height()
            pad = 15
            avail_w = box_w - 2 * pad
            avail_h = box_h - 2 * pad
            
            if img.get_width() * avail_h > avail_w * img.get_height():
                new_w = avail_w
                new_h = int(avail_w / aspect)
            else:
                new_h = avail_h
                new_w = int(avail_h * aspect)
            
            disp_img = pygame.transform.smoothscale(img, (new_w, new_h))
            screen.blit(disp_img, (gallery_box.x + (box_w - new_w) // 2, gallery_box.y + (box_h - new_h) // 2))
            
            arrow_l = pygame.Rect(WIDTH // 2 - 480, HEIGHT // 2 - 25, 50, 50)
            arrow_r = pygame.Rect(WIDTH // 2 + 430, HEIGHT // 2 - 25, 50, 50)
            
            l_col = COL_TEAL if arrow_l.collidepoint(mx, my) else (100, 100, 120)
            r_col = COL_TEAL if arrow_r.collidepoint(mx, my) else (100, 100, 120)
            
            draw_glow_rect(screen, arrow_l, l_col, 10, 2)
            draw_glow_rect(screen, arrow_r, r_col, 10, 2)
            
            l_txt = btn_font.render("<", True, COL_WHITE)
            r_txt = btn_font.render(">", True, COL_WHITE)
            screen.blit(l_txt, l_txt.get_rect(center=arrow_l.center))
            screen.blit(r_txt, r_txt.get_rect(center=arrow_r.center))
            
            if mouse_clicked:
                if arrow_l.collidepoint(mx, my):
                    gallery_idx = (gallery_idx - 1) % len(saved_journeys)
                if arrow_r.collidepoint(mx, my):
                    gallery_idx = (gallery_idx + 1) % len(saved_journeys)
        else:
            draw_text_centered("No saved journeys yet. Press 'S' to save!", font_medium, (150, 150, 200), HEIGHT // 2)

        gal_back_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 55)
        draw_glow_rect(screen, gal_back_btn, COL_PINK, 15, 2)
        gal_back_txt = font_medium.render("BACK", True, COL_WHITE)
        screen.blit(gal_back_txt, gal_back_txt.get_rect(center=gal_back_btn.center))
        if gal_back_btn.collidepoint(mx, my) and mouse_clicked:
            game_state = "MENU"

    if shake_offset_x != 0:
        scroll_x -= shake_offset_x
        scroll_y -= shake_offset_y

    pygame.display.flip()
    clock.tick(60)

pygame.quit()