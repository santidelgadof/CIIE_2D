import pygame
from ResourceManager import ResourceManager

resource_manager = ResourceManager()

class Cucaracha(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(resource_manager.cucaracha.get(), (80, 80))
        self.image = pygame.transform.scale(self.image, (70, 70))  # Escalar la imagen 
        self.rect = self.image.get_rect()
        self.active = False
        self.spawn_time = 0
    
    def update(self, in_slow_motion_mode, in_speed_mode):
        if self.active:
            time_threshold = 1300 if in_slow_motion_mode else 500 if in_speed_mode else 800
            if pygame.time.get_ticks() - self.spawn_time >= time_threshold:
                self.active = False
                self.kill()  # Elimina el sprite del grupo
