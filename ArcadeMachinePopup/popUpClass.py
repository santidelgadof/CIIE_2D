import pygame


def rectanguloRedondo(pantalla, x, y, ancho, alto, radio, color):
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto), 0, radio)



class PopUp:
    def __init__(self, x, y, ancho, alto, radio, colorInterno, tam_borde, colorBorde, botones = [], textos = [], rotaciones = []):
        if len(textos) != len(rotaciones):
            raise ValueError("textos y rotaciones deben ser del mismo tamaño")
        
        self.x = x
        self.y = y

        self.ancho = ancho
        self.alto = alto
        self.radio = radio

        self.colorIn = colorInterno
        self.colorOut = colorBorde

        
        self.bordeX = x-tam_borde
        self.bordeY = y-tam_borde
        self.bordeAncho = ancho+tam_borde*2
        self.bordeAlto = alto+tam_borde*2

        self.botones = botones
        self.textos = textos
        self.rotaciones = rotaciones

    def draw(self, pantalla):
        rectanguloRedondo(pantalla, self.bordeX, self.bordeY, self.bordeAncho, self.bordeAlto, self.radio, self.colorOut)
        rectanguloRedondo(pantalla, self.x, self.y, self.ancho, self.alto, self.radio, self.colorIn)
        i = 0
        while i<len(self.textos):
            self.textos[i].dibujar(pantalla, self.rotaciones[i])
            i+=1

        for boton in self.botones:
            boton.dibujar(pantalla)
            boton.update(pantalla)
    
    def get_rect(self):
        return pygame.Rect(self.bordeX, self.bordeY, self.bordeAncho, self.bordeAlto)
