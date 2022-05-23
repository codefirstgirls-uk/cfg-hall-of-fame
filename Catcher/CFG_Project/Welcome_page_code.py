import pygame
import database_functions as dbf
import catcher as ct
import highscorepage
from config import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.font.init()
width, height = SCREEN_WIDTH, SCREEN_HEIGHT
win = pygame.display.set_mode((width, height))
back_color = (255, 250, 240)
pygame.init()

paster_blue = (174, 198, 207)
def main():
    # initialize variables
    player_id = 0
    username = None
    user_text = 'Enter Name'
    user_first_input = False
    # prepare rectangles to be drawn else it throws a warning
    input_rect = pygame.Rect(400, 530, 140, 32)
    login_button = pygame.Rect(420, 600, 100, 30)
    highscore_button = pygame.Rect(800, 10, 205, 30)

    input_box_active = False
    logged_in = False

    login_button_text = 'Login'
    refresh = True
    # main loop
    while refresh:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                refresh = False
                break
            # mouse up to prevent instant clicks
            if event.type == pygame.MOUSEBUTTONUP:
                print(pygame.mouse.get_pos())
                # if mouse intersects input box, also acts as the logout button too, when logged in
                if input_rect.collidepoint(event.pos):
                    if logged_in:
                        logged_in = False
                        player_id = 0
                        username = None
                        login_button_text = 'Login'
                        user_text = ''
                    else:
                        # not logged in, so name input box
                        input_box_active = True
                else:
                    # if any click is outside this box, input box deactivates
                    input_box_active = False

                # login button, doubles as play button when logged in
                if login_button.collidepoint(event.pos):
                    if logged_in:
                        # play button action
                        ct.main(player_id)

                    # login button action
                    else:
                        if user_first_input and user_text:
                            username = user_text
                            player_id = dbf.login(username)
                            login_button_text = 'Play'
                            logged_in = True
                if highscore_button.collidepoint(event.pos):
                    highscorepage.main(player_id)

            if event.type == pygame.KEYDOWN and input_box_active:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                # Unicode standard is used for string
                # formation
                else:
                    if len(user_text) < 10:
                        user_text += event.unicode

        background_image = pygame.image.load("images/background.jpg")
        picture = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))



        win.blit(picture, (0, 0))
        # pygame.display.update()
        title_font = pygame.font.Font('fonts/Charge Vector Black.otf', 64)
        name = title_font.render('Catcher', True, (240, 230, 100))
        win.blit(name, (320, 300))

        welcome_font = pygame.font.Font('fonts/Square One Bold.ttf', 120)
        name = welcome_font.render('Welcome', True, (200, 100, 100))
        win.blit(name, (220, 150))

        start = pygame.image.load("images/start2.png")
        picture1 = pygame.transform.scale(start, (100, 100))
        win.blit(picture1, (420, 400))

        boy = pygame.image.load("images/boy.png")
        boy_scaled = pygame.transform.scale(boy, (150, 150))
        win.blit(boy_scaled, (600, 500))

        coin = pygame.image.load("images/coin.png")
        coin_scaled = pygame.transform.scale(coin, (30, 30))
        win.blit(coin_scaled, (770, 470))

        if logged_in:
            # display information about the logged in user
            font = pygame.font.Font('fonts/Charge Vector Black.otf', 32)
            user_id = font.render('Player ID : {}'.format(player_id), True, (240, 230, 100))
            user_username = font.render('Username : {}'.format(username), True, (240, 230, 100))
            user_topscore = font.render('Top Score : {}'.format(dbf.get_user_top_score(player_id)), True,
                                        (240, 230, 100))
            win.blit(user_id, (100, 525))
            win.blit(user_username, (100, 565))
            win.blit(user_topscore, (100, 605))
            pygame.draw.rect(win, pygame.Color((100, 100, 100)), input_rect, 1)
            logout_text_surface = font.render('Logout', True, (255, 255, 255))
            # render at position stated in arguments
            win.blit(logout_text_surface, (input_rect.x, input_rect.y))

        else:
            font = pygame.font.Font('fonts/Charge Vector Black.otf', 32)
            login_text = font.render('Enter Name:', True, (240, 230, 100))
            win.blit(login_text, (100, 525))

            # create input box
            input_box_colour_active = pygame.Color('lightskyblue3')
            input_box_colour_passive = pygame.Color('chartreuse4')
            input_box_colour = input_box_colour_passive

            if input_box_active:
                input_box_colour = input_box_colour_active
                if not user_first_input:
                    user_text = ''
                user_first_input = True
            else:
                input_box_colour = input_box_colour_passive
                if user_text == '':
                    user_first_input = False
                    user_text = 'Enter Name'

            # input area
            font = pygame.font.SysFont('Corbel', 35)
            pygame.draw.rect(win, input_box_colour, input_rect)
            text_surface = font.render(user_text, True, (255, 255, 255))
            # render at position stated in arguments
            win.blit(text_surface, (input_rect.x, input_rect.y))
            # set width of textfield so that text cannot get
            # outside of user's text input
            input_rect.w = max(100, text_surface.get_width() + 10)

        # login button:
        login_button_font = pygame.font.Font('fonts/Charge Vector Black.otf', 32)
        pygame.draw.rect(win, pygame.Color((100, 100, 100)), login_button, 1)
        login_text_surface = login_button_font.render(login_button_text, True, (240, 230, 100))
        win.blit(login_text_surface, (login_button.x, login_button.y))

        # highscore button
        highscore_button_font = pygame.font.Font('fonts/Charge Vector Black.otf', 28)
        highscore_text_surface = highscore_button_font.render('High Scores', True, (240, 230, 100))
        highscore_button.w = highscore_text_surface.get_width()
        win.blit(highscore_text_surface, (highscore_button.x, highscore_button.y))

        pygame.display.update()

    pygame.quit()


pygame.display.update()
# if __name__ == "__main__":
main()
