import pygame
from CucarachaGame.ClassGameVariables import GameVariables
from ResourceManager import ResourceManager

resource_manager = ResourceManager()
gameVars = GameVariables()

class Cucaracha(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(resource_manager.cucaracha.get(), (80, 80))
        self.image = pygame.transform.scale(self.image, (70, 70))  
        self.rect = self.image.get_rect()
        self.active = False
        self.spawn_time = 0
    
    def update(self, in_slow_motion_mode, in_speed_mode):
        if self.active:
            time_threshold = 1300 if in_slow_motion_mode else 500 if in_speed_mode else 800
            if pygame.time.get_ticks() - self.spawn_time >= time_threshold:
                self.active = False
                self.kill()  # Deletes Sprite
            
