import pygame
import sys

class Menu:
    def __init__(self, screen, W, H, BG_COLOR):
        self.screen = screen
        self.W = W
        self.H = H
        self.BG_COLOR = BG_COLOR

        self.font_title = pygame.font.Font("fonts/arcade.ttf", 108)
        self.font_button = pygame.font.Font("fonts/arcade2.ttf", 24)

        self.start_button = pygame.Rect(self.W // 2 - 150, self.H // 2 + 100, 300, 80)
        self.start_color = (200, 0, 0)
        self.hover_color = (255, 30, 30)

        self.title_fill = (255, 255, 255)
        self.title_outline = (200, 0, 0)
        self.button_text_color = (255, 255, 255)

    def draw_text_with_outline(self, text, font, x, y, fill_color, outline_color):
        base = font.render(text, True, fill_color)
        outline = font.render(text, True, outline_color)
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            self.screen.blit(outline, (x + dx, y + dy))
        self.screen.blit(base, (x, y))

    def draw(self):
        self.screen.fill(self.BG_COLOR)

        y_offset = self.H // 4 + 20
        x_center = self.W // 2

        title1 = "AVENTURAS"
        title2 = "CALLEJERAS"

        surf1 = self.font_title.render(title1, True, self.title_fill)
        surf2 = self.font_title.render(title2, True, self.title_fill)

        x1 = x_center - surf1.get_width() // 2
        x2 = x_center - surf2.get_width() // 2

        self.draw_text_with_outline(title1, self.font_title, x1, y_offset, self.title_fill, self.title_outline)
        self.draw_text_with_outline(title2, self.font_title, x2, y_offset + 90, self.title_fill, self.title_outline)

        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.start_button.collidepoint(mouse_pos)
        color = self.hover_color if is_hover else self.start_color
        text_color = (0, 0, 0) if is_hover else self.button_text_color

        pygame.draw.rect(self.screen, color, self.start_button)
        pygame.draw.rect(self.screen, (0, 0, 0), self.start_button, 3)
        
        text = self.font_button.render("Press Start", True, text_color)
        text_rect = text.get_rect(center=self.start_button.center)
        self.screen.blit(text, text_rect)
      
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    return True
        return False