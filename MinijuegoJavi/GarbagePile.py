import pygame
import random
import sys
import os

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Definir dimensiones de la pantalla
ANCHO = 800
ALTO = 800

# Definir tamaño y cantidad de bloques
ANCHO_BLOQUE = 120
ALTO_BLOQUE = 120
CANTIDAD_BLOQUES = 10

# Definir tiempo límite en segundos
TIEMPO_LIMITE = 10

def cargar_imagenes():
    imagenes = []
    for nombre_archivo in os.listdir("repositorio\CIIE\MinijuegoJavi\images//bloques"):
        ruta = os.path.join("repositorio\CIIE\MinijuegoJavi\images//bloques", nombre_archivo)
        if os.path.isfile(ruta):
            imagen = pygame.image.load(ruta).convert_alpha()
            imagen = pygame.transform.scale(imagen, (ANCHO_BLOQUE, ALTO_BLOQUE))
            imagenes.append(imagen)
    return imagenes

# Crear clase para representar un bloque
class Bloque(pygame.sprite.Sprite):
    def __init__(self, x, y, tecla, imagenes):
        super().__init__()
        #self.image = pygame.Surface([ANCHO_BLOQUE, ALTO_BLOQUE])
        #self.image.fill(NEGRO)
        self.image = random.choice(imagenes)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO/2 - ANCHO_BLOQUE
        self.rect.y = ALTO/2 - ALTO_BLOQUE
        self.tecla = tecla

    def update(self):
        pass

    def dibujar_letra(self, superficie):
        fuente = pygame.font.SysFont(None, 50)
        texto = fuente.render(self.tecla, True, NEGRO)
        posicion = (self.rect.x + ANCHO_BLOQUE // 2 - texto.get_width() // 2, self.rect.y + 10)
        superficie.blit(texto, posicion)

# Función para mostrar texto en pantalla
def mostrar_texto(texto, fuente, superficie, x, y):
    texto_objeto = fuente.render(texto, True, NEGRO)
    rectangulo_texto = texto_objeto.get_rect()
    rectangulo_texto.topleft = (x, y)
    superficie.blit(texto_objeto, rectangulo_texto)

# Función principal del juego
def main():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Juego de Bloques')

    imagenes_bloques = cargar_imagenes()

    # Crear lista de bloques
    bloques = pygame.sprite.Group()
    for i in range(CANTIDAD_BLOQUES):
        bloque = Bloque(ANCHO_BLOQUE,
                        ALTO_BLOQUE,
                        chr(random.randint(97, 122)),
                        imagenes_bloques)
        bloques.add(bloque)

    # Crear reloj
    reloj = pygame.time.Clock()

    # Tiempo inicial
    tiempo_inicio = pygame.time.get_ticks()

    # Ciclo principal del juego
    while True:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Verificar si se presionó la tecla correspondiente al bloque superior
                if bloques:
                    # Obtener el último bloque del grupo
                    ultimo_bloque = bloques.sprites()[-1]
                    
                    # Verificar si la tecla presionada coincide con la tecla del último bloque
                    if event.key == ord(ultimo_bloque.tecla):
                        # Eliminar el último bloque
                        ultimo_bloque.kill()

        # Limpiar pantalla
        pantalla.fill(BLANCO)

        # Actualizar y dibujar bloques
        for bloque in bloques:
            bloque.update()
            pantalla.blit(bloque.image, bloque.rect)
            bloque.dibujar_letra(pantalla)

        #bloques.draw(pantalla)

        # Calcular tiempo transcurrido
        tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio
        tiempo_restante = max(0, TIEMPO_LIMITE - tiempo_transcurrido // 1000)

        # Mostrar tiempo restante en pantalla
        mostrar_texto("Tiempo restante: " + str(tiempo_restante), pygame.font.Font(None, 36), pantalla, 10, 10)

        #Verificar si quedan bloques
        if len(bloques) == 0:
            mostrar_texto("ENHORABUENA", pygame.font.Font(None, 36), pantalla, ANCHO/2 - 80, ALTO/2)
            mostrar_texto("Has conseguido limpiar la pila de basura en: " + str(TIEMPO_LIMITE-tiempo_restante) + "s", pygame.font.Font(None, 36), pantalla,  ANCHO/2 - 300, ALTO/2 + 50)
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        # Verificar si se acabó el tiempo
        if tiempo_transcurrido >= TIEMPO_LIMITE * 1000:
            mostrar_texto("¡Se acabó el tiempo!", pygame.font.Font(None, 72), pantalla, ANCHO//2 - 200, ALTO//2)
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

        # Actualizar pantalla
        pygame.display.flip()

        # Controlar la velocidad de actualización
        reloj.tick()

if __name__ == '__main__':
    main()
