import pygame

def BlitTransparente(screen, color, size, coord):
    trans_screen = pygame.Surface(size, pygame.SRCALPHA)
    trans_screen.fill(color)
    screen.blit(trans_screen, coord)

class Bloque(pygame.sprite.Sprite):
    def __init__(self, x, y, key, word, img, w, h, colorTxt, colorScreen):
        super().__init__()
        self.image = img 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.w_block = w
        self.h_block = h

        self.key = key
        self.word = word
        self.correct = False

        self.color_txt = colorTxt
        self.color_screen = colorScreen

    def draw_letter(self, screen):
        font = pygame.font.SysFont(None, 30)
        text = font.render(self.key, True, self.color_txt)
        pos = (self.rect.x + self.w_block // 2 - text.get_width() // 2, self.rect.y + self.h_block//2 - text.get_height()//2)

        text_rect = text.get_rect()
        text_rect.center = (self.rect.centerx, self.rect.centery - self.h_block // 4)  
        sqr_rect = pygame.Rect(text_rect.left - 10, text_rect.bottom, text_rect.width + 20, text_rect.height+20)
        pygame.draw.rect(screen, self.color_screen, sqr_rect)
       
        screen.blit(text, pos)

