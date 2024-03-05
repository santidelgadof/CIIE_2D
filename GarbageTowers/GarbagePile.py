import pygame
import random
import sys
import os
from GarbageTowers.bloquePila import Bloque
from GarbageTowers.bloqueClicable import ClicableObject
from ArcadeMachinePopup.textClass import Text
from ArcadeMachinePopup.buttonClass import Boton
from ArcadeMachinePopup.popUpClass import PopUp
from ResourceManager import ResourceManager

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (47, 55, 65)
GREEN = (0, 255, 0, 100)  # Alfa 0 para transparencia
RED = (255,0,0,100)
YELLOW = (222, 196, 65)
TRANSPARENT = (0, 0, 0, 50)

# Definir dimensiones de la screen
WIDTH = 800
HEIGHT = 800

# Definir sizeaño y cantidad de blocks
WIDTH_BLOQUE = 120
HEIGHT_BLOQUE = 120
#Cantidad de palabras
NBLOCKS = 5
SIZES = 5

SIZE_FLOOR = WIDTH_BLOQUE*3

RM = ResourceManager()

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
    for img in RM.pile_blocks:
        images += img.get()
    return images

def music(stop = False):
    if not stop:
        pygame.mixer.music.load("GarbageTowers/music/music2.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    else: pygame.mixer.music.stop()


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

def exit_game(score):
    return score

def createMountain():
    #elegir orden y words de los niveles de la montaña
    i = 0
    aux = 9
    mountain = []
    n=3 #dificultad incremental
    
    while i<NBLOCKS: 
        
        if aux == 9:
            size = random.randint(0,SIZES-n)
        else: 
            size = random.randint(aux, SIZES-n)
        
        repeated = True
        while repeated:
            word = random.choice(words[size])
            if word not in mountain:
                repeated = False
        
        mountain.append(word)
        aux = size
        i = i+1
        if n>0:
            n-=1
    return mountain
    
def transBlit(screen, color, size, coord):
    screen_transparente = pygame.Surface(size, pygame.SRCALPHA)
    screen_transparente.fill(color)
    screen.blit(screen_transparente, coord)


# Función principal del juego
def main():
    music()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Juego de Bloques')

    bg = pygame.transform.scale(RM.pile_bg.get(), (800,800))
    fuenteGP = "ArcadeMachinePopup/fuentes/game_power.ttf"
    fuente8Bit = "ArcadeMachinePopup/fuentes/8Bit.ttf"
    lightBulbON = pygame.transform.scale(RM.pile_lightOn.get(), (50,50))
    lightBulbOff = pygame.transform.scale(RM.pile_lightOff.get(), (50,50))
    floor = pygame.transform.scale(RM.pile_floor.get(), (SIZE_FLOOR, SIZE_FLOOR))

    images_blocks = RM.pile_blocks
    
    screen.blit(bg, (0, 0))

    MountainArray = createMountain() #crea la lista de words

     # Crear lista de lista de blocks con las letras para cada word
    blocks = []
    i = 0
    for word in MountainArray: 
        
        blocks.append(pygame.sprite.Group())
        img = pygame.transform.scale(random.choice(images_blocks).get(), (WIDTH_BLOQUE, HEIGHT_BLOQUE))
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
    score = 0

    next_letter = False
    end = False
    objectCreated = False
    lightBulbUsada = False
    hint_bool = False
    running = True

    invertedBlocks = blocks[::-1]

    letter_sound = pygame.mixer.Sound("GarbageTowers/music/right_letter.wav")
    word_sound = pygame.mixer.Sound("GarbageTowers/music/right_word.wav")
    letter_sound.set_volume(0)
    sound_channel = letter_sound.play()
    letter_sound.set_volume(0.2)
    word_sound.set_volume(0.7)
    
    
    # Ciclo principal del juego
    while running:
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
                            if limitTime-5 <= 0:
                                end = True
                                limitTime = 0
                            else:
                                limitTime -= 5

                        word = blocks[n].sprites()[0].word

                        guess += chr(event.key)

                        if guess == word:
                            word_sound.play()
                            successes += 1
                            for sprites in blocks[n]:
                                sprites.kill()     
                            n+=1
                            guess = ""
                        elif guess in word:
                            
                            while m < len(guess):
                                if guess[m] == word[m]:
                                    if sound_channel.get_busy():
                                        letter_sound.stop()
                                    
                                    sound_channel = letter_sound.play()
                                    
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

                if end:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if window.get_rect().collidepoint(mouse_x, mouse_y):
                            for boton in window.botones:
                                if boton.rect.collidepoint(mouse_x, mouse_y):
                                    if boton.accion == "REINICIAR":
                                        music(True)
                                        return main()
                                    elif boton.accion == "SALIR":
                                        music(True)
                                        return exit_game(score)


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
                        
            
        showText(guess, pygame.font.Font(fuente8Bit, 30), screen, 0, HEIGHT//2+350, bg= False, letter_color=BLACK)
        
            
        # Mostrar tiempo restante en screen
        showText("Tiempo restante: " + str(remaining_time), pygame.font.Font(fuente8Bit, 30), screen, 10, 10)
        score = successes * 100

        if end:
            if not objectCreated:
                objectCreated = True

                popup_width = 400  
                popup_height = 300  
                popup_x = (WIDTH - popup_width) // 2 
                popup_y = (HEIGHT - popup_height) // 2 

                rotations = [0, 0]

                game_over_text = [
                    Text("Game Over", 60, BLACK, popup_x + popup_width // 2, popup_y + popup_height // 3 - 20, True, fuenteGP),
                    Text(f"Score: {score}", 50, BLACK, popup_x + popup_width // 2, popup_y + popup_height // 3 + 30, True, fuenteGP)
                ]

                buttons = [
                    Boton(popup_x + popup_width // 2, popup_y + popup_height // 3 + 110, 100, 40, "REINICIAR", fuenteGP, TRANSPARENT, BLACK, 40, "REINICIAR"),
                    Boton(popup_x + popup_width // 2, popup_y + popup_height // 3 + 160, 100, 40, "SALIR", fuenteGP, TRANSPARENT, BLACK, 40, "SALIR")
                ]

                window = PopUp(popup_x, popup_y, popup_width, popup_height, 60, YELLOW, 8, BLACK, buttons, game_over_text, rotations)
            
            window.draw(screen)

        if end and successes==NBLOCKS:
            showText("Has conseguido limpiar la pila de basura en: " + str(LIMIT_TIME-remaining_time) + "s", pygame.font.Font(fuente8Bit, 26), screen,  WIDTH/2, HEIGHT/2 + 200, centered=True)
            
        # Verificar si se acabó el tiempo
        if remaining_time==0:
            showText("¡Se acabó el tiempo!", pygame.font.Font(fuente8Bit, 36), screen, WIDTH//2, HEIGHT//2 + 200, centered= True)
            end = True
            

        # Actualizar screen
        pygame.display.flip()

        # Controlar la velocidad de actualización
        reloj.tick()

    pygame.quit()
    return score

if __name__ == '__main__':
    main()


"""#idea para cambiar juego -> añadir boton de pista, de saltarte una word...

Cuatroletras = ["caja", "lixo", "lata", "ropa", "tapa", "rata", "alga", "azul", "olor"]
CincoLetras  = ["resto", "sucio", "bolsa", "verde", "latas", "raton", "hedor", "tirar", "mugre"]
SeisLetras   = ["basura", "carton", "vidrio", "reusar", "limpio", "restos", "bodrio", "birria", "sarama", "sobras"]
SieteLetras  = ["bazofia", "podrido", "residuo", "desecho", "vertido"]
OchoLetras   = ["amarillo", "papelera", "reciclar", "escombro", "desechos", "suciedad"]"""
