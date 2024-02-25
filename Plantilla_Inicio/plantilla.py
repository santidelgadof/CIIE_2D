import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (12, 18, 58)
AMARILLO = (249, 247, 98 )
TRANSPARENTE = (0, 0, 0, 50)
#AZUL_OSCURO = (71, 21, 136)

# Definir dimensiones de la pantalla
ANCHO = 800
ALTO = 800

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Plantilla')
fondo = pygame.image.load("repositorio\CIIE//Plantilla_Inicio//images//fondoArcades.jpeg").convert()
fondo = pygame.transform.scale(fondo, (800,800))
fuenteGP = "repositorio\CIIE//Plantilla_Inicio//fuentes//game_power.ttf"
fuente8Bit = "repositorio\CIIE//Plantilla_Inicio//fuentes//8Bit.ttf"

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

        self.hover = False
        self.pressed = False
        self.clicked = False

    def update(self):
        self.clicked = False
        
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hover = True
            pantalla.blit(self.selector, self.sel_pos)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed is True:
                    self.pressed = False
                    self.clicked = True
        else:
            self.pressed = False
            self.hover = False

    def dibujar(self, pantalla):
        
        if not self.pressed:
            pantalla.blit(self.texto, self.rect.topleft)
        else:
            pantalla.blit(self.texto, self.elev_rect.topleft)
        
    
    def click(self):
        print(self.accion)

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
           

def rectanguloRedondo(x, y, ancho, alto, radio, color):
    pygame.draw.rect(pantalla, color, (x + radio, y, ancho - 2 * radio, alto))
    pygame.draw.rect(pantalla, color, (x, y + radio, ancho, alto - 2 * radio))
    pygame.draw.ellipse(pantalla, color, (x, y, 2 * radio, 2 * radio))
    pygame.draw.ellipse(pantalla, color, (x + ancho - 2 * radio, y, 2 * radio, 2 * radio))
    pygame.draw.ellipse(pantalla, color, (x, y + alto - 2 * radio, 2 * radio, 2 * radio))
    pygame.draw.ellipse(pantalla, color, (x + ancho - 2 * radio, y + alto - 2 * radio, 2 * radio, 2 * radio))

def texto(text, tam, color, x, y, centrado = True, rotacion = 0):
    fuente = pygame.font.Font(fuenteGP, tam)
    txt_render = fuente.render(text, True, color)
    txt_render = pygame.transform.rotate(txt_render, rotacion)

    rectangulo_texto = txt_render.get_rect() 
    if centrado:
        rectangulo_texto.topleft = (x-rectangulo_texto.width//2, y-rectangulo_texto.height//2)
    else:
        rectangulo_texto.topleft = (x, y)

    pantalla.blit(txt_render, rectangulo_texto)

def pantallaJuegos(x, y, ancho, alto, radio, colorInterno, Tam_borde,  colorBorde, botones):
    rectanguloRedondo(x-Tam_borde, y-Tam_borde, ancho+Tam_borde*2, alto+Tam_borde*2, radio, colorBorde)
    rectanguloRedondo(x, y, ancho, alto, radio, colorInterno)

    #se podría llegar a hacer una letra de cada color para el tetris

    tetrisTxt.dibujar(pantalla)
    coinTxt.dibujar(pantalla, 30)
    
    #texto("Tetris", 60, AMARILLO, x + ancho//2, y + alto//5)
    #texto("Insert a coin", 20, AMARILLO, x + ancho-100, y + alto-50, 90)

    for boton in botones:
        boton.dibujar(pantalla)
        boton.update()

def BlitTransparente(superficie, color, size, coord):
    superficie_transparente = pygame.Surface(size, pygame.SRCALPHA)
    superficie_transparente.fill(color)
    superficie.blit(superficie_transparente, coord)

            

def btnPlay():
    print("PLAY")

def btnMenu():
    print("MENU")


tetrisTxt = Text("Tetris", 60, AMARILLO, ANCHO//2-200 + 400//2, ALTO//3-200 + 300//5, True, fuenteGP)
coinTxt = Text("Insert a coin", 20, AMARILLO, ANCHO//2-200 + 400-100, ALTO//3-200 + 300-50, True, fuente8Bit)


botones = [
 Boton(ANCHO//2-200 + 400//2, ALTO//3-200 + 300- 140, 100, 40, "PLAY", fuenteGP, TRANSPARENTE, AMARILLO, 40, "play"),
 Boton(ANCHO//2-200+ 400//2, ALTO//3-200+ 300- 70, 100, 40, "MENU", fuenteGP, TRANSPARENTE, AMARILLO, 40, "menu")
]

# Bucle principal del juego
while True:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for boton in botones:
                    if boton.rect.collidepoint(event.pos):
                        boton.click()
                

    # Limpiar la pantalla
    pantalla.blit(fondo, (0,0))

    # Dibujar el rectángulo con bordes redondeados
    pantallaJuegos(ANCHO//2-200, ALTO//3-200, 400, 300, 60, AZUL, 8, NEGRO, botones)

    

    # Actualizar la pantalla
    pygame.display.flip()
