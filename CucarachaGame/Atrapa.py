import pygame
import random
from CucarachaGame.ClassCucaracha import Cucaracha
from CucarachaGame.ClassAgujero import Agujero
from CucarachaGame.ClassSlowItem import SlowItem
from CucarachaGame.ClassSpeedItem import SpeedItem
from CucarachaGame.CucaPop.popUpClass import PopUp
from CucarachaGame.CucaPop.textClass import Text
from CucarachaGame.CucaPop.buttonClass import Boton
from ResourceManager import ResourceManager

pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 200  # Cell size for hole grid
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE  # Number of rows and columns for the grid
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atrapa Cucarachas")

#colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (249, 247, 98)
TRANSPARENT = (0, 0, 0, 50)
BLUE = (12, 18, 58)

global a, b    
a=0
b=0
CELL_SIZE = 200
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
fuenteGP = "ArcadeMAchinePopup/fuentes/game_power.ttf"


items_shown = 0
items_mostrados = 0 
cucarachas_mostradas = 0 
spawn_timer = 0

cucarachas = pygame.sprite.Group()
slow_items = pygame.sprite.Group()
speed_items = pygame.sprite.Group()

next_spawn_time = random.randint(600, 5000)
item_spawn_time = random.randint(1500, 6000)
speed_spawn_time = random.randint(1000, 5000)
   
show_final_score = False
font = pygame.font.Font(None, 36)
button_width = 300
button_height = 50
button_color = (140, 83, 11)
marco = (0, 0, 0)

def reset_game_variables():
    global in_slow_motion_mode, in_speed_mode
    global items_shown, items_mostrados, cucarachas_mostradas, spawn_timer
    global a, b

    # Reiniciar todas las variables del juego
    in_slow_motion_mode = False
    in_speed_mode = False
    items_shown = 0
    items_mostrados = 0 
    cucarachas_mostradas = 0 
    spawn_timer = 0
    a = 0
    b = 0

def initialize_pygame():
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT)), pygame.time.Clock()
window, clock = initialize_pygame()
resource_manager = ResourceManager()

# ITEMS
def update_slow_items():
    spawn_slow_item()
    slow_items.update()  # Update the status of the slowItem
    slow_items.draw(window)  # Draw the slowItem in the window
    
def spawn_slow_item():
    global items_mostrados, spawn_timer, item_spawn_time
    agujeros = create_holes()

    if spawn_timer >= item_spawn_time and items_mostrados==0:
        slow_item = SlowItem()
        random_hole = random.choice(agujeros.sprites())
        slow_item.rect.center = random_hole.rect.center
        spawn_timer = 0
        slow_item.active = True
        slow_item.spawn_time = pygame.time.get_ticks()
        slow_items.add(slow_item)
        items_mostrados += 1

def enter_slow_motion_mode():
    global in_slow_motion_mode, a
    
    in_slow_motion_mode = True
    if a<1:
        pygame.mixer.music.load("CucarachaGame/Music/baile_slow.ogg")  
        pygame.mixer.music.play(-1) 
    a+=1    

def update_speed_items():
    spawn_speed_item()
    speed_items.update()
    speed_items.draw(window)       
  
def spawn_speed_item():
    agujeros = create_holes()
    global items_shown, spawn_timer, speed_spawn_time
    if spawn_timer >= speed_spawn_time and items_shown == 0 :
        speed_item = SpeedItem()
        random_hole = random.choice(agujeros.sprites())
        speed_item.rect.center = random_hole.rect.center
        spawn_timer = 0
        speed_item.active = True
        speed_item.spawn_time = pygame.time.get_ticks()
        speed_items.add(speed_item)
        items_shown += 1

def enter_speed_mode():
    global in_speed_mode, b
    in_speed_mode = True
    if b<1:
        pygame.mixer.music.load("CucarachaGame/Music/baile_speed.ogg")  
        pygame.mixer.music.play(-1) 
    b+=1   

# Holes, MUSIC and BACKGROUND
def create_holes():
    agujeros = pygame.sprite.Group()
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2

            if in_slow_motion_mode:
                hole = pygame.transform.scale(resource_manager.hole_slow.get(), (CELL_SIZE - 50, CELL_SIZE - 50))
            elif in_speed_mode:
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
    if in_slow_motion_mode:
        background =  pygame.transform.scale(resource_manager.background_slow.get(), (WIDTH, WIDTH))
    elif in_speed_mode:
        background =  pygame.transform.scale(resource_manager.background_speed.get(), (WIDTH, WIDTH))
    else: 
        background =  pygame.transform.scale(resource_manager.background_image.get(), (WIDTH, WIDTH))

    window.blit(background, (0, 0))

def draw_holes():
    agujeros = create_holes()
    for agujero in agujeros:
            window.blit(agujero.image, agujero.rect.topleft)


# Handle clicks
def handle_events(score):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for cucaracha in cucarachas:
                if cucaracha.active and cucaracha.rect.collidepoint(event.pos):
                    handle_cucaracha_click(cucaracha)
                    score +=1
            for slow_item in slow_items:
                if slow_item.active and slow_item.rect.collidepoint(event.pos):
                    handle_slow_item_click(slow_item)
            for speed_item in speed_items:
                if speed_item.active and speed_item.rect.collidepoint(event.pos):
                    handle_speed_item_click(speed_item)        

    return score

def handle_slow_item_click(item):
    global in_slow_motion_mode, in_speed_mode
    item.kill()  # Delete item
    item.active = False  # Deactivate the item
    in_slow_motion_mode = True  # Enter slowmode
    in_speed_mode = False

def handle_speed_item_click(item):
    global in_speed_mode, in_slow_motion_mode
    item.kill()  # Delete item
    item.active = False  # Deactivate the item
    in_speed_mode = True  # Enter en speedmode
    in_slow_motion_mode = False    

def handle_cucaracha_click(cucaracha):
    insect = pygame.transform.scale(resource_manager.insect.get(), (80, 80))
    cucaracha.active = False
    cucaracha.kill()
    cell_center = (cucaracha.rect.centerx // CELL_SIZE * CELL_SIZE + CELL_SIZE // 2,
                   cucaracha.rect.centery // CELL_SIZE * CELL_SIZE + CELL_SIZE // 2)
    window.blit(insect, (cell_center[0] - insect.get_width(), cell_center[1] - insect.get_height() // 2))

    pygame.display.flip()
    pygame.time.delay(300)

# CUCARACHA  
def update_cucarachas():
    spawn_cucaracha()
    cucarachas.update(in_slow_motion_mode, in_speed_mode)
    cucarachas.draw(window)

def spawn_cucaracha():
    agujeros = create_holes()

    global spawn_timer, cucarachas_mostradas, next_spawn_time
    spawn_timer += clock.get_time()
    if spawn_timer >= next_spawn_time and cucarachas_mostradas < 16:
        spawn_timer = 0
        next_spawn_time = random.randint(2000, 5000)
        random_hole = random.choice(agujeros.sprites())
        cucaracha = Cucaracha()
        cucaracha.rect.center = random_hole.rect.center
        cucaracha.active = True
        cucaracha.spawn_time = pygame.time.get_ticks()
        cucarachas.add(cucaracha)
        cucarachas_mostradas += 1

#FINAL SCORE
def exit_game(score):
    return score
   
def draw_final_score_screen(score):
    if not(score>0):
        score=0

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
            
    window.draw(window)


# Main game loop
def main():
    global in_slow_motion_mode, in_speed_mode 
    running = True
    in_slow_motion_mode = False
    in_speed_mode = False
    game_over = False

    time_in_slow_motion = 0 
    time_in_speed_mode = 0
    score = 0
    
    
    play_music()

    while running:
        if not game_over:    
            draw_background()
            draw_holes()
            score = handle_events(score)
            # if not handle_events():
            #     break
        
            update_slow_items()
            update_cucarachas()
            update_speed_items()
            
            if in_slow_motion_mode:
                enter_slow_motion_mode()   
                time_in_slow_motion += clock.get_time() / 1000  # Convert time in milliseconds to seconds
                
                # If more than 10 seconds have passed, exit slow mode
                if time_in_slow_motion > 12:
                    in_slow_motion_mode = False
                    pygame.mixer.music.load("CucarachaGame/Music/baile.ogg")  
                    pygame.mixer.music.play(-1)          
            elif in_speed_mode:
                enter_speed_mode()
                time_in_speed_mode += clock.get_time() / 1000
                if time_in_speed_mode > 11:  
                    in_speed_mode = False
                    pygame.mixer.music.load("CucarachaGame/Music/baile.ogg") 
                    pygame.mixer.music.play(-1)    

            if cucarachas_mostradas > 1:  # Exit the game when you reach 10 cockroaches
                game_over = True 


        if game_over:
            pygame.mixer.music.stop()  

            popup_width = 400  
            popup_height = 300  
            popup_x = (WIDTH - popup_width) // 2 
            popup_y = (HEIGHT - popup_height) // 2 

            rotations = [0, 0]

            game_over_text = [
                Text("Game Over", 60, YELLOW, popup_x + popup_width // 2, popup_y + popup_height // 3 - 20, True, fuenteGP),
                Text(f"Score: {score}", 50, YELLOW, popup_x + popup_width // 2, popup_y + popup_height // 3 + 30, True, fuenteGP)
            ]

            buttons = [
                Boton(popup_x + popup_width // 2, popup_y + popup_height // 3 + 110, 100, 40, "REINICIAR", fuenteGP, TRANSPARENT, YELLOW, 40, "REINICIAR"),
                Boton(popup_x + popup_width // 2, popup_y + popup_height // 3 + 160, 100, 40, "SALIR", fuenteGP, TRANSPARENT, YELLOW, 40, "SALIR")
            ]

            final_score_popup = PopUp(popup_x, popup_y, popup_width, popup_height, 60, BLUE, 8, BLACK, buttons, game_over_text, rotations)

            final_score_popup.draw(window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game_over:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if final_score_popup.get_rect().collidepoint(mouse_x, mouse_y):
                            for boton in final_score_popup.botones:
                                if boton.rect.collidepoint(mouse_x, mouse_y):
                                    if boton.accion == "REINICIAR":
                                        reset_game_variables()
                                        return main()
                                    elif boton.accion == "SALIR":
                                        return exit_game(score)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return score
