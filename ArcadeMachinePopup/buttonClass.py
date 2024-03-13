import pygame

class Boton:
    def __init__(self, x, y, w, h, text, font, color_bg, text_color, text_size, action):
        self.font = pygame.font.Font(font, text_size)
        self.text = self.font.render(text, True, text_color)
        self.rect = self.text.get_rect()
        self.rect.topleft = (x-self.rect.width//2,y-self.rect.height//2)
        self.elev_rect = pygame.Rect((self.rect.topleft[0]+6, self.rect.topleft[1]+6), (self.rect.width, self.rect.height))
        self.elev_rect.topleft = (x+6-self.rect.width//2,y+6-self.rect.height//2)

        self.color_bg = color_bg
        self.text_color = text_color
        self.text_size = text_size
        self.action = action

        self.selector = self.font.render(">", False, text_color)
        self.sel_pos = (self.rect.topleft[0] - 20, self.rect.topleft[1])

        self.pressed = False


    def update(self, screen):
        
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.selector, self.sel_pos)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed is True:
                    self.pressed = False
        else:
            self.pressed = False

    def draw(self, screen):
        
        if not self.pressed:
            screen.blit(self.text, self.rect.topleft)
        else:
            screen.blit(self.text, self.elev_rect.topleft)
        
    
    def click(self):
        print(self.action)