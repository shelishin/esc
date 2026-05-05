import pygame
import sys

# ---------------- INIT ----------------
pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Diary Book")

clock = pygame.time.Clock()

# ---------------- LOAD IMAGES ----------------
background = pygame.image.load("bg start.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

book = pygame.image.load("book.png")
book = pygame.transform.scale(book, (700, 450))

# ---------------- FONT ----------------
title_font = pygame.font.SysFont("brush script", 42, True)
text_font = pygame.font.SysFont("brush script", 30)

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ---------------- TEXT ----------------
user_text = ""

# ---------------- BOOK POSITION ----------------
book_x = WIDTH // 2 - 350
book_y = HEIGHT // 2 - 225

# Writing area inside book
left_x = book_x + 55
right_x = book_x + 375

start_y = book_y + 70
line_spacing = 30

max_chars = 22
max_lines_left = 9
max_lines_right = 9


# ---------------- WRAP TEXT ----------------
def wrap_text(text):
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


# ---------------- MAIN LOOP ----------------
running = True
while running:

    screen.blit(background, (0, 0))
    screen.blit(book, (book_x, book_y))

    # Title
    title = title_font.render("My Diary", True, WHITE)
    screen.blit(title, (540, 50))

    # Wrap text
    lines = wrap_text(user_text)

    # LEFT PAGE
    y = start_y
    for i in range(min(len(lines), max_lines_left)):
        txt = text_font.render(lines[i], True, BLACK)
        screen.blit(txt, (left_x, y))
        y += line_spacing

    # RIGHT PAGE
    y = start_y
    for i in range(max_lines_left, min(len(lines), max_lines_left + max_lines_right)):
        txt = text_font.render(lines[i], True, BLACK)
        screen.blit(txt, (right_x, y))
        y += line_spacing

    pygame.display.update()

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]

            elif event.key == pygame.K_RETURN:
                user_text += " "

            else:
                user_text += event.unicode

    clock.tick(60)

pygame.quit()
sys.exit()