import pygame

class Text:
    def __init__(self, text, size, x, y, color_letter = (255, 255, 255), centered = False, font = None, bg = False, border = False, color_bg = (255, 255, 255), color_border = (0,0,0), size_border = 4):
        self.font = pygame.font.Font(font, size)
        self.render = self.font.render(text, True, color_letter)
        self.centered = centered
    
        self.x = x
        self.y = y

        self.bg = bg
        self.colorBg = color_bg

        self.border = border
        self.colorBorder = color_border
        self.size_border = size_border

    def draw(self, pantalla):

        rect_text = self.render.get_rect() 
        if self.centered:
            rect_text.topleft = (self.x-rect_text.width//2, self.y-rect_text.height//2)
        else:
            rect_text.topleft = (self.x, self.y)

        if self.bg:
            rect = pygame.Rect(rect_text.topleft[0], rect_text.topleft[1], rect_text.width, rect_text.height)

            if self.border:
                pygame.draw.rect(pantalla, self.color_border, (rect[0]-self.size_border, rect[1]-self.size_border, rect[2]+self.size_border*2, rect[3]+self.size_border*2))
            pygame.draw.rect(pantalla, self.colorBg, rect)
    
        pantalla.blit(self.render, rect_text)