import pygame
import sys
from textClass import Text
from buttonClass import Boton
from popUpClass import PopUp

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
     
def rectanguloRedondo(x, y, ancho, alto, radio, color):
    pygame.draw.rect(pantalla, color, (x + radio, y, ancho - 2 * radio, alto))
    pygame.draw.rect(pantalla, color, (x, y + radio, ancho, alto - 2 * radio))
    pygame.draw.ellipse(pantalla, color, (x, y, 2 * radio, 2 * radio))
    pygame.draw.ellipse(pantalla, color, (x + ancho - 2 * radio, y, 2 * radio, 2 * radio))
    pygame.draw.ellipse(pantalla, color, (x, y + alto - 2 * radio, 2 * radio, 2 * radio))
    pygame.draw.ellipse(pantalla, color, (x + ancho - 2 * radio, y + alto - 2 * radio, 2 * radio, 2 * radio))

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
        boton.update(pantalla)

def BlitTransparente(superficie, color, size, coord):
    superficie_transparente = pygame.Surface(size, pygame.SRCALPHA)
    superficie_transparente.fill(color)
    superficie.blit(superficie_transparente, coord)

            

def btnPlay():
    print("PLAY")

def btnMenu():
    print("MENU")


tetrisTxt = Text("Tetris", 60, AMARILLO, ANCHO//2-200 + 400//2, ALTO//3-200 + 300//5, True, fuenteGP)
coinTxt = Text("Insert a coin", 20, AMARILLO, ANCHO//2-200 + 400-100, ALTO//3-200 + 300-70, True, fuente8Bit)

textos = [
    Text("Tetris", 60, AMARILLO, ANCHO//2-200 + 400//2, ALTO//3-200 + 300//5, True, fuenteGP),
    Text("Insert a coin", 20, AMARILLO, ANCHO//2-200 + 400-100, ALTO//3-200 + 300-70, True, fuente8Bit)
]

rotaciones = [0, 30]

botones = [
 Boton(ANCHO//2-200 + 400//2, ALTO//3-200 + 300- 140, 100, 40, "PLAY", fuenteGP, TRANSPARENTE, AMARILLO, 40, "play"),
 Boton(ANCHO//2-200+ 400//2, ALTO//3-200+ 300- 70, 100, 40, "MENU", fuenteGP, TRANSPARENTE, AMARILLO, 40, "menu")
]

ventana = PopUp(ANCHO//2-200, ALTO//3-200, 400, 300, 60, AZUL, 8, NEGRO, botones, textos, rotaciones)

def main():
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
        #pantallaJuegos(ANCHO//2-200, ALTO//3-200, 400, 300, 60, AZUL, 8, NEGRO, botones)
        ventana.draw(pantalla)

        

        # Actualizar la pantalla
        pygame.display.flip()


if __name__ == '__main__':
    main()