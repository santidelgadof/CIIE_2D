import pygame

def BlitTransparente(superficie, color, size, coord):
    superficie_transparente = pygame.Surface(size, pygame.SRCALPHA)
    superficie_transparente.fill(color)
    superficie.blit(superficie_transparente, coord)

class Bloque(pygame.sprite.Sprite):
    def __init__(self, x, y, tecla, palabra, imagen, ancho, alto, colorTxt, colorSup):
        super().__init__()
        self.image = imagen 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.ancho_bloque = ancho
        self.alto_bloque = alto

        self.tecla = tecla
        self.palabra = palabra
        self.correcto = False

        self.color_texto = colorTxt
        self.color_superficie = colorSup

    def dibujar_letra(self, superficie):
        fuente = pygame.font.SysFont(None, 30)
        texto = fuente.render(self.tecla, True, self.color_texto)
        posicion = (self.rect.x + self.ancho_bloque // 2 - texto.get_width() // 2, self.rect.y + self.alto_bloque//2 - texto.get_height()//2)

        texto_rect = texto.get_rect()
        texto_rect.center = (self.rect.centerx, self.rect.centery - self.alto_bloque // 4)  
        cuadrado_rect = pygame.Rect(texto_rect.left - 10, texto_rect.bottom, texto_rect.width + 20, texto_rect.height+20)
        pygame.draw.rect(superficie, self.color_superficie, cuadrado_rect)
       
        superficie.blit(texto, posicion)

