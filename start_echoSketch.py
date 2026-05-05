import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1024, 576  # Match your image resolution
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Echo Sketch - Start Menu")

# Colors
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

# Fonts
# Ensure you have a clean sans-serif font
font_path = pygame.font.match_font('verdana', 'arial')
button_font = pygame.font.Font(font_path, 60)

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
    pygame.draw.rect(SCREEN, color, button_rect, border_thickness, border_radius=20)
    
    # Subtle "Glass" Overlay
    glass_surf = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    glass_surf.fill((255, 255, 255, 20)) # Very faint white
    SCREEN.blit(glass_surf, (rect_x, y_pos))

    # Render Text
    text_surf = button_font.render(text, True, color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    SCREEN.blit(text_surf, text_rect)

    return button_rect

def main_menu():
    run = True
    while run:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(BACKGROUND, (0, 0))

        # Draw Buttons
        play_btn = draw_button("play", 200, mouse_pos)
        options_btn = draw_button("options", 350, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if play_btn.collidepoint(mouse_pos):
            #         # print("Starting Game...")
            #         # Transition to your game loop here
            #     if options_btn.collidepoint(mouse_pos):
            #         # print("Opening Options...")

        pygame.display.update()

if __name__ == "__main__":
    main_menu()