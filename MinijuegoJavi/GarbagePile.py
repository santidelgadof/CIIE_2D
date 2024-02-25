import pygame
import random
import sys
import os

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL_SUELO = (47, 55, 65)
AZUL_ENTREBASURA = (69, 85, 106 )
TRANSPARENTE_VERDE = (0, 255, 0, 100)  # Alfa 0 para transparencia
TRANSPARENTE_ROJJO = (255,0,0,100)

# Definir dimensiones de la pantalla
ANCHO = 800
ALTO = 800

# Definir tamaño y cantidad de bloques
ANCHO_BLOQUE = 120
ALTO_BLOQUE = 120
CANTIDAD_BLOQUES = 3
SIZES = 5

TAM_ENTREIMG = ANCHO_BLOQUE*3

# Definir tiempo límite en segundos
TIEMPO_LIMITE = 60

Palabras = [["caja", "lixo", "lata", "ropa", "tapa", "rata", "alga", "azul", "olor"], 
            ["resto", "sucio", "bolsa", "verde", "latas", "raton", "hedor", "tirar", "mugre"], 
            ["basura", "carton", "vidrio", "reusar", "limpio", "restos", "bodrio", "birria", "sarama", "sobras"], 
            ["bazofia", "podrido", "residuo", "desecho", "vertido"], 
            ["amarillo", "papelera", "reciclar", "escombro", "desechos", "suciedad"]]


PosPalabras = [
               [(ANCHO//2-ANCHO_BLOQUE, ALTO//2-ALTO_BLOQUE), (ANCHO//2, ALTO//2-ALTO_BLOQUE), 
                (ANCHO//2-ANCHO_BLOQUE, ALTO//2), (ANCHO//2, ALTO//2)], 

               [(ANCHO//2-ANCHO_BLOQUE//2, ALTO//2-ALTO_BLOQUE//2), (ANCHO//2-ANCHO_BLOQUE//2, ALTO//2-int(ALTO_BLOQUE*1.5)), 
                (ANCHO//2+ANCHO_BLOQUE//2, ALTO//2-ALTO_BLOQUE//2), (ANCHO//2-ANCHO_BLOQUE//2, ALTO//2+ALTO_BLOQUE//2),
                (ANCHO//2-int(ANCHO_BLOQUE*1.5), ALTO//2-ALTO_BLOQUE//2)],

               [(ANCHO//2-int(ANCHO_BLOQUE*1.5), ALTO//2-ALTO_BLOQUE), (ANCHO//2-ANCHO_BLOQUE//2, ALTO//2-ALTO_BLOQUE),
                (ANCHO//2+ANCHO_BLOQUE//2, ALTO//2-ALTO_BLOQUE), (ANCHO//2-int(ANCHO_BLOQUE*1.5), ALTO//2), 
                (ANCHO//2-ANCHO_BLOQUE//2, ALTO//2), (ANCHO//2+ANCHO_BLOQUE//2, ALTO//2)], 
                
               [(ANCHO//2-int(ANCHO_BLOQUE*1.5), ALTO//2-int(ALTO_BLOQUE*1.5)), (ANCHO//2-ANCHO_BLOQUE//2, ALTO//2-int(ALTO_BLOQUE*1.5)), 
                (ANCHO//2+ANCHO_BLOQUE//2, ALTO//2-int(ALTO_BLOQUE*1.5)), (ANCHO//2-ANCHO_BLOQUE//2, ALTO//2-ALTO_BLOQUE//2), 
                (ANCHO//2-int(ANCHO_BLOQUE*1.5), ALTO//2+ALTO_BLOQUE//2), (ANCHO//2-ANCHO_BLOQUE//2, ALTO//2+ALTO_BLOQUE//2), 
                (ANCHO//2+ANCHO_BLOQUE//2, ALTO//2+ALTO_BLOQUE//2)], 
              
               [(ANCHO//2-int(ANCHO_BLOQUE*1.5), ALTO//2-int(ALTO_BLOQUE*1.5)), (ANCHO//2-ANCHO_BLOQUE//2, ALTO//2-int(ALTO_BLOQUE*1.5)), 
                (ANCHO//2+ANCHO_BLOQUE//2, ALTO//2-int(ALTO_BLOQUE*1.5)), (ANCHO//2+ANCHO_BLOQUE//2, ALTO//2-ALTO_BLOQUE//2), 
                (ANCHO//2+ANCHO_BLOQUE//2, ALTO//2+ALTO_BLOQUE//2), (ANCHO//2-ANCHO_BLOQUE//2, ALTO//2+ALTO_BLOQUE//2), 
                (ANCHO//2-int(ANCHO_BLOQUE*1.5), ALTO//2+ALTO_BLOQUE//2), (ANCHO//2-int(ANCHO_BLOQUE*1.5), ALTO//2-ALTO_BLOQUE//2)]
                ]

def cargar_imagenes():
    imagenes = []
    for nombre_archivo in os.listdir("repositorio\CIIE\MinijuegoJavi\images//bloques"):
        ruta = os.path.join("repositorio\CIIE\MinijuegoJavi\images//bloques", nombre_archivo)
        if os.path.isfile(ruta):
            imagen = pygame.image.load(ruta).convert_alpha()
            imagen = pygame.transform.scale(imagen, (ANCHO_BLOQUE, ALTO_BLOQUE))
            imagenes.append(imagen)
    return imagenes

def musica():
    pygame.mixer.music.load("repositorio\CIIE\MinijuegoJavi\music\music2.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

# Crear clase para representar un bloque
class Bloque(pygame.sprite.Sprite):
    def __init__(self, x, y, tecla, palabra, imagen):
        super().__init__()
        self.image = imagen 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tecla = tecla
        self.palabra = palabra
        self.correcto = False

    def update(self):
        pass

    def dibujar_letra(self, superficie):
        fuente = pygame.font.SysFont(None, 30)
        texto = fuente.render(self.tecla, True, BLANCO)
        posicion = (self.rect.x + ANCHO_BLOQUE // 2 - texto.get_width() // 2, self.rect.y + ALTO_BLOQUE//2 - texto.get_height()//2)

        texto_rect = texto.get_rect()
        texto_rect.center = (self.rect.centerx, self.rect.centery - ALTO_BLOQUE // 4)  
        cuadrado_rect = pygame.Rect(texto_rect.left - 10, texto_rect.bottom, texto_rect.width + 20, texto_rect.height+20)
        pygame.draw.rect(superficie, AZUL_SUELO, cuadrado_rect)
       
        superficie.blit(texto, posicion)

class ClicableObject(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Función para mostrar texto en pantalla
def mostrar_texto(texto, fuente, superficie, x, y, color_fondo = NEGRO, color_letras = BLANCO, color_borde = AZUL_SUELO, centrado = False, fondo = True, borde = True,  tam_borde = 4):

    texto_objeto = fuente.render(texto, True, color_letras)
    rectangulo_texto = texto_objeto.get_rect() 
    if centrado:
        rectangulo_texto.topleft = (x-rectangulo_texto.width//2, y-rectangulo_texto.height//2)
    else:
        rectangulo_texto.topleft = (x, y)

    if fondo:
        rectangulo = pygame.Rect(rectangulo_texto.topleft[0], rectangulo_texto.topleft[1], rectangulo_texto.width, rectangulo_texto.height)

        if borde:
            pygame.draw.rect(superficie, color_borde, (rectangulo[0]-tam_borde, rectangulo[1]-tam_borde, rectangulo[2]+tam_borde*2, rectangulo[3]+tam_borde*2))
        pygame.draw.rect(superficie, color_fondo, rectangulo)
    
    superficie.blit(texto_objeto, rectangulo_texto)

def crearListaBloques(img, bloques, palabra, nBloques):
    letras = random.sample(palabra, nBloques)
    i = 0
    while i < nBloques:
        aux = True
        
        bloque = Bloque(PosPalabras[nBloques-4][i][0],
                        PosPalabras[nBloques-4][i][1],
                        letras[i],
                        palabra, 
                        img)
    
        bloques.add(bloque)
        i=i+1
    return bloques


def CreacionMountain():
    #elegir orden y palabras de los niveles de la montaña
    i = 0
    aux = 9
    mountain = []
    
    while i<CANTIDAD_BLOQUES: 
        
        if aux == 9:
            size = random.randint(0,SIZES-1)
        else: 
            size = random.randint(aux, SIZES-1)
        
        repetida = True
        while repetida:
            palabra = random.choice(Palabras[size])
            if palabra not in mountain:
                repetida = False
        
        mountain.append(palabra)
        aux = size
        i = i+1
    return mountain
    
def BlitTransparente(superficie, color, size, coord):
    superficie_transparente = pygame.Surface(size, pygame.SRCALPHA)
    superficie_transparente.fill(color)
    superficie.blit(superficie_transparente, coord)


# Función principal del juego
def main():
    musica()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Juego de Bloques')

    imagenes_bloques = cargar_imagenes()
    fondo = pygame.image.load("repositorio\CIIE\MinijuegoJavi\images//fondoNuevo.jpg").convert()
    fondo = pygame.transform.scale(fondo, (800,800))
    bombillaON = pygame.image.load("repositorio\CIIE\MinijuegoJavi\images//bombillaOn.png")
    bombillaON = pygame.transform.scale(bombillaON, (50,50))
    bombillaOff = pygame.image.load("repositorio\CIIE\MinijuegoJavi\images//bombillaOff.png")
    bombillaOff = pygame.transform.scale(bombillaOff, (50,50))
    entreBasura = pygame.image.load("repositorio\CIIE\MinijuegoJavi\images//entreBasura.jpg")
    entreBasura = pygame.transform.scale(entreBasura, (TAM_ENTREIMG, TAM_ENTREIMG))

    pantalla.blit(fondo, (0, 0))

    MountainArray = CreacionMountain() #crea la lista de palabras

     # Crear lista de lista de bloques con las letras para cada palabra
    bloques = []
    i = 0
    for palabra in MountainArray: 
        
        bloques.append(pygame.sprite.Group())
        img = random.choice(imagenes_bloques)
        bloques[i] = crearListaBloques(img, bloques[i], palabra, len(palabra))
        i = i+1

    bombilla = ClicableObject(ANCHO-50, ALTO-100, bombillaON)
    # Crear reloj
    reloj = pygame.time.Clock()

    # Tiempo inicial
    tiempoLimite = TIEMPO_LIMITE
    tiempo_inicio = pygame.time.get_ticks()
    aciertos = 0
    guess = ""
    n = 0
    m=0
    next_letter = False
    fin = False
    
    bombillaUsada = False
    hint_bool = False
    bloquesInvertidos = bloques[::-1]
    #entreBasura =  pygame.Rect(ANCHO//2 - TAM_ENTREIMG//2, ALTO//2-TAM_ENTREIMG//2, TAM_ENTREIMG,TAM_ENTREIMG)
    
    # Ciclo principal del juego
    while True:
        isKey = True
        palabra = bloques[n].sprites()[0].palabra
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                try:
                    chr(event.key)
                except:
                    #guess = ""
                    isKey = False
                    

                if bloques and isKey:

                    if not next_letter: 
                        guess = "" 
                        tiempoLimite -= 5

                    palabra = bloques[n].sprites()[0].palabra

                    guess += chr(event.key)

                    if guess == palabra:
                        aciertos += 1
                        for sprites in bloques[n]:
                            sprites.kill()
                            
                        n+=1
                        guess = ""
                    elif guess in palabra:
                        
                        while m < len(guess):
                            if guess[m] == palabra[m]:
                                next_letter = True
                            else: 
                                next_letter = False
                            m+=1
                        m = 0
                                
                    else: guess = ""
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bloques[n]:
                    if bombilla.rect.collidepoint(event.pos): #lógica de la ayuda
                        if not bombillaUsada:
                            #ejecutar ayuda
                            letra_a_mostrar = palabra[len(guess)]
                            for grupos in bloques[n]:
                                if grupos.tecla == letra_a_mostrar:
                                    # pintar sobre grupos.image??
                                    hint = (bloques[n], TRANSPARENTE_VERDE, (120,120), (grupos.rect.x, grupos.rect.y))
                                    hint_bool = True
                                    BlitTransparente(pantalla, TRANSPARENTE_VERDE, (120,120), (grupos.rect.x,grupos.rect.y))
                                    break
                        bombillaUsada = True


        if aciertos == CANTIDAD_BLOQUES: fin = True

        # Limpiar pantalla
        pantalla.blit(fondo, (0, 0))

        

        
        # Actualizar y dibujar bloques
        if bombillaUsada:
            bombilla.image = bombillaOff
        else:
            bombilla.image = bombillaON

        pantalla.blit(bombilla.image, (bombilla.rect.x, bombilla.rect.y))
        #cambiar para pintar al reves
        
        if not fin:
            for group in bloquesInvertidos:
                if len(group) != 0:
                    #pygame.draw.rect(pantalla, AZUL_ENTREBASURA, entreBasura)
                    pantalla.blit(entreBasura, (ANCHO//2 - TAM_ENTREIMG//2, ALTO//2-TAM_ENTREIMG//2))
                    for sprite in group:
                        sprite.update()
                        pantalla.blit(sprite.image, sprite.rect)
                        sprite.dibujar_letra(pantalla)
                    if hint_bool == True and group == hint[0]:
                            BlitTransparente(pantalla, hint[1], hint[2], hint[3])
        


        mostrar_texto(guess, pygame.font.Font(None, 30), pantalla, 0, ALTO//2+350, fondo= False, color_letras=NEGRO)
        
        if next_letter:
            BlitTransparente(pantalla, TRANSPARENTE_VERDE, (800, 30), (0, ALTO//2 + 350))
        else:
            BlitTransparente(pantalla, TRANSPARENTE_ROJJO, (800, 30), (0, ALTO//2 + 350))
            guess = ""
        #Resalta la letra que usas, HACERLO DE OTRA FORMA O QUITARLO
        for letra in guess:
            for grupos in bloques[n]:
                if grupos.tecla == letra:
                    BlitTransparente(pantalla, TRANSPARENTE_VERDE, (120,120), (grupos.rect.x,grupos.rect.y))
                    break

        # Calcular tiempo transcurrido
        if not fin:
            tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio
            tiempo_restante = max(0, tiempoLimite - tiempo_transcurrido // 1000)

        # Mostrar tiempo restante en pantalla
        mostrar_texto("Tiempo restante: " + str(tiempo_restante), pygame.font.Font(None, 36), pantalla, 10, 10)
        #Verificar si quedan bloques
        if fin and aciertos==CANTIDAD_BLOQUES:
            mostrar_texto("ENHORABUENA", pygame.font.Font(None, 36), pantalla, ANCHO/2, ALTO/2, centrado=True)
            mostrar_texto("Has conseguido limpiar la pila de basura en: " + str(TIEMPO_LIMITE-tiempo_restante) + "s", pygame.font.Font(None, 36), pantalla,  ANCHO/2, ALTO/2 + 50, centrado=True)
            

        # Verificar si se acabó el tiempo
        if tiempo_restante==0:
            mostrar_texto("¡Se acabó el tiempo!", pygame.font.Font(None, 72), pantalla, ANCHO//2, ALTO//2, centrado= True)
            fin = True
            

        # Actualizar pantalla
        pygame.display.flip()

        # Controlar la velocidad de actualización
        reloj.tick()

if __name__ == '__main__':
    main()


"""#idea para cambiar juego -> añadir boton de pista, de saltarte una palabra...

Cuatroletras = ["caja", "lixo", "lata", "ropa", "tapa", "rata", "alga", "azul", "olor"]
CincoLetras  = ["resto", "sucio", "bolsa", "verde", "latas", "raton", "hedor", "tirar", "mugre"]
SeisLetras   = ["basura", "carton", "vidrio", "reusar", "limpio", "restos", "bodrio", "birria", "sarama", "sobras"]
SieteLetras  = ["bazofia", "podrido", "residuo", "desecho", "vertido"]
OchoLetras   = ["amarillo", "papelera", "reciclar", "escombro", "desechos", "suciedad"]"""
