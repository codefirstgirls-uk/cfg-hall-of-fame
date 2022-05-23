import pygame
import database_functions as dbf
from config import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.font.init()
width, height = SCREEN_WIDTH, SCREEN_HEIGHT
win = pygame.display.set_mode((width, height))
back_color = (255, 250, 240)


def main(player_id):
    background_image = pygame.image.load("background_new.jpg")
    picture = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # most recent score button
    recent_score_button = pygame.Rect((width)/9, height/5, 200, 30)
    # top scores
    top_score_button = pygame.Rect((width*4)/9, height/5, 200, 30)
    # user score
    user_score_button = pygame.Rect((width*6)/9, height/5, 200, 30)
    # return button
    return_button = pygame.Rect(800, 10, 200, 30)
    refresh = True
    scores = []
    # main loop
    while refresh:

        win.blit(picture, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                refresh = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if recent_score_button.collidepoint(event.pos):
                    scores = dbf.get_recent_scores(10)
                if top_score_button.collidepoint(event.pos):
                    scores = dbf.get_top_scores(10)
                if user_score_button.collidepoint(event.pos):
                    if player_id:
                        scores = dbf.get_user_scores(player_id)
                    else:
                        scores = [('Login to see user high scores', '', '')]
                if return_button.collidepoint(event.pos):
                    return

        welcome_font = pygame.font.Font('Square One Bold.ttf', 64)
        name = welcome_font.render('High Scores', True, (200, 100, 100))
        win.blit(name, ((width/2)-200, height/12))

        font = pygame.font.Font('Charge Vector Black.otf', 32)
        for index, score in enumerate(scores):
            score_string = score[0].ljust(20) + str(score[1]).ljust(20) + score[2].ljust(20)
            entry = font.render(score_string, True, (240, 230, 100))
            win.blit(entry, (width/9, height/5 + 50 + (index*30)))

        pygame.draw.rect(win, pygame.Color((100, 100, 100)), recent_score_button, 1)
        recent_score_surface = font.render('Recent Scores', True, (240, 230, 100))
        recent_score_button.w = recent_score_surface.get_width()
        win.blit(recent_score_surface, (recent_score_button.x, recent_score_button.y))

        pygame.draw.rect(win, pygame.Color((100, 100, 100)), top_score_button, 1)
        top_score_surface = font.render('Top Scores', True, (240, 230, 100))
        top_score_button.w = top_score_surface.get_width()
        win.blit(top_score_surface, (top_score_button.x, top_score_button.y))

        pygame.draw.rect(win, pygame.Color((100, 100, 100)), user_score_button, 1)
        user_score_surface = font.render('User Scores', True, (240, 230, 100))
        user_score_button.w = user_score_surface.get_width()
        win.blit(user_score_surface, (user_score_button.x, user_score_button.y))

        pygame.draw.rect(win, pygame.Color((100, 100, 100)), return_button, 1)
        return_surface = font.render('Main Menu', True, (240, 230, 100))
        return_button.w = return_surface.get_width()
        win.blit(return_surface, (return_button.x, return_button.y))

        pygame.display.update()
    return

