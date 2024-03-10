import pygame
import random
import sys
from pygame.locals import *
from CucarachaGame.ClassCucaracha import Cucaracha
from CucarachaGame.ClassAgujero import Agujero
from CucarachaGame.ClassSlowItem import SlowItem
from CucarachaGame.ClassSpeedItem import SpeedItem
from CucarachaGame.ClassGameVariables import GameVariables
from ArcadeMachinePopup.popUpClass import PopUp
from ArcadeMachinePopup.textClass import Text
from ArcadeMachinePopup.buttonClass import Boton
from ResourceManager import ResourceManager

pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 200  # Cell size for hole grid
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE  # Number of rows and columns for the grid
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atrapa Cucarachas")

# Colors
BLACK = (0, 0, 0)
YELLOW = (249, 247, 98)
TRANSPARENT = (0, 0, 0, 50)
MARRON = (171, 109, 0)

# Font
fuenteGP = "ArcadeMAchinePopup/fuentes/game_power.ttf"

cucarachas = pygame.sprite.Group()
slow_items = pygame.sprite.Group()
speed_items = pygame.sprite.Group()
gameVars = GameVariables()
resource_manager = ResourceManager()

#Spawn
next_spawn_time = random.randint(600, 5000)
item_spawn_time = random.randint(1500, 6000)
speed_spawn_time = random.randint(1000, 5000)


def initialize_pygame():
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT)), pygame.time.Clock()
window, clock = initialize_pygame()


# ITEMS
def update_slow_items():
    spawn_slow_item()
    slow_items.update()  # Update the status of the slowItem
    slow_items.draw(window)  # Draw the slowItem in the window
    
def spawn_slow_item():
    agujeros = create_holes()

    if gameVars.spawn_timer >= item_spawn_time and gameVars.slow_shown==0:
        slow_item = SlowItem()
        random_hole = random.choice(agujeros.sprites())
        slow_item.rect.center = random_hole.rect.center
        gameVars.spawn_timer = 0
        slow_item.active = True
        slow_item.spawn_time = pygame.time.get_ticks()
        slow_items.add(slow_item)
        gameVars.slow_shown += 1

def enter_slow_motion_mode():

    gameVars.in_slow_motion_mode = True
    if gameVars.a<1:
        pygame.mixer.music.load("CucarachaGame/Music/baile_slow.ogg")  
        pygame.mixer.music.play(-1) 
    gameVars.a+=1    

def update_speed_items():
    spawn_speed_item()
    speed_items.update()
    speed_items.draw(window)       
  
def spawn_speed_item():
    agujeros = create_holes()
    
    if gameVars.spawn_timer >= speed_spawn_time and gameVars.speed_shown == 0 :
        speed_item = SpeedItem()
        random_hole = random.choice(agujeros.sprites())
        speed_item.rect.center = random_hole.rect.center
        gameVars.spawn_timer = 0
        speed_item.active = True
        speed_item.spawn_time = pygame.time.get_ticks()
        speed_items.add(speed_item)
        gameVars.speed_shown += 1

def enter_speed_mode():
    gameVars.in_speed_mode = True
    if gameVars.b<1:
        pygame.mixer.music.load("CucarachaGame/Music/baile_speed.ogg")  
        pygame.mixer.music.play(-1) 
    gameVars.b+=1   

# Holes, MUSIC and BACKGROUND
def create_holes():
    agujeros = pygame.sprite.Group()
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2

            if gameVars.in_slow_motion_mode:
                hole = pygame.transform.scale(resource_manager.hole_slow.get(), (CELL_SIZE - 50, CELL_SIZE - 50))
            elif gameVars.in_speed_mode:
                hole =  pygame.transform.scale(resource_manager.hole_speed.get(), (CELL_SIZE - 50, CELL_SIZE - 50))
            else:
                hole = pygame.transform.scale(resource_manager.hole.get(), (CELL_SIZE - 50, CELL_SIZE - 50))

            agujero = Agujero(x, y, hole)
            agujeros.add(agujero)
    return agujeros

def play_music():
    pygame.mixer.music.load("CucarachaGame/Music/baile.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

def draw_background():
    if gameVars.in_slow_motion_mode:
        background =  pygame.transform.scale(resource_manager.background_slow.get(), (WIDTH, WIDTH))
    elif gameVars.in_speed_mode:
        background =  pygame.transform.scale(resource_manager.background_speed.get(), (WIDTH, WIDTH))
    else: 
        background =  pygame.transform.scale(resource_manager.background_image.get(), (WIDTH, WIDTH))

    window.blit(background, (0, 0))

def draw_holes():
    agujeros = create_holes()
    for agujero in agujeros:
            window.blit(agujero.image, agujero.rect.topleft)

# Handle clicks
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for cucaracha in cucarachas:
                if cucaracha.active and cucaracha.rect.collidepoint(event.pos):
                    handle_cucaracha_click(cucaracha)
                    gameVars.score +=1
            for slow_item in slow_items:
                if slow_item.active and slow_item.rect.collidepoint(event.pos):
                    handle_slow_item_click(slow_item)
            for speed_item in speed_items:
                if speed_item.active and speed_item.rect.collidepoint(event.pos):
                    handle_speed_item_click(speed_item)        


def handle_slow_item_click(item):
    item.kill()  # Delete item
    item.active = False  # Deactivate the item
    gameVars.in_slow_motion_mode = True  # Enter slowmode
    gameVars.in_speed_mode = False

def handle_speed_item_click(item):
    item.kill()  # Delete item
    item.active = False  # Deactivate the item
    gameVars.in_speed_mode = True  # Enter en speedmode
    gameVars.in_slow_motion_mode = False    

def handle_cucaracha_click(cucaracha):
    insect = pygame.transform.scale(resource_manager.insect.get(), (80, 80))
    cucaracha.active = False
    cucaracha.Kill()
    cell_center = (cucaracha.rect.centerx // CELL_SIZE * CELL_SIZE + CELL_SIZE // 2,
                   cucaracha.rect.centery // CELL_SIZE * CELL_SIZE + CELL_SIZE // 2)
    window.blit(insect, (cell_center[0] - insect.get_width(), cell_center[1] - insect.get_height() // 2))

    pygame.display.flip()
    pygame.time.delay(300)

# CUCARACHA  
def update_cucarachas():
    spawn_cucaracha()
    cucarachas.update(gameVars.in_slow_motion_mode, gameVars.in_speed_mode)
    cucarachas.draw(window)

def spawn_cucaracha():
    agujeros = create_holes()

    gameVars.spawn_timer += clock.get_time()
    if gameVars.spawn_timer >= next_spawn_time and gameVars.cucarachas_shown < 16:
        gameVars.spawn_timer = 0
        random_hole = random.choice(agujeros.sprites())
        cucaracha = Cucaracha()
        cucaracha.rect.center = random_hole.rect.center
        cucaracha.active = True
        cucaracha.spawn_time = pygame.time.get_ticks()
        cucarachas.add(cucaracha)
        gameVars.cucarachas_shown += 1

#FINAL SCORE
def exit_game():
    return gameVars.score
   
def draw_final_score_screen():
    if not(gameVars.score>0):
        gameVars.score=0

    popup_width = 400  
    popup_height = 300  
    popup_x = (WIDTH - popup_width) // 2 
    popup_y = (HEIGHT - popup_height) // 2 

    rotations = [0, 0]

    game_over_text = [
        Text("Game Over", 60, BLACK, popup_x + popup_width // 2, popup_y + popup_height // 3 - 20, True, fuenteGP),
        Text(f"Score: {gameVars.score}", 50, BLACK, popup_x + popup_width // 2, popup_y + popup_height // 3 + 30, True, fuenteGP)
        ]

    buttons = [
            Boton(popup_x + popup_width // 2, popup_y + popup_height // 3 + 110, 100, 40, "REINICIAR", fuenteGP, TRANSPARENT, BLACK, 40, "REINICIAR"),
            Boton(popup_x + popup_width // 2, popup_y + popup_height // 3 + 160, 100, 40, "SALIR", fuenteGP, TRANSPARENT, BLACK, 40, "SALIR")
        ]

    window = PopUp(popup_x, popup_y, popup_width, popup_height, 60, YELLOW, 8, BLACK, buttons, game_over_text, rotations)
            
    window.draw(window)


# Main game loop
def main():

    running = True
    game_over = False
    
    gameVars.in_slow_motion_mode = False
    gameVars.in_speed_mode = False
    gameVars.score = 0

    time_in_speed_mode = 0
    time_in_slow_motion = 0

    # Start playing the background music
    play_music()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Main game loop
        if not game_over: 

            # Draw the background and holes
            draw_background()
            draw_holes()

            # Handle game events and update game elements
            handle_events()
            update_slow_items()
            update_cucarachas()
            update_speed_items()
            
            # Enter slow motion mode if TRUE
            if gameVars.in_slow_motion_mode:
                enter_slow_motion_mode()   
                # Update the time spent in slow motion
                time_in_slow_motion += clock.get_time() / 1000  # Convert time in milliseconds to seconds
                
                # If more than 12 seconds have passed, exit slow mode
                if time_in_slow_motion > 12:
                    gameVars.in_slow_motion_mode = False
                    # Switch back to the regular background music
                    pygame.mixer.music.load("CucarachaGame/Music/baile.ogg")  
                    pygame.mixer.music.play(-1)  

            # Enter speed mode if TRUE
            elif gameVars.in_speed_mode:
                enter_speed_mode()
                # Update the time spent in speed mode
                time_in_speed_mode += clock.get_time() / 1000

                # If more than 11 seconds have passed, exit speed mode
                if time_in_speed_mode > 11:  
                    gameVars.in_speed_mode = False
                    # Switch back to the regular background music
                    pygame.mixer.music.load("CucarachaGame/Music/baile.ogg") 
                    pygame.mixer.music.play(-1)    

            # End the game when reaching a certain number of shown cucarachas
            if gameVars.cucarachas_shown > 10: 
                game_over = True 

        # Display the final score screen when the game is over
        if game_over:
            pygame.mixer.music.stop() 
            # Display the game over popup window
            popup_width = 400  
            popup_height = 300  
            popup_x = (WIDTH - popup_width) // 2 
            popup_y = (HEIGHT - popup_height) // 2 

            rotations = [0, 0]

            game_over_text = [
                Text("Game Over", 60, YELLOW, popup_x + popup_width // 2, popup_y + popup_height // 3 - 20, True, fuenteGP),
                Text(f"Score: {gameVars.score}", 50, YELLOW, popup_x + popup_width // 2, popup_y + popup_height // 3 + 30, True, fuenteGP)
            ]

            buttons = [
                Boton(popup_x + popup_width // 2, popup_y + popup_height // 3 + 110, 100, 40, "RESTART", fuenteGP, TRANSPARENT, YELLOW, 40, "RESTART"),
                Boton(popup_x + popup_width // 2, popup_y + popup_height // 3 + 160, 100, 40, "EXIT", fuenteGP, TRANSPARENT, YELLOW, 40, "EXIT")
            ]

            final_score_popup = PopUp(popup_x, popup_y, popup_width, popup_height, 60, MARRON, 8, BLACK, buttons, game_over_text, rotations)

            final_score_popup.draw(window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game_over:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if final_score_popup.get_rect().collidepoint(mouse_x, mouse_y):
                            for boton in final_score_popup.botones:
                                if boton.rect.collidepoint(mouse_x, mouse_y):
                                    if boton.accion == "RESTART":
                                        gameVars.reset()
                                        return main()
                                    elif boton.accion == "EXIT":
                                        return exit_game()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return gameVars.score
