import pygame


class Agujero(pygame.sprite.Sprite):
    def __init__(self, x, y, hole_image):
        super().__init__()
        self.image = hole_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pass
