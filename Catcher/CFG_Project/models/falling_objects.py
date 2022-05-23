import pygame
import random
import config

class FallingObject(pygame.sprite.Sprite):
    def __init__(self):
        super(FallingObject, self).__init__()

        self.rect = self.image.get_rect()

        # Start each new object
        self.rect.x = random.randint(10, config.SCREEN_WIDTH)
        self.rect.y = random.randint(-100, -40)

        self.speed = random.randint(2, 4)        

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > config.SCREEN_HEIGHT:
            self.kill()
    
    def collision(self, screen, player):
        self.kill()

class Bomb(FallingObject):
    def __init__(self):
        self.image = pygame.image.load('images/bomb.png')
        super(Bomb, self).__init__()
    def collision(self, screen, player):
        pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/bomb.wav'))
        screen.blit(player.image, player.rect, special_flags=pygame.BLEND_SUB)
        self.kill()

class Coin(FallingObject):
    def __init__(self):
        self.image = pygame.image.load('images/coin.png')
        super(Coin, self).__init__()
    def collision(self, screen, player):
        pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/coin.wav'))
        screen.blit(player.image, player.rect, special_flags=pygame.BLEND_ADD)
        self.kill()