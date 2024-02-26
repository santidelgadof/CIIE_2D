import pygame
from TrashGame.Container import TrashType
import os

class TrashItem:
    classified = False
    container_x = None
    container_y = None
    dead = False
    for_a_good_reason = False
    def __init__(self, resource, size, initial_position, speed, trash_type):
        self.image = resource.get()
        self.size = size
        self.image = pygame.transform.scale(self.image, size)
        self.position = list(initial_position)
        self.speed = speed
        self.trash_type = trash_type
    
    # This function moves the TrashItem to next position
    def move(self):
        if not self.dead:
            if not self.classified:
                    if self.position[1] < 700:
                        self.position[1] += self.speed
                    else:
                        self.image.set_alpha(max(0, self.image.get_alpha() - 10))
                        if self.image.get_alpha() == 0:
                            # Notify the main loop that this Object will never be used again so it can be removed
                            self.dead = True
                            self.for_a_good_reason = False 
            else:
                container_x, container_y = self.container_x, self.container_y
                if self.position[0] < container_x:
                    self.position[0] += min(self.speed, container_x - self.position[0])
                elif self.position[0] > container_x:
                    self.position[0] -= min(self.speed, self.position[0] - container_x)
                else:
                    if self.position[1] < container_y:
                        self.position[1] += min(self.speed, container_y - self.position[1])
                    elif self.position[1] > container_y:
                        self.position[1] -= min(self.speed, self.position[1] - container_y)
                    else:
                        if self.size[0] > 0 and self.size[1] > 0:
                            # Transition to disappear with decreasing opacity
                            self.image.set_alpha(max(0, self.image.get_alpha() - 10))
                            if self.image.get_alpha() == 0:
                                # Notify the main loop that this Object will never be used again and can be removed
                                self.dead = True
                                self.for_a_good_reason = True 

    # Draws the TrashItem on a surface
    def draw(self, surface):
        surface.blit(self.image, self.position)
    # Returns the x position
    def get_x_position(self):
        return self.position[0]
    # Returns the y position
    def get_y_position(self):
        return self.position[1]
    # Updates the location of the container to which the TrashItem should be displayed
    def classify(self, con_x, con_y):
        self.container_x = con_x
        self.container_y = con_y
        self.classified = True
       
        
    
