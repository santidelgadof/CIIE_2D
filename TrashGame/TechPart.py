import pygame
# This class represents a tech part of the machine
class TechPart:
    dead = False
    def __init__(self, resource, initial_position, speed):
        image = resource.get()
        scaled_width = image.get_width() //4 #// 12
        scaled_height = image.get_height() //4 #// 12
        self.image = pygame.transform.scale(image, (scaled_width, scaled_height))
        self.position = list(initial_position)
        self.speed = speed
    
    def draw(self, surface):
        surface.blit(self.image, self.position)

    def move(self):
        if self.position[1] < 700:
            self.position[1] += self.speed
        else:
            self.image.set_alpha(max(0, self.image.get_alpha() - 10))
            if self.image.get_alpha() == 0:
                self.dead = True
                            
        