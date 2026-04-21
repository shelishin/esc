import pygame
import random
import math
import os

pygame.init()
pygame.mixer.init() 
WIDTH, HEIGHT      = 1000, 700
VIRTUAL_WORLD_SIZE = 5000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Echo Sketch")
clock = pygame.time.Clock()

PARALLAX_FACTOR = 0.3
EDGE_MARGIN     = 12

font_large  = pygame.font.SysFont("Courier New", 48, bold=True)
font_medium = pygame.font.SysFont("Courier New", 30, bold=True)
font_small  = pygame.font.SysFont("Courier New", 22)
font_tiny   = pygame.font.SysFont("Courier New", 18)

def load_sound(name):
    try:
        return pygame.mixer.Sound(name)
    except:
        return None

def play_sound(snd):
    if snd:
        snd.play()

SND_NOTE     = load_sound("note.wav")
SND_JOURNAL  = load_sound("journal.wav")
SND_ORB      = load_sound("orb.wav")
SND_CLOUD    = load_sound("cloud.wav")
SND_ASTEROID = load_sound("asteroid.wav")

SND_NOTE.set_volume(0.4)
SND_JOURNAL.set_volume(0.5)
SND_ORB.set_volume(0.6)
SND_CLOUD.set_volume(0.3)
SND_ASTEROID.set_volume(0.5)

COL_BG       = (10,  10,  25)
COL_WHITE    = (255, 255, 255)
COL_PINK     = (255, 100, 200)
COL_BLUE     = (100, 180, 255)
COL_YELLOW   = (255, 230, 100)
COL_TEAL     = (60,  220, 200)
COL_ORANGE   = (255, 160, 60)
COL_LAVENDER = (180, 140, 255)

MOOD_SETTINGS = {
    "low": {
        "trail_len":    110,
        "base_radius":  28,
        "colors":       [COL_BLUE, (80, 120, 255), (120, 80, 255)],
        "alpha_floor":  80,
        "label":        "Low Energy / Calm",
        "desc":         "Slow, deep blues, thick lines",
    },
    "balanced": {
        "trail_len":    70,
        "base_radius":  20,
        "colors":       [COL_PINK, COL_TEAL, COL_LAVENDER],
        "alpha_floor":  50,
        "label":        "Balanced",
        "desc":         "Medium pace, mixed palette",
    },
    "high": {
        "trail_len":    38,
        "base_radius":  13,
        "colors":       [COL_YELLOW, COL_ORANGE, (255, 255, 80)],
        "alpha_floor":  25,
        "label":        "High Energy / Anxious",
        "desc":         "Fast, bright yellows, thin lines",
    },
}

JOURNAL_MESSAGES = [
    "A new thought transcribed...",
    "Feelings put into words...",
    "Your story continues...",
    "Reflection captured...",
    "A moment of clarity...",
]

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
    if sx > WIDTH  + 100: sx -= VIRTUAL_WORLD_SIZE
    if sy > HEIGHT + 100: sy -= VIRTUAL_WORLD_SIZE
    return sx, sy

def draw_text_centered(text, font, color, y_center):
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center=(WIDTH // 2, y_center)))


def vibe_check_screen(bg_tile, t_w, t_h):
    tick = 0
    while True:
        tick += 1
        screen.fill(COL_BG)
       
        ox = int(-(tick * 0.3) % t_w)
        oy = int(-(tick * 0.15) % t_h)
        for tx in range(-1, (WIDTH // t_w) + 2):
            for ty in range(-1, (HEIGHT // t_h) + 2):
                screen.blit(bg_tile, (tx * t_w + ox, ty * t_h + oy))

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        draw_text_centered("VIBE CHECK", font_large, COL_PINK, 100)
        draw_text_centered("How are you feeling right now?", font_small, (180, 180, 220), 165)

        keys = ["1", "2", "3"]
        moods = ["low", "balanced", "high"]
        for i, (k, m) in enumerate(zip(keys, moods)):
            ms  = MOOD_SETTINGS[m]
            y   = 260 + i * 110
            col = ms["colors"][0]
            pygame.draw.rect(screen, (*col, 60),
                             pygame.Rect(WIDTH//2 - 280, y - 32, 560, 68),
                             border_radius=12)
            pygame.draw.rect(screen, col,
                             pygame.Rect(WIDTH//2 - 280, y - 32, 560, 68),
                             width=2, border_radius=12)
            draw_text_centered(f"{k}  —  {ms['label']}", font_medium, COL_WHITE,   y - 8)
            draw_text_centered(ms["desc"],                 font_tiny,   (160,160,200), y + 24)

        pulse = (math.sin(tick * 0.05) + 1) / 2
        pc    = (int(200 + 55 * pulse), int(200 + 55 * pulse), int(80 + 60 * pulse))
        draw_text_centered("Press 1, 2 or 3 to begin", font_tiny, pc, HEIGHT - 45)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: return "low"
                if event.key == pygame.K_2: return "balanced"
                if event.key == pygame.K_3: return "high"


class SplashParticle:
    def __init__(self, x, y, color, is_big=False, is_rock=False):
        self.x, self.y = x, y
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(4, 8) if is_rock else (random.uniform(1, 4) if is_big else random.uniform(3, 7))
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color    = color
        self.lifetime = 255
        self.size     = random.randint(3, 6) if is_rock else (random.randint(8, 15) if is_big else random.randint(2, 5))
        self.is_big   = is_big
        self.is_rock  = is_rock

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 10 if self.is_rock else (4 if self.is_big else 7)
        self.size *= 0.95

    def draw(self, surface, scroll_x, scroll_y):
        if self.lifetime <= 0: return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        r = max(1, int(self.size))
        s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, max(0, self.lifetime)), (r, r), r)
        surface.blit(s, (int(sx - r), int(sy - r)))


class Cloud:
    def __init__(self, unlockable_color=None):
        self.x = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.y = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.base_color     = [220, 220, 255]
        self.current_color  = list(self.base_color)
        self.target_color   = list(self.base_color)
        self.fluff_blobs    = [{'ox': random.randint(-35, 35),
                                'oy': random.randint(-25, 25),
                                'r':  random.randint(25, 45)} for _ in range(6)]
        self.collision_radius = 60
        self.gathered         = False
        self.unlockable_color = unlockable_color  

    def hit(self, particle_list):
        new_color = list(self.unlockable_color) if self.unlockable_color else \
                    [random.randint(80, 255) for _ in range(3)]
        new_color[random.randint(0, 2)] = 255
        self.target_color = new_color
        self.gathered     = True
        for _ in range(5):  particle_list.append(SplashParticle(self.x, self.y, new_color, is_big=True))
        for _ in range(15): particle_list.append(SplashParticle(self.x, self.y, new_color))

    def update(self):
        for i in range(3):
            self.current_color[i] += (self.target_color[i] - self.current_color[i]) * 0.15
        for i in range(3):
            self.target_color[i]  += (self.base_color[i]   - self.target_color[i])  * 0.015

    def draw(self, surface, scroll_x, scroll_y):
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        for b in self.fluff_blobs:
            pos = (int(sx + b['ox']), int(sy + b['oy']))
            r   = b['r']
            s   = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            alpha = 100 + (100 if self.gathered else 0)
            pygame.draw.circle(s, (*[int(c) for c in self.current_color], min(200, alpha)),
                               (r, r), r)
            surface.blit(s, (pos[0]-r, pos[1]-r))
        
        if self.gathered:
            pygame.draw.circle(surface, COL_WHITE, (int(sx), int(sy)), 5)


class InspirationSymbol:
    COLORS = {"note": COL_PINK, "journal": COL_YELLOW}

    def __init__(self, sym_type):
        self.x         = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.y         = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.type      = sym_type
        self.collected = False
        self.radius    = 20
        self.pulse     = random.uniform(0, math.pi * 2)
        self.world_pos = (self.x, self.y)

    def update(self):
        self.pulse = (self.pulse + 0.05) % (math.pi * 2)

    def draw(self, surface, scroll_x, scroll_y):
        if self.collected: return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        col  = self.COLORS[self.type]
        r    = self.radius + int(math.sin(self.pulse) * 4)
        glow = pygame.Surface((r*4, r*4), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*col, 40), (r*2, r*2), r*2)
        pygame.draw.circle(glow, (*col, 160),(r*2, r*2), r)
        surface.blit(glow, (int(sx - r*2), int(sy - r*2)))
        
        if self.type == "note":
            pygame.draw.circle(surface, COL_WHITE, (int(sx), int(sy)), 6)
        else:
            pygame.draw.rect(surface, COL_WHITE,
                             pygame.Rect(int(sx)-8, int(sy)-8, 16, 16), border_radius=3)

    def check_collision(self, px, py):
        if not self.collected and wrapping_dist(px, py, self.x, self.y) < self.radius + 18:
            self.collected = True
            return True
        return False


class SupportOrb:
    def __init__(self):
        self.x         = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.y         = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.collected = False
        self.pulse     = random.uniform(0, math.pi * 2)

    def update(self):
        self.pulse = (self.pulse + 0.07) % (math.pi * 2)

    def draw(self, surface, scroll_x, scroll_y):
        if self.collected: return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        r = 16 + int(math.sin(self.pulse) * 4)
        g = pygame.Surface((r*3, r*3), pygame.SRCALPHA)
        pygame.draw.circle(g, (255, 200, 80,  50), (r+r//2, r+r//2), r + r//2)
        pygame.draw.circle(g, (255, 220, 120, 200),(r+r//2, r+r//2), r)
        surface.blit(g, (int(sx - r - r//2), int(sy - r - r//2)))

    def check_collision(self, px, py):
        if not self.collected and wrapping_dist(px, py, self.x, self.y) < 22:
            self.collected = True
            return True
        return False


class Asteroid:
    def __init__(self):
        self.x      = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.y      = random.randint(0, VIRTUAL_WORLD_SIZE)
        self.radius = random.randint(15, 30)
        self.color  = (120, 110, 100)
        self.active = True

    def hit(self, particle_list):
        self.active = False
        for _ in range(12):
            particle_list.append(SplashParticle(self.x, self.y, (120, 110, 100), is_rock=True))

    def draw(self, surface, scroll_x, scroll_y):
        if not self.active: return
        sx, sy = screen_pos(self.x, self.y, scroll_x, scroll_y)
        pygame.draw.circle(surface, self.color, (int(sx), int(sy)), self.radius)
        pygame.draw.circle(surface, (80, 75, 70), (int(sx), int(sy)), self.radius, 2)


class TinyPlanet:
    def __init__(self, base_color):
        self.x = self.y = VIRTUAL_WORLD_SIZE // 2
        self.base_color   = base_color
        self.radius       = 18
        self.trail        = []       
        self.trail_length = 70
        self.hue          = 0
        self.extra_radius = 0        
        self.extra_timer  = 0

    def update(self, target_wx, target_wy, mood_settings, unlocked_colors, color_idx):
        self.trail.append((self.x, self.y, unlocked_colors[color_idx]))
        if len(self.trail) > mood_settings["trail_len"]:
            self.trail.pop(0)
        self.x += (target_wx - self.x) * 0.04
        self.y += (target_wy - self.y) * 0.04
        self.x %= VIRTUAL_WORLD_SIZE
        self.y %= VIRTUAL_WORLD_SIZE
        self.hue = (self.hue + 2) % 360
        if self.extra_timer > 0:
            self.extra_timer -= 1
        else:
            self.extra_radius = max(0, self.extra_radius - 1)

    def boost(self):
        self.extra_radius = 14
        self.extra_timer  = 180

    def draw(self, surface, scroll_x, scroll_y, mood_settings):
        tl  = len(self.trail)
        btr = mood_settings["base_radius"] + self.extra_radius
        for i, (wx, wy, col) in enumerate(self.trail):
            t      = i / max(tl, 1)
            radius = max(1, int(btr * (0.15 + 0.85 * t)))
            alpha  = max(mood_settings["alpha_floor"], int(220 * t))
            sx, sy = screen_pos(wx, wy, scroll_x, scroll_y)
            ps     = radius * 2
            s      = pygame.Surface((ps, ps), pygame.SRCALPHA)
            pygame.draw.circle(s, (*col, alpha), (radius, radius), radius)
            surface.blit(s, (int(sx - radius), int(sy - radius)))
        
        bx, by = screen_pos(self.x, self.y, scroll_x, scroll_y)
        pygame.draw.circle(surface, self.base_color, (int(bx), int(by)), self.radius)
        pygame.draw.circle(surface, COL_WHITE,       (int(bx), int(by)), self.radius, 2)
    
        if self.extra_radius > 0:
            gs = pygame.Surface(((self.radius+10)*2, (self.radius+10)*2), pygame.SRCALPHA)
            pygame.draw.circle(gs, (255, 220, 80, 80),
                               (self.radius+10, self.radius+10), self.radius+10)
            surface.blit(gs, (int(bx - self.radius - 10), int(by - self.radius - 10)))



def load_custom_bg(filename):
    if os.path.exists(filename):
        try:
            base = pygame.image.load(filename).convert()
            w, h = base.get_size()
            img  = pygame.transform.smoothscale(base, (600, int(h * (600 / w))))
            w, h = img.get_size()
            mega = pygame.Surface((w*2, h*2))
            mega.blit(img, (0, 0))
            mega.blit(pygame.transform.flip(img, True,  False), (w, 0))
            mega.blit(pygame.transform.flip(img, False, True),  (0, h))
            mega.blit(pygame.transform.flip(img, True,  True),  (w, h))
            return mega
        except: pass
    f = pygame.Surface((400, 400)); f.fill((10, 15, 35))
    return f


def draw_expression_zone(surface, collected_notes, collected_journals, score,
                         max_score, mood, unlocked_colors, orb_count):
    zone_h = 70
    zone_y = HEIGHT - zone_h
    bg     = pygame.Surface((WIDTH, zone_h), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 160))
    surface.blit(bg, (0, zone_y))
    pygame.draw.line(surface, (100, 80, 160), (0, zone_y), (WIDTH, zone_y), 1)

    
    icon_x = 16
    for _ in range(collected_notes):
        pygame.draw.circle(surface, COL_PINK,   (icon_x, zone_y + 22), 8)
        pygame.draw.circle(surface, COL_WHITE,  (icon_x, zone_y + 22), 3)
        icon_x += 20
    for _ in range(collected_journals):
        pygame.draw.rect(surface, COL_YELLOW,
                         pygame.Rect(icon_x - 7, zone_y + 14, 14, 14), border_radius=2)
        icon_x += 20

    
    orb_label = font_tiny.render(f"Orbs: {orb_count}", True, (255, 220, 80))
    surface.blit(orb_label, (icon_x + 8, zone_y + 14))

    
    pct    = min(score / max(max_score, 1), 1.0)
    bar_x  = 16
    bar_y  = zone_y + 44
    bar_w  = 320
    bar_h  = 10
    pygame.draw.rect(surface, (50, 40, 80), (bar_x, bar_y, bar_w, bar_h), border_radius=5)
    pygame.draw.rect(surface, COL_PINK,     (bar_x, bar_y, int(bar_w * pct), bar_h), border_radius=5)
    score_lbl = font_tiny.render(f"Constellation  {score} / {max_score}", True, COL_WHITE)
    surface.blit(score_lbl, (bar_x + bar_w + 10, bar_y - 2))

   
    mood_col = {"low": COL_BLUE, "balanced": COL_TEAL, "high": COL_YELLOW}[mood]
    mb = font_tiny.render(f"Vibe: {mood.upper()}", True, mood_col)
    surface.blit(mb, (WIDTH - mb.get_width() - 16, zone_y + 14))

    
    for ci, col in enumerate(unlocked_colors):
        cx = WIDTH - 16 - ci * 22
        pygame.draw.circle(surface, col, (cx, zone_y + 50), 8)

    
    hint = font_tiny.render("S = save  |  R = reset  |  Click = cycle color", True, (80, 80, 120))
    surface.blit(hint, (WIDTH // 2 - hint.get_width() // 2, zone_y + 50))



def draw_constellation(surface, positions, scroll_x, scroll_y):
    if len(positions) < 2: return
    screen_pts = [screen_pos(wx, wy, scroll_x, scroll_y) for wx, wy in positions]
    for i in range(len(screen_pts) - 1):
        p1, p2 = screen_pts[i], screen_pts[i+1]
        line_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(line_surf, (200, 200, 255, 55), p1, p2, 1)
        surface.blit(line_surf, (0, 0))
    for pt in screen_pts:
        pygame.draw.circle(surface, (200, 200, 255), pt, 3)



bg_tile = load_custom_bg('111-1.png')
t_w, t_h = bg_tile.get_size()


mood          = vibe_check_screen(bg_tile, t_w, t_h)
mood_settings = MOOD_SETTINGS[mood]

unlocked_colors = list(mood_settings["colors"])
color_idx       = 0

player    = TinyPlanet(COL_TEAL)
asteroids = [Asteroid() for _ in range(40)]


extra_colors = [COL_ORANGE, COL_LAVENDER, (80, 255, 140), (255, 80, 80)]
clouds = [Cloud(unlockable_color=random.choice(extra_colors)) for _ in range(20)]


notes    = [InspirationSymbol("note")    for _ in range(12)]
journals = [InspirationSymbol("journal") for _ in range(5)]
all_symbols = notes + journals


orbs = [SupportOrb() for _ in range(6)]

splashes = []
scroll_x = scroll_y = 0

constellation_positions = []  
collected_notes    = 0
collected_journals = 0
collected_orbs     = 0
score              = 0
MAX_SCORE          = 12 * 10 + 5 * 20 + 6 * 5   

show_journal_text  = False
journal_timer      = 0
journal_message    = ""
edge_flash_timer   = 0
save_flash_timer   = 0
orb_flash_timer    = 0
tick               = 0

game_state = "MENU"

running = True
while running:
    tick += 1
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == "MENU":
                game_state = "PLAYING"
            if event.key == pygame.K_s and game_state == "PLAYING":
                pygame.image.save(screen, "my_journey.png")
                save_flash_timer = 100
            if event.key == pygame.K_r and game_state == "PLAYING":
               
                mood          = vibe_check_screen(bg_tile, t_w, t_h)
                mood_settings = MOOD_SETTINGS[mood]
                unlocked_colors = list(mood_settings["colors"])
                color_idx       = 0
                player          = TinyPlanet(COL_TEAL)
                asteroids       = [Asteroid() for _ in range(40)]
                clouds          = [Cloud(unlockable_color=random.choice(extra_colors)) for _ in range(20)]
                notes           = [InspirationSymbol("note")    for _ in range(12)]
                journals        = [InspirationSymbol("journal") for _ in range(5)]
                all_symbols     = notes + journals
                orbs            = [SupportOrb() for _ in range(6)]
                splashes.clear()
                constellation_positions.clear()
                collected_notes = collected_journals = collected_orbs = score = 0
                edge_flash_timer = save_flash_timer = orb_flash_timer = 0
                show_journal_text = False
                game_state = "MENU"

        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "PLAYING":
            color_idx = (color_idx + 1) % len(unlocked_colors)

    
    if game_state == "PLAYING":

     
        target_wx = mx + scroll_x
        target_wy = my + scroll_y
        player.update(target_wx, target_wy, mood_settings, unlocked_colors, color_idx)

       
        scroll_x = player.x - WIDTH  // 2
        scroll_y = player.y - HEIGHT // 2

        
        for c in clouds:
            if not c.gathered:
                if wrapping_dist(player.x, player.y, c.x, c.y) < c.collision_radius + player.radius:
                    c.hit(splashes)
                    play_sound(SND_CLOUD)  
                    if c.unlockable_color and c.unlockable_color not in unlocked_colors:
                        unlocked_colors.append(c.unlockable_color)
            c.update()

        
        for sym in all_symbols:
            sym.update()
            if sym.check_collision(player.x, player.y):
                constellation_positions.append((sym.x, sym.y))
                if sym.type == "note":
                    score += 10; collected_notes += 1
                else:
                    score += 20; collected_journals += 1
                    play_sound(SND_JOURNAL)  
                    show_journal_text = True
                    journal_timer     = 130
                    journal_message   = random.choice(JOURNAL_MESSAGES)

        if show_journal_text:
            journal_timer -= 1
            if journal_timer <= 0:
                show_journal_text = False

  
        for orb in orbs:
            orb.update()
            if orb.check_collision(player.x, player.y):
                score += 5; collected_orbs += 1
                player.boost()
                orb_flash_timer = 90
                play_sound(SND_ORB)  

        if orb_flash_timer > 0: orb_flash_timer -= 1

 
        for a in asteroids:
            if a.active and wrapping_dist(player.x, player.y, a.x, a.y) < a.radius + player.radius:
                a.hit(splashes)
                play_sound(SND_ASTEROID)  

        for s in splashes[:]:
            s.update()
            if s.lifetime <= 0: splashes.remove(s)

        if mx <= EDGE_MARGIN or mx >= WIDTH - EDGE_MARGIN or \
           my <= EDGE_MARGIN or my >= HEIGHT - EDGE_MARGIN:
            edge_flash_timer = 18
        if edge_flash_timer > 0: edge_flash_timer -= 1

      
        if save_flash_timer > 0: save_flash_timer -= 1

    screen.fill(COL_BG)

    ox = int(-(scroll_x * PARALLAX_FACTOR) % t_w)
    oy = int(-(scroll_y * PARALLAX_FACTOR) % t_h)
    for tx in range(-1, (WIDTH // t_w) + 2):
        for ty in range(-1, (HEIGHT // t_h) + 2):
            screen.blit(bg_tile, (tx * t_w + ox, ty * t_h + oy))

    if game_state == "PLAYING":

        
        if edge_flash_timer > 0:
            alpha = int(edge_flash_timer / 18 * 55)
            ef = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ef.fill((160, 210, 255, alpha))
            screen.blit(ef, (0, 0))

        draw_constellation(screen, constellation_positions, scroll_x, scroll_y)

       
        for a   in asteroids: a.draw(screen, scroll_x, scroll_y)
        for c   in clouds:    c.draw(screen, scroll_x, scroll_y)
        for sym in all_symbols: sym.draw(screen, scroll_x, scroll_y)
        for orb in orbs:      orb.draw(screen, scroll_x, scroll_y)
        for s   in splashes:  s.draw(screen, scroll_x, scroll_y)

        player.draw(screen, scroll_x, scroll_y, mood_settings)

      
        draw_expression_zone(screen, collected_notes, collected_journals,
                             score, MAX_SCORE, mood,
                             unlocked_colors, collected_orbs)

       
        if show_journal_text:
            txt  = font_medium.render(journal_message, True, COL_WHITE)
            trct = txt.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            bgs  = pygame.Surface((trct.width + 28, trct.height + 14), pygame.SRCALPHA)
            bgs.fill((0, 0, 0, 170))
            screen.blit(bgs, (trct.x - 14, trct.y - 7))
            screen.blit(txt, trct)

        
        if save_flash_timer > 0:
            sv = font_small.render("Journey saved as  my_journey.png!", True, (120, 255, 180))
            screen.blit(sv, sv.get_rect(center=(WIDTH // 2, 36)))

       
        if orb_flash_timer > 0:
            ob = font_small.render("Support boost active!", True, (255, 220, 80))
            screen.blit(ob, ob.get_rect(topright=(WIDTH - 16, 16)))

       
        all_done = all(sym.collected for sym in all_symbols)
        if all_done:
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ov.fill((8, 6, 24, 190))
            screen.blit(ov, (0, 0))
            draw_text_centered("Constellation Complete!", font_large, COL_YELLOW, HEIGHT // 2 - 50)
            draw_text_centered(f"Final score: {score}   —   S to save  |  R to restart",
                               font_small, COL_WHITE, HEIGHT // 2 + 20)

    else:
        
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 175))
        screen.blit(ov, (0, 0))

        draw_text_centered("ECHO SKETCH: VIBE FLOW", font_large,  COL_PINK,  HEIGHT//2 - 130)
        draw_text_centered("Move Mouse to guide the Spark", font_small, COL_WHITE, HEIGHT//2 - 50)
        draw_text_centered("Float through Clouds to unlock new trail colors", font_small, COL_WHITE, HEIGHT//2 - 10)
        draw_text_centered("Collect Inspiration Symbols to form Constellations", font_small, COL_WHITE, HEIGHT//2 + 30)
        draw_text_centered("Touch Support Orbs (gold) to glow brighter", font_small, COL_WHITE, HEIGHT//2 + 70)
        draw_text_centered("Shatter Asteroids by passing through them",font_small, COL_WHITE, HEIGHT//2 + 110)
        draw_text_centered("Click to cycle trail color  |  S = save  |  R = reset", font_tiny, (120, 120, 180), HEIGHT//2 + 155)

        pulse      = (math.sin(tick * 0.05) + 1) / 2
        pc         = (int(200 + 55*pulse), int(200 + 55*pulse), int(80 + 60*pulse))
        draw_text_centered("[ PRESS SPACE TO BEGIN ]", font_medium, pc, HEIGHT//2 + 210)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
