import pygame
import config


class Display:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('fonts/Charge Vector Black.otf', 32)

    def show_score(self, score):
        score_text = self.font.render(f'Score: {score}', True, (240, 230, 100))
        self.screen.blit(score_text, (30, 30))

    def show_lives(self, lives):
        heart = pygame.image.load('images/heart.png')
        heart_width = heart.get_rect()[2]
        if lives > 0:
            self.screen.blit(heart, (30, 70))
        if lives > 1:
            self.screen.blit(heart, (35 + heart_width, 70))
        if lives > 2:
            self.screen.blit(heart, (40 + heart_width * 2, 70))

    def show_counter(self, counter):
        self.screen.blit(self.font.render(str(counter), True, (0, 0, 0)), (config.SCREEN_WIDTH - 100, 30))

    def show_game_over(self):
        text = self.font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2))
        self.screen.blit(text, text_rect)

    def times_up(self):
        text = self.font.render("Times UP", True, (255, 0, 0))
        text_rect = text.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2))
        self.screen.blit(text, text_rect)
