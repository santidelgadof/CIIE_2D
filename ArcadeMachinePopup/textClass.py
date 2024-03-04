import pygame

class Text:
    def __init__(self, text, tam, color, x, y, centrado = True, fuente = None):
        self.fuente = pygame.font.Font(fuente, tam)
        self.render = self.fuente.render(text, True, color)
        self.centrado = centrado
        self.x = x
        self.y = y
    
    def dibujar(self, pantalla, rot = 0):
        txt_render = pygame.transform.rotate(self.render, rot)

        rectangulo_texto = txt_render.get_rect() 
        if self.centrado:
            rectangulo_texto.topleft = (self.x-rectangulo_texto.width//2, self.y-rectangulo_texto.height//2)
        else:
            rectangulo_texto.topleft = (self.x, self.y)

        pantalla.blit(txt_render, rectangulo_texto)