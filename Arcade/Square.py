import pygame

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, number):
        super().__init__()
        self.image = pygame.Surface((110, 110), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.number = number
        self.active = True
