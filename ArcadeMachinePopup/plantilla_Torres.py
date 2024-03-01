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
AMARILLO_Letras = (249, 247, 98 )
AMARILLO = (222, 196, 65)
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
     
            

def btnPlay():
    print("PLAY")

def btnMenu():
    print("MENU")


textos = [Text("Torre", 60, NEGRO, ANCHO//2, ALTO//3-140, True, fuenteGP), 
          Text("Basura", 60, NEGRO, ANCHO//2, ALTO//3-90, True, fuenteGP),
          Text("Insert a coin", 20, NEGRO, ANCHO//2+100, ALTO//3+30, True, fuente8Bit)]

rotaciones = [0, 0, 30]

botones = [
 Boton(ANCHO//2-200 + 400//2, ALTO//3-180 + 300- 140, 100, 40, "PLAY", fuenteGP, TRANSPARENTE, NEGRO, 40, "play"),
 Boton(ANCHO//2-200+ 400//2, ALTO//3-200+ 300- 70, 100, 40, "MENU", fuenteGP, TRANSPARENTE, NEGRO, 40, "menu")
]

ventana = PopUp(ANCHO//2-200, ALTO//3-200, 400, 300, 60, AMARILLO, 8, NEGRO, botones, textos, rotaciones)

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