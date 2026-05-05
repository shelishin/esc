# diary_book.py
import pygame


class DiaryBook:
    def __init__(self, width=1280, height=720):
        self.WIDTH = width
        self.HEIGHT = height

        # ---------------- LOAD IMAGES ----------------
        self.background = pygame.image.load("bg start.png")
        self.background = pygame.transform.scale(
            self.background, (self.WIDTH, self.HEIGHT)
        )

        self.book = pygame.image.load("color-de-papel.png")
        self.book = pygame.transform.scale(self.book, (700, 450))

        # ---------------- FONT ----------------
        self.title_font = pygame.font.SysFont("brush script", 42, True)
        self.text_font = pygame.font.SysFont("brush script", 30)

        # ---------------- COLORS ----------------
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # ---------------- TEXT ----------------
        self.user_text = ""

        # ---------------- BOOK POSITION ----------------
        self.book_x = self.WIDTH // 2 - 350
        self.book_y = self.HEIGHT // 2 - 225

        # Writing area inside book
        self.left_x = self.book_x + 55
        self.right_x = self.book_x + 375

        self.start_y = self.book_y + 70
        self.line_spacing = 30

        self.max_chars = 22
        self.max_lines_left = 9
        self.max_lines_right = 9

    # ---------------- WRAP TEXT ----------------
    def wrap_text(self, text):
        words = text.split(" ")
        lines = []
        current = ""

        for word in words:
            test = current + word + " "

            if len(test) <= self.max_chars:
                current = test
            else:
                lines.append(current)
                current = word + " "

        lines.append(current)
        return lines

    # ---------------- HANDLE INPUT ----------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]

            elif event.key == pygame.K_RETURN:
                self.user_text += " "

            else:
                self.user_text += event.unicode

    # ---------------- DRAW ----------------
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.book, (self.book_x, self.book_y))

        # Title
        title = self.title_font.render("My Diary", True, self.WHITE)
        screen.blit(title, (540, 50))

        # Wrap text
        lines = self.wrap_text(self.user_text)

        # LEFT PAGE
        y = self.start_y
        for i in range(min(len(lines), self.max_lines_left)):
            txt = self.text_font.render(lines[i], True, self.BLACK)
            screen.blit(txt, (self.left_x, y))
            y += self.line_spacing

        # RIGHT PAGE
        y = self.start_y
        for i in range(
            self.max_lines_left,
            min(len(lines), self.max_lines_left + self.max_lines_right),
        ):
            txt = self.text_font.render(lines[i], True, self.BLACK)
            screen.blit(txt, (self.right_x, y))
            y += self.line_spacing