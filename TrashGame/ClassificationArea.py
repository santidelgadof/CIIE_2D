import pygame
class ClassificationArea:

    def __init__(self, size, y_position, color):
        self.size = size
        self.y_position = y_position
        self.color = color
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(350, self.y_position, self.size, self.size), 0, 15)
        
    # This function classifies the trash items that are inside the ClassificationArea 
    def classify(self, trash_items, container_x, container_y, trash_type, current_lives):
        for trash_item in trash_items:
            if trash_item.get_x_position() == 360:
                if self.y_position - self.size/2 <= trash_item.get_y_position() <= self.y_position + self.size/2:
                    # Classify the trash item
                    if  not trash_type.__contains__(trash_item.trash_type):
                        current_lives = current_lives - 1
                    trash_item.classify(container_x, container_y)
        return current_lives
