import pygame
import config


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # Load boy image
        self.boy_right_image = pygame.image.load('images/boy.png')
        self.boy_left_image = pygame.transform.flip(self.boy_right_image, True, False)

        self.image = self.boy_right_image
        self.img_height = self.image.get_rect()[3]
        self.img_width = self.image.get_rect()[2]

        # Center player
        self.rect = self.image.get_rect()

        self.rect.x = (config.SCREEN_WIDTH - self.img_width) / 2
        self.rect.y = config.SCREEN_HEIGHT - self.img_height - 15

        # Stores the change in players position
        self.position_change = 0

    def update_image(self, pixels):
        if pixels >= 0:
            self.image = self.boy_right_image
        else:
            self.image = self.boy_left_image

    # Function for moving the player sprite on key presses
    def move(self, pixels):
        self.rect.x += pixels
        self.update_image(pixels)

        if self.rect.x < 0:
            self.rect.x = 0

        if self.rect.x > config.SCREEN_WIDTH - self.img_width:
            self.rect.x = config.SCREEN_WIDTH - self.img_width

    def set_position_change(self, change):
        self.position_change = change

    def update(self):
        if self.position_change != 0:
            self.move(self.position_change)
