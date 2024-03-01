import pygame

class HealthBar:
    def __init__(self, max_lives, radius=10, padding=5):
        self.max_lives = max_lives
        self.radius = radius
        self.padding = padding
        self.lives = max_lives
    
    def draw(self, window, current_lives):
        # Calculate starting position for the health bar
        start_x = window.get_width() - (self.max_lives * (self.radius * 2 + self.padding))
        start_y = self.padding
        
        # Draw red circles for each life
        for i in range(self.max_lives):
            color = (255, 0, 0) if i < current_lives else (100, 100, 100)  # Red if life is active, gray if lost
            pygame.draw.circle(window, color, (start_x + i * (self.radius * 2 + self.padding) + self.radius, start_y + self.radius), self.radius)