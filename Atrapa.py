import pygame
import random
import sys
from ClassCucaracha import Cucaracha
from ClassAgujero import Agujero
from ClassSlowItem import SlowItem
from ClassSpeedItem import SpeedItem

pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 200  # Tamaño de celda para la cuadrícula de agujeros
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE  # Número de filas y columnas para la cuadrícula
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atrapa Cucarachas")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def initialize_pygame():
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT)), pygame.time.Clock()

def load_images():
    # Las imágenes y sus tamaños pueden cambiar dependiendo de tu implementación específica
    hole = pygame.transform.scale(pygame.image.load("Assets/Agujero.png").convert_alpha(), (CELL_SIZE - 50, CELL_SIZE - 50))
    hole_slow = pygame.transform.scale(pygame.image.load("Assets/Agujero_slow.png").convert_alpha(), (CELL_SIZE - 50, CELL_SIZE - 50))
    hole_speed = pygame.transform.scale(pygame.image.load("Assets/Agujero_speed.png").convert_alpha(), (CELL_SIZE - 50, CELL_SIZE - 50))
    insect = pygame.transform.scale(pygame.image.load("Assets/Insecticida.png").convert_alpha(), (80, 80))
    background_image = pygame.transform.scale(pygame.image.load("Assets/back.jpg").convert(), (WIDTH, HEIGHT))
    background_slow = pygame.transform.scale(pygame.image.load("Assets/back_slow.png").convert(), (WIDTH, HEIGHT))  # Fondo para modo lento
    background_speed = pygame.transform.scale(pygame.image.load("Assets/back_speed.png").convert(), (WIDTH, HEIGHT))
    return hole, hole_slow, insect, background_image, background_slow, hole_speed, background_speed


# ITEMS
def update_slow_items():
    spawn_slow_item()
    slow_items.update()  # Actualiza el estado de los slowItem
    slow_items.draw(window)  # Dibuja los slowItem en la ventana
    
def spawn_slow_item():
    global slow_item, items_mostrados, spawn_timer, item_spawn_time
    if spawn_timer >= item_spawn_time and items_mostrados==0:
        slow_item = SlowItem()
        random_hole = random.choice(agujeros.sprites())
        slow_item.rect.center = random_hole.rect.center
        spawn_timer = 0
        slow_item.active = True
        item_spawn_time = random.randint(1000, 8000)
        slow_item.spawn_time = pygame.time.get_ticks()
        slow_items.add(slow_item)
        items_mostrados += 1

def enter_slow_motion_mode():
    global in_slow_motion_mode, hole, a

    in_slow_motion_mode = True
    hole = hole_slow  # Cambiar el agujero al modo lento
    if a<1:
        pygame.mixer.music.load("Music/baile_slow.mp3")  
        pygame.mixer.music.play(-1) 
    a+=1    

def update_speed_items():
    spawn_speed_item()
    speed_items.update()
    speed_items.draw(window)       
  
def spawn_speed_item():
    global speed_item, items_shown, spawn_timer, speed_spawn_time
    if spawn_timer >= speed_spawn_time and items_shown == 0 :
        speed_item = SpeedItem()
        random_hole = random.choice(agujeros.sprites())
        speed_item.rect.center = random_hole.rect.center
        spawn_timer = 0
        speed_item.active = True
        speed_spawn_time = random.randint(2000, 9000)
        speed_item.spawn_time = pygame.time.get_ticks()
        speed_items.add(speed_item)
        items_shown += 1

def enter_speed_mode():
    global in_speed_mode, hole, b
    in_speed_mode = True
    hole = hole_speed
    if b<1:
        pygame.mixer.music.load("Music/baile_speed.mp3")  
        pygame.mixer.music.play(-1) 
    b+=1   

# Holes, MUSIC and BACKGROUND
def create_holes():
    agujeros = pygame.sprite.Group()
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            agujero = Agujero(x, y, hole)
            agujeros.add(agujero)
    return agujeros

def play_music():
    pygame.mixer.music.load("Music/baile.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

def draw_background():
    global background 
    if in_slow_motion_mode:
        background = background_slow
    elif in_speed_mode:
        background = background_speed    
    else:
        background = background_image

    window.blit(background, (0, 0))

def draw_holes():
    
    if in_slow_motion_mode:
        for agujero in agujeros:
            window.blit(hole_slow, agujero.rect.topleft)
    elif in_speed_mode:
        for agujero in agujeros:
            window.blit(hole_speed, agujero.rect.topleft)        
    else:
        for agujero in agujeros:
            window.blit(agujero.image, agujero.rect.topleft)


# Handle clicks
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for cucaracha in cucarachas:
                if cucaracha.active and cucaracha.rect.collidepoint(event.pos):
                    handle_cucaracha_click(cucaracha)
            for slow_item in slow_items:
                if slow_item.active and slow_item.rect.collidepoint(event.pos):
                    handle_slow_item_click(slow_item)
            for speed_item in speed_items:
                if speed_item.active and speed_item.rect.collidepoint(event.pos):
                    handle_speed_item_click(speed_item)        

    return True

def handle_slow_item_click(item):
    global in_slow_motion_mode, in_speed_mode
    item.kill()  # Eliminar el item del grupo de sprites
    item.active = False  # Desactivar el item
    in_slow_motion_mode = True  # Entrar en slowmode
    in_speed_mode = False

def handle_speed_item_click(item):
    global in_speed_mode, in_slow_motion_mode
    item.kill()  # Eliminar el item del grupo de sprites
    item.active = False  # Desactivar el item
    in_speed_mode = True  # Entrar en slowmode
    in_slow_motion_mode = False    

def handle_cucaracha_click(cucaracha):
    global score
    score += 1
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
def show_final_score_screen():
    draw_final_score_screen()
    while True:
        if not handle_final_score_events():
            break

def draw_final_score_screen():
    global background 
    background = background_image
    pygame.mixer.music.load("Music/end.wav")
    pygame.mixer.music.play()
    window.blit(background, (0, 0))
    final_score_text = font.render("Puntuación final: " + str(score), True, BLACK)
    button_rect = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - button_height) // 2, button_width, button_height)
    pygame.draw.rect(window, marco, button_rect)
    pygame.draw.rect(window, button_color, button_rect.inflate(-4, -4))
    text_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(final_score_text, text_rect.topleft)
    pygame.display.flip()

def handle_final_score_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True

def cargar_cursor(nombre_cursor, tamaño):
    # Carga la imagen desde el directorio actual del programa
    imagen = pygame.image.load(nombre_cursor)
    # Escala la imagen al tamaño deseado
    imagen = pygame.transform.scale(imagen, tamaño)
    # Convierte la imagen en un formato compatible con el cursor
    pygame.mouse.set_cursor((tamaño[0], tamaño[1]), (0, 0), *pygame.cursors.compile(pygame.cursors.sizer_x_strings))
    return imagen

# Main game loop
def main():
    global running, in_slow_motion_mode, in_speed_mode 
    running = True
    in_slow_motion_mode = False
    in_speed_mode = False
    time_in_slow_motion = 0 
    time_in_speed_mode = 0
    play_music()

    while running:
        
        draw_background()
        draw_holes()
        if not handle_events():
            break
       
        update_slow_items()
        update_cucarachas()
        update_speed_items()
        
        if in_slow_motion_mode:
            enter_slow_motion_mode()   
            time_in_slow_motion += clock.get_time() / 1000  # Convertir el tiempo en milisegundos a segundos
            # Si ha pasado más de 10 segundos, salir del modo lento
            if time_in_slow_motion > 12:
                in_slow_motion_mode = False
                pygame.mixer.music.load("Music/baile.ogg")  # Restaurar la música normal
                pygame.mixer.music.play(-1)  # Reproducir la música normal en bucle
                
        elif in_speed_mode:
            enter_speed_mode()
            time_in_speed_mode += clock.get_time() / 1000
            if time_in_speed_mode > 10:  
                in_speed_mode = False
                pygame.mixer.music.load("Music/baile.ogg")  # Restaurar la música normal
                pygame.mixer.music.play(-1)  # Reproducir la música normal en bucle
                

        if cucarachas_mostradas > 10:  # Salir del juego cuando se alcanzan 10 cucarachas
            running = False 
           
        #draw_gif_animation()
        pygame.display.flip()
    
        clock.tick(60)
    show_final_score_screen()

if __name__ == "__main__":
    global a, b    
    a=0
    b=0
    CELL_SIZE = 200
    ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
    window, clock = initialize_pygame()
    hole, hole_slow, insect, background_image, background_slow, hole_speed, background_speed= load_images()
    agujeros = create_holes()
    
    items_shown = 0
    score = 0
    items_mostrados = 0 
    cucarachas_mostradas = 0 
    spawn_timer = 0
    gif_frame_index = 0

    cucarachas = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()
    speed_items = pygame.sprite.Group()

    next_spawn_time = random.randint(500, 5000)
    item_spawn_time = random.randint(1000, 8000)
    speed_spawn_time = random.randint(1000, 6000)
   
    show_final_score = False
    font = pygame.font.Font(None, 36)
    button_width = 300
    button_height = 50
    button_color = (140, 83, 11)
    marco = (0, 0, 0)
    main()
    
    pygame.quit()
    sys.exit()