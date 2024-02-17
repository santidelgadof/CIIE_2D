import pygame
import random
import sys
import numpy as np
from moviepy.editor import VideoFileClip

pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 200  # Tamaño de celda para la cuadrícula de agujeros
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE  # Número de filas y columnas para la cuadrícula
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atrapa Cucarachas")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Cucaracha(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cucaracha.png").convert_alpha()  # Cargar la imagen 
        self.image = pygame.transform.scale(self.image, (70, 70))  # Escalar la imagen 
        self.rect = self.image.get_rect()
        self.active = False
        self.spawn_time = 0

    def update(self):
        if self.active:
            if in_slow_motion_mode:
                if pygame.time.get_ticks() - self.spawn_time >= 1300:  
                    self.active = False
                    self.kill()  # Elimina el sprite del grupo
            elif in_speed_mode:   
                if pygame.time.get_ticks() - self.spawn_time >= 500:  
                    self.active = False
                    self.kill()  # Elimina el sprite del grupo
            else:
                if pygame.time.get_ticks() - self.spawn_time >= 800:  
                    self.active = False
                    self.kill()  # Elimina el sprite del grupo

class Agujero(pygame.sprite.Sprite):
    def __init__(self, x, y, hole_image):
        super().__init__()
        self.image = hole_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pass

class PinkItem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("pink_item.png").convert_alpha(), (80, 80))
        self.rect = self.image.get_rect()
        self.active = False
        self.spawn_time = 0

    def update(self):
        if self.active:
            if pygame.time.get_ticks() - self.spawn_time >= 1000:
                self.active = False
                self.kill()

class SpeedItem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("speed_item.png").convert_alpha(), (80, 80))
        self.rect = self.image.get_rect()
        self.active = False
        self.spawn_time = 0

    def update(self):
        if self.active:
            if pygame.time.get_ticks() - self.spawn_time >= 1500:
                self.active = False
                self.kill()

def initialize_pygame():
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT)), pygame.time.Clock()

def load_images():
    # Las imágenes y sus tamaños pueden cambiar dependiendo de tu implementación específica
    hole = pygame.transform.scale(pygame.image.load("agujero.png").convert_alpha(), (CELL_SIZE - 50, CELL_SIZE - 50))
    hole_slow = pygame.transform.scale(pygame.image.load("agujero_slow.png").convert_alpha(), (CELL_SIZE - 50, CELL_SIZE - 50))
    hole_speed = pygame.transform.scale(pygame.image.load("agujero_speed.png").convert_alpha(), (CELL_SIZE - 50, CELL_SIZE - 50))
    insect = pygame.transform.scale(pygame.image.load("insecticida.png").convert_alpha(), (100, 100))
    background_image = pygame.transform.scale(pygame.image.load("back.jpg").convert(), (WIDTH, HEIGHT))
    background_slow = pygame.transform.scale(pygame.image.load("back_slow.png").convert(), (WIDTH, HEIGHT))  # Fondo para modo lento
    background_speed = pygame.transform.scale(pygame.image.load("back_speed.png").convert(), (WIDTH, HEIGHT))
    return hole, hole_slow, insect, background_image, background_slow, hole_speed, background_speed


# ITEMS
def update_pink_items():
    spawn_pink_item()
    pink_items.update()  # Actualiza el estado de los PinkItem
    pink_items.draw(window)  # Dibuja los PinkItem en la ventana
    
def spawn_pink_item():
    global pink_item, items_mostrados, spawn_timer, item_spawn_time
    if spawn_timer >= item_spawn_time and items_mostrados==0:
        pink_item = PinkItem()
        random_hole = random.choice(agujeros.sprites())
        pink_item.rect.center = random_hole.rect.center
        spawn_timer = 0
        pink_item.active = True
        item_spawn_time = random.randint(1000, 8000)
        pink_item.spawn_time = pygame.time.get_ticks()
        pink_items.add(pink_item)
        items_mostrados += 1

def enter_slow_motion_mode():
    global in_slow_motion_mode, hole, a

    in_slow_motion_mode = True
    hole = hole_slow  # Cambiar el agujero al modo lento
    if a<1:
        pygame.mixer.music.load("baile_slow.mp3")  
        pygame.mixer.music.play(-1) 
    a+=1    

def update_speed_items():
    spawn_speed_item()
    speed_items.update()
    speed_items.draw(window)       
  
def spawn_speed_item():
    global speed_item, items_shown, spawn_timer, speed_spawn_time
    if spawn_timer >= speed_spawn_time and items_shown == 0:
        speed_item = SpeedItem()
        random_hole = random.choice(agujeros.sprites())
        speed_item.rect.center = random_hole.rect.center
        spawn_timer = 0
        speed_item.active = True
        speed_spawn_time = random.randint(1000, 8000)
        speed_item.spawn_time = pygame.time.get_ticks()
        speed_items.add(speed_item)
        items_shown += 1

def enter_speed_mode():
    global in_speed_mode, hole, b
    in_speed_mode = True
    hole = hole_speed
    if b<1:
        pygame.mixer.music.load("baile_speed.mp3")  
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
    pygame.mixer.music.load("baile.ogg")
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


# Handle 
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for cucaracha in cucarachas:
                if cucaracha.active and cucaracha.rect.collidepoint(event.pos):
                    handle_cucaracha_click(cucaracha)
            for pink_item in pink_items:
                if pink_item.active and pink_item.rect.collidepoint(event.pos):
                    handle_slow_item_click(pink_item)
            for speed_item in speed_items:
                if speed_item.active and speed_item.rect.collidepoint(event.pos):
                    handle_speed_item_click(speed_item)        

    return True

def handle_slow_item_click(item):
    global in_slow_motion_mode
    item.kill()  # Eliminar el item del grupo de sprites
    item.active = False  # Desactivar el item
    in_slow_motion_mode = True  # Entrar en slowmode

def handle_speed_item_click(item):
    global in_speed_mode
    item.kill()  # Eliminar el item del grupo de sprites
    item.active = False  # Desactivar el item
    in_speed_mode = True  # Entrar en slowmode    

def handle_cucaracha_click(cucaracha):
    global score
    score += 1
    cucaracha.active = False
    cucaracha.kill()
    cell_center = (cucaracha.rect.centerx // CELL_SIZE * CELL_SIZE + CELL_SIZE // 2,
                   cucaracha.rect.centery // CELL_SIZE * CELL_SIZE + CELL_SIZE // 2)
    window.blit(insect, (cell_center[0] - insect.get_width() // 2,
                            cell_center[1] - insect.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(300)

# CUCARACHA  
def update_cucarachas():
    spawn_cucaracha()
    cucarachas.update()
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

def draw_gif_animation():
    window.blit(gif_surfaces[int(gif_frame_index)], gif_position)
    update_gif_frame_index()

def update_gif_frame_index():
    global gif_frame_index
    gif_frame_index = (gif_frame_index + gif_animation_speed) % len(gif_surfaces)


#FINAL SCORE
def show_final_score_screen():
    draw_final_score_screen()
    while True:
        if not handle_final_score_events():
            break

def draw_final_score_screen():
    global background 
    background = background_image
    pygame.mixer.music.load("end.wav")
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


# Main game loop
def main():
    global running, score, in_slow_motion_mode, in_speed_mode, background_image, background 
    running = True
    score = 0
    in_slow_motion_mode = False
    in_speed_mode = False
    time_in_slow_motion = 0 
    time_in_speed_mode = 0
    

    while running:
        
        draw_background()
        draw_holes()
        if not handle_events():
            break
        
        update_pink_items()
        update_cucarachas()
        update_speed_items()
        if in_slow_motion_mode:
            enter_slow_motion_mode()   
            time_in_slow_motion += clock.get_time() / 1000  # Convertir el tiempo en milisegundos a segundos
            # Si ha pasado más de 10 segundos, salir del modo lento
            if time_in_slow_motion > 12:
                in_slow_motion_mode = False
                pygame.mixer.music.load("baile.ogg")  # Restaurar la música normal
                pygame.mixer.music.play(-1)  # Reproducir la música normal en bucle
                
        elif in_speed_mode:
            enter_speed_mode()
            time_in_speed_mode += clock.get_time() / 1000
            if time_in_speed_mode > 10:  
                in_speed_mode = False
                pygame.mixer.music.load("baile.ogg")  # Restaurar la música normal
                pygame.mixer.music.play(-1)  # Reproducir la música normal en bucle
                

        if cucarachas_mostradas > 15:  # Salir del juego cuando se alcanzan 10 cucarachas
            running = False 
           
        draw_gif_animation()
        pygame.display.flip()
    
        clock.tick(60)
    show_final_score_screen()

if __name__ == "__main__":
    global a, b    
    a=0
    b=0
    WIDTH, HEIGHT = 800, 600
    CELL_SIZE = 200
    ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
    window, clock = initialize_pygame()
    hole, hole_slow, insect, background_image, background_slow, hole_speed, background_speed= load_images()
    agujeros = create_holes()

    cucarachas = pygame.sprite.Group()
    pink_items = pygame.sprite.Group()
    speed_items = pygame.sprite.Group()

    #Gift
    gif_path = "baile.gif"
    gif_clip = VideoFileClip(gif_path)
    gif_frames = [np.rot90(np.array(frame) * 255) for frame in gif_clip.iter_frames()]
    gif_surfaces = [pygame.surfarray.make_surface(frame) for frame in gif_frames]
    gif_surfaces = [pygame.transform.scale(surface, (40, 40)) for surface in gif_surfaces]
    gif_position = [760, 560]
    gif_frame_index = 0
    gif_animation_speed = 0.18

    spawn_timer = 0
    next_spawn_time = random.randint(500, 5000)
    item_spawn_time = random.randint(1000, 8000)
    speed_spawn_time = random.randint(1000, 6000)

    cucarachas_mostradas = 0
    items_mostrados = 0
    items_shown = 0

    play_music()
    score = 0
    show_final_score = False
    font = pygame.font.Font(None, 36)
    button_width = 300
    button_height = 50
    button_color = (140, 83, 11)
    marco = (0, 0, 0)
    main()
    
    pygame.quit()
    sys.exit()
