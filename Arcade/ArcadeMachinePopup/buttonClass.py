import pygame

class Boton:
    def __init__(self, x, y, ancho, alto, texto, fuente, color_fondo, color_texto, tam_texto, accion):
        self.fuente = pygame.font.Font(fuente, tam_texto)
        self.texto = self.fuente.render(texto, True, color_texto)
        self.rect = self.texto.get_rect()
        self.rect.topleft = (x-self.rect.width//2,y-self.rect.height//2)
        self.elev_rect = pygame.Rect((self.rect.topleft[0]+6, self.rect.topleft[1]+6), (self.rect.width, self.rect.height))
        self.elev_rect.topleft = (x+6-self.rect.width//2,y+6-self.rect.height//2)

        self.color_fondo = color_fondo
        self.color_texto = color_texto
        self.tam_texto = tam_texto
        self.accion = accion

        self.selector = self.fuente.render(">", False, color_texto)
        self.sel_pos = (self.rect.topleft[0] - 20, self.rect.topleft[1])

        self.pressed = False


    def update(self, pantalla):
        self.clicked = False
        
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pantalla.blit(self.selector, self.sel_pos)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed is True:
                    self.pressed = False
        else:
            self.pressed = False

    def dibujar(self, pantalla):
        
        if not self.pressed:
            pantalla.blit(self.texto, self.rect.topleft)
        else:
            pantalla.blit(self.texto, self.elev_rect.topleft)
        
    
    def click(self):
        print(self.accion)