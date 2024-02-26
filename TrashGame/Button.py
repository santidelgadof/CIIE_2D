import pygame

class Button:
    
    def __init__(self, x, y, width, height, text, text_color, color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.color = color
        self.action = action
        self.clicked = False

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse)
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 40)
        if hovered:
            text = font.render(self.text, True, self.text_color)
        else:
            text = font.render(self.text, True, (50,50,50))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_clicked(self, pos):
        
        if not self.clicked:
            if self.rect.collidepoint(pos):
                if self.action is not None:
                    res = self.action()
                    self.clicked = True
                    return res
        
        
        