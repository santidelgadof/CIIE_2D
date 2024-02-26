import pygame

class Text:
    def __init__(self, text, tam, x, y, color_letras = (255, 255, 255), centrado = False, fuente = None, fondo = False, borde = False, color_fondo = (255, 255, 255), color_borde = (0,0,0), tam_borde = 4):
        self.fuente = pygame.font.Font(fuente, tam)
        self.render = self.fuente.render(text, True, color_letras)
        self.centrado = centrado
    
        self.x = x
        self.y = y

        self.fondo = fondo
        self.colorFondo = color_fondo

        self.borde = borde
        self.colorBorde = color_borde
        self.tam_borde = tam_borde

    def dibujar(self, pantalla):

        rectangulo_texto = self.render.get_rect() 
        if self.centrado:
            rectangulo_texto.topleft = (self.x-rectangulo_texto.width//2, self.y-rectangulo_texto.height//2)
        else:
            rectangulo_texto.topleft = (self.x, self.y)

        if self.fondo:
            rectangulo = pygame.Rect(rectangulo_texto.topleft[0], rectangulo_texto.topleft[1], rectangulo_texto.width, rectangulo_texto.height)

            if self.borde:
                pygame.draw.rect(pantalla, self.color_borde, (rectangulo[0]-self.tam_borde, rectangulo[1]-self.tam_borde, rectangulo[2]+self.tam_borde*2, rectangulo[3]+self.tam_borde*2))
            pygame.draw.rect(pantalla, self.colorFondo, rectangulo)
    
        pantalla.blit(self.render, rectangulo_texto)