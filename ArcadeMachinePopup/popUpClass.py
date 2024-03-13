import pygame


def roundedRectangle(screen, x, y, w, h, r, color):
    pygame.draw.rect(screen, color, (x, y, w, h), 0, r)



class PopUp:
    def __init__(self, x, y, w, h, r, colorIn, border_size, border_color, buttons = [], texts = [], rotations = []):
        if len(texts) != len(rotations):
            raise ValueError("textos y rotaciones deben ser del mismo tamaño")
        
        self.x = x
        self.y = y

        self.w = w
        self.h = h
        self.r = r

        self.colorIn = colorIn
        self.colorOut = border_color

        
        self.borderX = x-border_size
        self.borderY = y-border_size
        self.borderW = w+border_size*2
        self.borderH = h+border_size*2

        self.buttons = buttons
        self.texts = texts
        self.rotations = rotations

    def draw(self, screen):
        roundedRectangle(screen, self.borderX, self.borderY, self.borderW, self.borderH, self.r, self.colorOut)
        roundedRectangle(screen, self.x, self.y, self.w, self.h, self.r, self.colorIn)
        i = 0
        while i<len(self.texts):
            self.texts[i].draw(screen, self.rotations[i])
            i+=1

        for btn in self.buttons:
            btn.draw(screen)
            btn.update(screen)
    
    def get_rect(self):
        return pygame.Rect(self.borderX, self.borderY, self.borderW, self.borderH)
