import pygame
import random
import config
import database_functions as dbf
from models.falling_objects import Bomb, Coin
from models.player import Player
from models.display import Display
from config import SCREEN_HEIGHT, SCREEN_WIDTH
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards


from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    USEREVENT
)


def main(player_id):
    # Initialise the game
    pygame.init()

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption('Catcher')

    # Add music
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/background.wav")
    pygame.mixer.music.play(-1, 0.0)

    # Instantiate the player
    player = Player()

    # This will be a list that will contain all the sprites we intend to use in our game.
    all_sprites_list = pygame.sprite.Group()

    # Object is used for collision detection
    falling_objects = pygame.sprite.Group()

    # Add new object
    ADDOBJECT = USEREVENT + 1
    pygame.time.set_timer(ADDOBJECT, 700)

    # Adding the player to the list of sprites
    all_sprites_list.add(player)

    run = True
    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()
    pygame.time.set_timer(USEREVENT, 1000)

    # Load background
    background = pygame.image.load('images/background.jpg')
    picture = pygame.transform.scale(background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    # Player X coordinate change
    playerX_change = 0

    score = 0
    lives = 3
    counter = 30

    display = Display(screen)

    while run:
        screen.blit(picture, (0, 0))
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user click the window closed (x) button? If so stop the loop
            if event.type == QUIT:
                run = False

            if event.type == USEREVENT:
                counter -= 1

            # Add objects
            if event.type == ADDOBJECT:
                ran = random.random()
                if ran < 0.8:
                    new_object = Coin()
                else:
                    new_object = Bomb()
                falling_objects.add(new_object)
                all_sprites_list.add(new_object)

            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
                if event.key == K_ESCAPE:
                    run = False
                elif event.key == pygame.K_LEFT:
                    player.set_position_change(-15)
                elif event.key == pygame.K_RIGHT:
                    player.set_position_change(15)

            # Did the user release a key?
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.set_position_change(0)

        # --- Game logic should go here
        all_sprites_list.update()

        # Draw all sprites
        for entity in all_sprites_list:
            screen.blit(entity.image, entity.rect)

        # Check collisions
        sprite_collided = pygame.sprite.spritecollideany(player, falling_objects)

        if sprite_collided:
            sprite_collided.collision(screen, player)
            if isinstance(sprite_collided, Coin):
                score += 1
            elif isinstance(sprite_collided, Bomb):
                lives -= 1

        display.show_score(score)
        display.show_lives(lives)
        display.show_counter(counter)

        if lives <= 0 or counter == 0:
            run = False
            display.show_game_over()
            pygame.display.flip()

        # Update the display screen
        pygame.display.flip()
        clock.tick(30)


    dbf.insert_score(player_id, score)
    pygame.time.wait(3000)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN:
                done = True

    return


if __name__ == '__main__':
    pass


