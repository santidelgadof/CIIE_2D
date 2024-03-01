import pygame
from enum import Enum

# This class represent a trash container
class Container:
    def __init__(self, trash_type, image, position) -> None:
        self.trash_type = trash_type
        
        scaled_width = image.get_width() // 3
        scaled_height = image.get_height() // 3
        self.image = pygame.transform.scale(image, (scaled_width, scaled_height))
        self.position = position
    
    def draw(self, surface):
        surface.blit(self.image, self.position)
    def get_x_position(self):
        return self.position[0] + 20
    # Returns the y position
    def get_y_position(self):
        return self.position[1] - 5

class TrashType(Enum):
    ORGANIC = 1
    PLASTIC = 2
    PAPER = 3
    GLASS = 4