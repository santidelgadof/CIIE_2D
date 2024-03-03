import pygame
import random
import sys
import os
from bloquePila import Bloque
from bloqueClicable import ClicableObject

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (47, 55, 65)
GREEN = (0, 255, 0, 100)  # Alfa 0 para transparencia
RED = (255,0,0,100)

# Definir dimensiones de la screen
WIDTH = 800
HEIGHT = 800

# Definir sizeaño y cantidad de blocks
WIDTH_BLOQUE = 120
HEIGHT_BLOQUE = 120
NBLOCKS = 3
SIZES = 5

SIZE_FLOOR = WIDTH_BLOQUE*3

# Definir tiempo límite en segundos
LIMIT_TIME = 60

words = [["caja", "lixo", "lata", "ropa", "tapa", "rata", "alga", "azul", "olor"], 
            ["resto", "sucio", "bolsa", "verde", "latas", "raton", "hedor", "tirar", "mugre"], 
            ["basura", "carton", "vidrio", "reusar", "limpio", "restos", "bodrio", "birria", "sarama", "sobras"], 
            ["bazofia", "podrido", "residuo", "desecho", "vertido"], 
            ["amarillo", "papelera", "reciclar", "escombro", "desechos", "suciedad"]]


Poswords = [
               [(WIDTH//2-WIDTH_BLOQUE, HEIGHT//2-HEIGHT_BLOQUE), (WIDTH//2, HEIGHT//2-HEIGHT_BLOQUE), 
                (WIDTH//2-WIDTH_BLOQUE, HEIGHT//2), (WIDTH//2, HEIGHT//2)], 

               [(WIDTH//2-WIDTH_BLOQUE//2, HEIGHT//2-HEIGHT_BLOQUE//2), (WIDTH//2-WIDTH_BLOQUE//2, HEIGHT//2-int(HEIGHT_BLOQUE*1.5)), 
                (WIDTH//2+WIDTH_BLOQUE//2, HEIGHT//2-HEIGHT_BLOQUE//2), (WIDTH//2-WIDTH_BLOQUE//2, HEIGHT//2+HEIGHT_BLOQUE//2),
                (WIDTH//2-int(WIDTH_BLOQUE*1.5), HEIGHT//2-HEIGHT_BLOQUE//2)],

               [(WIDTH//2-int(WIDTH_BLOQUE*1.5), HEIGHT//2-HEIGHT_BLOQUE), (WIDTH//2-WIDTH_BLOQUE//2, HEIGHT//2-HEIGHT_BLOQUE),
                (WIDTH//2+WIDTH_BLOQUE//2, HEIGHT//2-HEIGHT_BLOQUE), (WIDTH//2-int(WIDTH_BLOQUE*1.5), HEIGHT//2), 
                (WIDTH//2-WIDTH_BLOQUE//2, HEIGHT//2), (WIDTH//2+WIDTH_BLOQUE//2, HEIGHT//2)], 
                
               [(WIDTH//2-int(WIDTH_BLOQUE*1.5), HEIGHT//2-int(HEIGHT_BLOQUE*1.5)), (WIDTH//2-WIDTH_BLOQUE//2, HEIGHT//2-int(HEIGHT_BLOQUE*1.5)), 
                (WIDTH//2+WIDTH_BLOQUE//2, HEIGHT//2-int(HEIGHT_BLOQUE*1.5)), (WIDTH//2-WIDTH_BLOQUE//2, HEIGHT//2-HEIGHT_BLOQUE//2), 
                (WIDTH//2-int(WIDTH_BLOQUE*1.5), HEIGHT//2+HEIGHT_BLOQUE//2), (WIDTH//2-WIDTH_BLOQUE//2, HEIGHT//2+HEIGHT_BLOQUE//2), 
                (WIDTH//2+WIDTH_BLOQUE//2, HEIGHT//2+HEIGHT_BLOQUE//2)], 
              
               [(WIDTH//2-int(WIDTH_BLOQUE*1.5), HEIGHT//2-int(HEIGHT_BLOQUE*1.5)), (WIDTH//2-WIDTH_BLOQUE//2, HEIGHT//2-int(HEIGHT_BLOQUE*1.5)), 
                (WIDTH//2+WIDTH_BLOQUE//2, HEIGHT//2-int(HEIGHT_BLOQUE*1.5)), (WIDTH//2+WIDTH_BLOQUE//2, HEIGHT//2-HEIGHT_BLOQUE//2), 
                (WIDTH//2+WIDTH_BLOQUE//2, HEIGHT//2+HEIGHT_BLOQUE//2), (WIDTH//2-WIDTH_BLOQUE//2, HEIGHT//2+HEIGHT_BLOQUE//2), 
                (WIDTH//2-int(WIDTH_BLOQUE*1.5), HEIGHT//2+HEIGHT_BLOQUE//2), (WIDTH//2-int(WIDTH_BLOQUE*1.5), HEIGHT//2-HEIGHT_BLOQUE//2)]
                ]

def load_img():
    images = []
    for folder in os.listdir("repositorio//CIIE//MinijuegoJavi//images//blocks"):
        path = os.path.join("repositorio//CIIE//MinijuegoJavi//images//blocks", folder)
        if os.path.isfile(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (WIDTH_BLOQUE, HEIGHT_BLOQUE))
            images.append(img)
    return images

def music():
    pygame.mixer.music.load("repositorio//CIIE//MinijuegoJavi//music//music2.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)


# Función para mostrar text en screen
def showText(text, font, screen, x, y, bg_color = BLACK, letter_color = WHITE, borderr_color = DARK_BLUE, centered = False, bg = True, border = True,  size_border = 4):

    text_object = font.render(text, True, letter_color)
    rectangle_text = text_object.get_rect() 
    if centered:
        rectangle_text.topleft = (x-rectangle_text.width//2, y-rectangle_text.height//2)
    else:
        rectangle_text.topleft = (x, y)

    if bg:
        rectangle = pygame.Rect(rectangle_text.topleft[0], rectangle_text.topleft[1], rectangle_text.width, rectangle_text.height)

        if border:
            pygame.draw.rect(screen, borderr_color, (rectangle[0]-size_border, rectangle[1]-size_border, rectangle[2]+size_border*2, rectangle[3]+size_border*2))
        pygame.draw.rect(screen, bg_color, rectangle)
    
    screen.blit(text_object, rectangle_text)

def blockList(img, blocks, word, nBlocks):
    letras = random.sample(word, nBlocks)
    i = 0
    while i < nBlocks:
        aux = True
        
        block = Bloque(Poswords[nBlocks-4][i][0],
                        Poswords[nBlocks-4][i][1],
                        letras[i],
                        word, 
                        img,
                        WIDTH_BLOQUE, HEIGHT_BLOQUE, 
                        WHITE, DARK_BLUE)
    
        blocks.add(block)
        i=i+1
    return blocks


def createMountain():
    #elegir orden y words de los niveles de la montaña
    i = 0
    aux = 9
    mountain = []
    
    while i<NBLOCKS: 
        
        if aux == 9:
            size = random.randint(0,SIZES-1)
        else: 
            size = random.randint(aux, SIZES-1)
        
        repeated = True
        while repeated:
            word = random.choice(words[size])
            if word not in mountain:
                repeated = False
        
        mountain.append(word)
        aux = size
        i = i+1
    return mountain
    
def transBlit(screen, color, size, coord):
    screen_transparente = pygame.Surface(size, pygame.SRCALPHA)
    screen_transparente.fill(color)
    screen.blit(screen_transparente, coord)


# Función principal del juego
def garbagePile():
    music()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Juego de Bloques')

    images_blocks = load_img()
    bg = pygame.image.load("repositorio//CIIE//MinijuegoJavi//images//bg.jpg").convert()
    bg = pygame.transform.scale(bg, (800,800))
    lightBulbON = pygame.image.load("repositorio//CIIE//MinijuegoJavi//images//lightBulbOn.png")
    lightBulbON = pygame.transform.scale(lightBulbON, (50,50))
    lightBulbOff = pygame.image.load("repositorio//CIIE//MinijuegoJavi//images//lightBulbOff.png")
    lightBulbOff = pygame.transform.scale(lightBulbOff, (50,50))
    floor = pygame.image.load("repositorio//CIIE//MinijuegoJavi//images//floor.jpg")
    floor = pygame.transform.scale(floor, (SIZE_FLOOR, SIZE_FLOOR))

    screen.blit(bg, (0, 0))

    MountainArray = createMountain() #crea la lista de words

     # Crear lista de lista de blocks con las letras para cada word
    blocks = []
    i = 0
    for word in MountainArray: 
        
        blocks.append(pygame.sprite.Group())
        img = random.choice(images_blocks)
        blocks[i] = blockList(img, blocks[i], word, len(word))
        i = i+1

    lightBulb = ClicableObject(WIDTH-50, HEIGHT-100, lightBulbON)
    # Crear reloj
    reloj = pygame.time.Clock()

    # Tiempo inicial
    limitTime = LIMIT_TIME
    startTime = pygame.time.get_ticks()
    successes = 0
    guess = ""
    n = 0
    m=0
    next_letter = False
    end = False
    
    lightBulbUsada = False
    hint_bool = False
    invertedBlocks = blocks[::-1]
    
    # Ciclo principal del juego
    while True:
        isKey = True
        if not end:
            word = blocks[n].sprites()[0].word
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not end:
                    try:
                        chr(event.key)
                    except:
                        isKey = False

                    if blocks and isKey:

                        if not next_letter: 
                            guess = "" 
                            limitTime -= 5

                        word = blocks[n].sprites()[0].word

                        guess += chr(event.key)

                        if guess == word:
                            successes += 1
                            for sprites in blocks[n]:
                                sprites.kill()     
                            n+=1
                            guess = ""
                        elif guess in word:
                            
                            while m < len(guess):
                                if guess[m] == word[m]:
                                    next_letter = True
                                else: 
                                    next_letter = False
                                m+=1
                            m = 0
                                    
                        else: guess = ""
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not end:
                    if blocks[n]:
                        if lightBulb.rect.collidepoint(event.pos): #lógica de la ayuda
                            if not lightBulbUsada:
                                #ejecutar ayuda
                                letter_to_show = word[len(guess)]
                                for groups in blocks[n]:
                                    if groups.key == letter_to_show:
                                        hint = (blocks[n], GREEN, (120,120), (groups.rect.x, groups.rect.y))
                                        hint_bool = True
                                        transBlit(screen, GREEN, (120,120), (groups.rect.x,groups.rect.y))
                                        break
                            lightBulbUsada = True


        if successes == NBLOCKS: end = True

        # Limpiar screen
        screen.blit(bg, (0, 0))

        
        # Actualizar y dibujar blocks
        if lightBulbUsada:
            lightBulb.image = lightBulbOff
        else:
            lightBulb.image = lightBulbON

        screen.blit(lightBulb.image, (lightBulb.rect.x, lightBulb.rect.y))
        #cambiar para pintar al reves
        
        if not end:
            for group in invertedBlocks:
                if len(group) != 0:
                    screen.blit(floor, (WIDTH//2 - SIZE_FLOOR//2, HEIGHT//2-SIZE_FLOOR//2))
                    for sprite in group:
                        sprite.update()
                        screen.blit(sprite.image, sprite.rect)
                        sprite.draw_letter(screen)
                    if hint_bool == True and group == hint[0]:
                            transBlit(screen, hint[1], hint[2], hint[3])
            if next_letter:
                transBlit(screen, GREEN, (800, 30), (0, HEIGHT//2 + 350))
            else:
                transBlit(screen, RED, (800, 30), (0, HEIGHT//2 + 350))
                guess = ""

            #Resalta la letter que usas
            
            for letter in guess:
                for groups in blocks[n]:
                    if groups.key == letter:
                        transBlit(screen, GREEN, (120,120), (groups.rect.x,groups.rect.y))
                        #if  not groups.letra_escrita:
                        #    groups.letra_escrita = True
                        break
                    else:
                        #for gruposs in blocks[n]:
                        #    gruposs.letra_escrita = False
                        #break
                        pass

            time_passed = pygame.time.get_ticks() - startTime
            remaining_time = max(0, limitTime - time_passed // 1000)
                        
            
        showText(guess, pygame.font.Font(None, 30), screen, 0, HEIGHT//2+350, bg= False, letter_color=BLACK)
        
            
        # Mostrar tiempo restante en screen
        showText("Tiempo restante: " + str(remaining_time), pygame.font.Font(None, 36), screen, 10, 10)
        #Verificar si quedan blocks
        if end and successes==NBLOCKS:
            showText("ENHORABUENA", pygame.font.Font(None, 36), screen, WIDTH/2, HEIGHT/2, centered=True)
            showText("Has conseguido limpiar la pila de basura en: " + str(LIMIT_TIME-remaining_time) + "s", pygame.font.Font(None, 36), screen,  WIDTH/2, HEIGHT/2 + 50, centered=True)
            

        # Verificar si se acabó el tiempo
        if remaining_time==0:
            showText("¡Se acabó el tiempo!", pygame.font.Font(None, 72), screen, WIDTH//2, HEIGHT//2, centered= True)
            end = True
            

        # Actualizar screen
        pygame.display.flip()

        # Controlar la velocidad de actualización
        reloj.tick()

if __name__ == '__main__':
    garbagePile()


"""#idea para cambiar juego -> añadir boton de pista, de saltarte una word...

Cuatroletras = ["caja", "lixo", "lata", "ropa", "tapa", "rata", "alga", "azul", "olor"]
CincoLetras  = ["resto", "sucio", "bolsa", "verde", "latas", "raton", "hedor", "tirar", "mugre"]
SeisLetras   = ["basura", "carton", "vidrio", "reusar", "limpio", "restos", "bodrio", "birria", "sarama", "sobras"]
SieteLetras  = ["bazofia", "podrido", "residuo", "desecho", "vertido"]
OchoLetras   = ["amarillo", "papelera", "reciclar", "escombro", "desechos", "suciedad"]"""
