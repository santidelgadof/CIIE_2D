import pygame
from ResourceManager import ResourceManager

resource_manager = ResourceManager()


class SlowItem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(resource_manager.slow.get(), (80, 80))
        self.rect = self.image.get_rect()
        self.active = False
        self.spawn_time = 0
    
    def update(self):
        if self.active:
            if pygame.time.get_ticks() - self.spawn_time >= 1000:
                self.active = False
                self.kill()