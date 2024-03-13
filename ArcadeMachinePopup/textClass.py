import pygame

class Text:
    def __init__(self, text, size, color, x, y, centered = True, font = None):
        self.font = pygame.font.Font(font, size)
        self.render = self.font.render(text, True, color)
        self.centered = centered
        self.x = x
        self.y = y
    
    def draw(self, screen, rot = 0):
        txt_render = pygame.transform.rotate(self.render, rot)

        rect_text = txt_render.get_rect() 
        if self.centered:
            rect_text.topleft = (self.x-rect_text.width//2, self.y-rect_text.height//2)
        else:
            rect_text.topleft = (self.x, self.y)

        screen.blit(txt_render, rect_text)