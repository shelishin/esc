# journal123.py

import pygame

def run(screen, WIDTH, HEIGHT, journal_text):
    running = True

    font = pygame.font.SysFont("Courier New", 28)
    title_font = pygame.font.SysFont("arial", 45, bold=True)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "SUMMARY"
                if event.key == pygame.K_ESCAPE:
                    return "BACK"

        screen.fill((10, 10, 30))

        title = title_font.render("MY JOURNAL", True, (120, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        text = font.render(journal_text, True, (255, 255, 255))
        screen.blit(text, (100, 200))

        hint = font.render("ENTER = continue | ESC = back", True, (255, 230, 100))
        screen.blit(hint, (100, HEIGHT - 80))

        pygame.display.flip()