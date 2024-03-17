import pygame
import random
import sys
from GarbageTowers.bloquePila import Bloque
from GarbageTowers.bloqueClicable import ClicableObject
from ArcadeMachinePopup.textClass import Text
from ArcadeMachinePopup.buttonClass import Boton
from ArcadeMachinePopup.popUpClass import PopUp
from ResourceManager import ResourceManager

# Init pygame
pygame.init()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (47, 55, 65)
GREEN = (0, 255, 0, 100)  # Alfa 0 para transparencia
RED = (255,0,0,100)
YELLOW = (222, 196, 65)
TRANSPARENT = (0, 0, 0, 50)

# SCREEN 
WIDTH = 800
HEIGHT = 800

# TRASH BAGS
WIDTH_BLOQUE = 120
HEIGHT_BLOQUE = 120

# WORDS
NBLOCKS = 5
SIZES = 5

# DIVIDER
SIZE_FLOOR = WIDTH_BLOQUE*3

# RESOURCE MANAGER
RM = ResourceManager()

# TIME LIMIT
LIMIT_TIME = 60
TIME_PENAL = 5

# DIFFERENT WORDS RELATED WITH GARBAGE
words = [["caja", "lixo", "lata", "ropa", "tapa", "rata", "azul", "olor"], 
            ["resto", "sucio", "bolsa", "verde", "latas", "raton", "hedor", "tirar", "mugre"], 
            ["basura", "carton", "vidrio", "reusar", "limpio", "restos", "bodrio", "sarama", "sobras"], 
            ["bazofia", "podrido", "residuo", "desecho", "vertido"], 
            ["amarillo", "papelera", "reciclar", "escombro", "morralla", "suciedad"]]

"""definitions = [["Se tira al papel", "Sinónimo de basura en gallego", "Hecha de aluminio", "Apor al revés", "Usado para cerrar botellas",
                 "Animal de alcantarilla", "Contenedor del cartón", "Lo genera la basura"], 
                 ["Residuo de la basura", "Sinónimo de manchado", 
                 "Donde se mete la basura", "Contenedor del vidrio", "Hechas de aluminio", "Animal", "Mal olor", "echar algo a la basura", 
                 "suciedad grasienta"], 
                 ["Conjunto de residuos", "Contenedor azul", "Contenedor verde", "Sinónimo de reutilizar",
                 "Antónimo de sucio", "Sinónimo de sobras", "Sinónimo de bazofia", "Sinónimo de suciedad", "Exceso"], 
                 ["Desechos de comida",
                 "Descompuesto", "Resultante de la destrucción de algo", "Aquello que queda", "Derramamiento de tóxicos"],
                 ["Contenedor de inorgánicos", "Recipiente para desperdicios", "Clasificar basura", "desecho de la construcción",
                 "Mezcla de cosas inútiles", "Porquería, grasa, mancha"]]"""
                 

# Array with positions for all the letters on the screen
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


# Function for loading array of img from the resource manager
def load_img():
    images = []
    for img in RM.pile_blocks:
        images += img.get()
    return images

# Function for starting or stopping the music
def music(stop = False):
    if not stop:
        pygame.mixer.music.load("GarbageTowers/music/music2.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    else: pygame.mixer.music.stop()


# Function for showing text on the screen
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

# Function for creating the list of sprites (words)
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

# Function for creating the garbage pile
def createMountain():
    # chose the level and words for each level of the pile
    i = 0
    aux = -1
    mountain = []
    n=3 # incremental difficulty
    
    while i<NBLOCKS: 
        
        if aux == -1:
            size = random.randint(0,SIZES-n)
        else: 
            size = random.randint(aux, SIZES-n)
        
        repeated = True
        while repeated:
            #wordN = random.randint(0, len(words[size])-1)
            word = random.choice(words[size])
            #word = words[size][wordN]
            if word not in mountain:
                repeated = False
        
        mountain.append(word)
        aux = size
        i = i+1
        if n>1:
            n-=1
    return mountain
    
# Function for using blit with Translucid surfaces
def transBlit(screen, color, size, coord):
    translucid_screen = pygame.Surface(size, pygame.SRCALPHA)
    translucid_screen.fill(color)
    screen.blit(translucid_screen, coord)

# Function called when the game is finished
def exit_game(score):
    return score

# Main function for the game
def main():
    music()

    # create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Juego de Bloques')

    # load resources
    bg = pygame.transform.scale(RM.pile_bg.get(), (800,800))
    fuenteGP = "ArcadeMachinePopup/fuentes/game_power.ttf"
    fuente8Bit = "ArcadeMachinePopup/fuentes/8Bit.ttf"
    lightBulbON = pygame.transform.scale(RM.pile_lightOn.get(), (50,50))
    lightBulbOff = pygame.transform.scale(RM.pile_lightOff.get(), (50,50))
    floor = pygame.transform.scale(RM.pile_floor.get(), (SIZE_FLOOR, SIZE_FLOOR))

    images_blocks = RM.pile_blocks
    
    screen.blit(bg, (0, 0))

    # Create list of blocks
    MountainArray= createMountain() 

    # Create list of list of blocks
    blocks = []
    i = 0
    for word in MountainArray: 
        
        blocks.append(pygame.sprite.Group())
        img = pygame.transform.scale(random.choice(images_blocks).get(), (WIDTH_BLOQUE, HEIGHT_BLOQUE))
        blocks[i] = blockList(img, blocks[i], word, len(word))
        i = i+1

    # Create clickable obj
    lightBulb = ClicableObject(WIDTH-50, HEIGHT-100, lightBulbON)

    # Create timer
    timer = pygame.time.Clock()

    # Initial Time
    limitTime = LIMIT_TIME
    startTime = pygame.time.get_ticks()

    # Vars for the main loop
    successes = 0
    guess = ""
    n = 0
    m=0
    score = 0

    next_letter = False
    end = False
    objectCreated = False

    hint_num = 3
    hint_bool = False

    running = True

    invertedBlocks = blocks[::-1]

    # Preparing different sounds for the game
    letter_sound = pygame.mixer.Sound("GarbageTowers/music/right_letter.wav")
    word_sound = pygame.mixer.Sound("GarbageTowers/music/right_word.wav")
    letter_sound.set_volume(0)
    sound_channel = letter_sound.play()
    letter_sound.set_volume(0.2)
    word_sound.set_volume(0.7)
    
    
    # Main loop
    while running:
        isKey = True
        if not end:
            word = blocks[n].sprites()[0].word

        # Event handler
        for event in pygame.event.get():

            # Exiting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # key pressed
            if event.type == pygame.KEYDOWN:

                if not end:

                    #Check if its an ASCII letter
                    try:
                        chr(event.key)
                    except:
                        isKey = False

                    if blocks and isKey:
                        
                        word = blocks[n].sprites()[0].word
                        guess += chr(event.key)

                        # WORD GUESSED
                        if guess == word:
                            word_sound.play()
                            successes += 1
                            for sprites in blocks[n]:
                                sprites.kill()     
                            n+=1
                            guess = ""
                        
                        # LETTER GUESSED
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

                        # MISS
                        if not next_letter: 
                            guess = "" 
                            if limitTime-TIME_PENAL <= 0:
                                end = True
                                limitTime = 0
                            else:
                                limitTime -= TIME_PENAL

            # Mouse button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not end:
                    if blocks[n]:

                        # HINT
                        if lightBulb.rect.collidepoint(event.pos): #lógica de la ayuda
                            if hint_num > 0:
                                # Use hint
                                letter_to_show = word[len(guess)]
                                for groups in blocks[n]:
                                    if groups.key == letter_to_show:
                                        hint = (blocks[n], GREEN, (120,120), (groups.rect.x, groups.rect.y))
                                        hint_bool = True
                                        break
                                hint_num -= 1

                # PopUp end game
                if end:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if window.get_rect().collidepoint(mouse_x, mouse_y):
                            for btn in window.buttons:
                                if btn.rect.collidepoint(mouse_x, mouse_y):
                                    if btn.action == "REINICIAR":
                                        music(True)
                                        return main()
                                    elif btn.action == "SALIR":
                                        music(True)
                                        return exit_game(score)


        if successes == NBLOCKS: end = True

        # Clean screan
        screen.blit(bg, (0, 0))

        # Update lightBulb
        if hint_num <= 0:
            lightBulb.image = lightBulbOff
        else:
            lightBulb.image = lightBulbON

        screen.blit(lightBulb.image, (lightBulb.rect.x, lightBulb.rect.y))
        
        
        if not end:

            # Draw blocks
            for group in invertedBlocks:
                if len(group) != 0:
                    screen.blit(floor, (WIDTH//2 - SIZE_FLOOR//2, HEIGHT//2-SIZE_FLOOR//2))
                    for sprite in group:
                        sprite.update()
                        screen.blit(sprite.image, sprite.rect)
                        sprite.draw_letter(screen)
                        
                    if hint_bool and group == hint[0]:
                            transBlit(screen, hint[1], hint[2], hint[3])
                    
            if next_letter:
                transBlit(screen, GREEN, (800, 30), (0, HEIGHT//2 + 350))
            else:
                transBlit(screen, RED, (800, 30), (0, HEIGHT//2 + 350))
                guess = ""

            # Highlight letters pressed
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
                        
        # Print guess on Screen
        showText(guess, pygame.font.Font(fuente8Bit, 30), screen, 0, HEIGHT//2+350, bg= False, letter_color=BLACK)
        
            
        # Print remaining time
        showText("Tiempo restante: " + str(remaining_time), pygame.font.Font(fuente8Bit, 30), screen, 10, 10)
        score = successes * 100

        # Game over
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
                    Boton(popup_x + popup_width // 2, popup_y + popup_height // 3 + 160, 100, 40, "CONTINUAR", fuenteGP, TRANSPARENT, BLACK, 40, "SALIR")
                ]

                window = PopUp(popup_x, popup_y, popup_width, popup_height, 60, YELLOW, 8, BLACK, buttons, game_over_text, rotations)
            
            window.draw(screen)

        if end and successes==NBLOCKS:
            showText("Has conseguido limpiar la pila de basura en: " + str(LIMIT_TIME-remaining_time) + "s", pygame.font.Font(fuente8Bit, 26), screen,  WIDTH/2, HEIGHT/2 + 200, centered=True)
            
        # Check if time is up
        if remaining_time==0:
            showText("¡Se acabó el tiempo!", pygame.font.Font(fuente8Bit, 36), screen, WIDTH//2, HEIGHT//2 + 200, centered= True)
            end = True
            
        # Update screen
        pygame.display.flip()

        timer.tick()

    pygame.quit()
    return score

if __name__ == '__main__':
    main()



