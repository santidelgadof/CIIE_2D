import pygame

class SlowItem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("CucarachaGame/Assets/slow_item.png").convert_alpha(), (80, 80))
        self.rect = self.image.get_rect()
        self.active = False
        self.spawn_time = 0

    def update(self):
        if self.active:
            if pygame.time.get_ticks() - self.spawn_time >= 1000:
                self.active = False
                self.kill()