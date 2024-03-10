import pygame
import sys
from Arcade.arcade import Arcade
from ArcadeMachinePopup.popUpClass import PopUp
from ArcadeMachinePopup.textClass import Text
from ArcadeMachinePopup.buttonClass import Boton
from ResourceManager import ResourceManager


# Inicializar Pygame
pygame.init()

# VARIABLES GLOBALES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (12, 18, 58)
YELLOW = (249, 247, 98 )
YELLOW_PILES = (222, 196, 65)
BROWN_CUCA = (171, 109, 0)
TRANSPARENT = (0, 0, 0, 50)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
LIMIT_DOWN_Y = 150 # Límite superior de movimiento para que no se mueva por la pared

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Arcade's Room")

resource_manager = ResourceManager()
# Cargar fuentes
fuenteGP = "ArcadeMachinePopup/fuentes/game_power.ttf"
fuente8Bit = "ArcadeMachinePopup/fuentes/8Bit.ttf"

# Cargar sonidos para ventana emergente
popup_sound_open = pygame.mixer.Sound('Arcade/assets/music/open.mp3')
popup_sound_close = pygame.mixer.Sound('Arcade/assets/music/close.mp3')

# Cargar imágenes del muñeco y fondo
player_up_image1 = pygame.transform.scale(resource_manager.arcade_player_up_image1.get(), (75, 75))
player_down_image1 = pygame.transform.scale(resource_manager.arcade_player_down_image1.get(), (75, 75))
player_left_image1 = pygame.transform.scale(resource_manager.arcade_player_left_image1.get(), (75, 75))
player_right_image1 = pygame.transform.scale(resource_manager.arcade_player_right_image1.get(), (75, 75))

player_up_image2 = pygame.transform.scale(resource_manager.arcade_player_up_image2.get(), (75, 75))
player_down_image2 = pygame.transform.scale(resource_manager.arcade_player_down_image2.get(), (75, 75))
player_left_image2 = pygame.transform.scale(resource_manager.arcade_player_left_image2.get(), (75, 75))
player_right_image2 = pygame.transform.scale(resource_manager.arcade_player_right_image2.get(), (75, 75))

background_image = pygame.transform.scale(pygame.image.load('Arcade/assets/arcade_background.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))

instructions_piles = pygame.transform.scale(resource_manager.pile_instructions.get(), (700, 762))
instructions_cuca = pygame.transform.scale(resource_manager.cuca_instructions.get(), (700, 775))
instructions_tetris = pygame.transform.scale(resource_manager.cuca_instructions.get(), (700, 774))

arcades_positions = [
    (100, 150), 
    (350, 150),  
    (590, 150)   
]

arcades = []  # Usaremos una lista en lugar de un grupo
for i, (center_x, center_y) in enumerate(arcades_positions):
    arcade = Arcade(center_x, center_y, i)
    arcades.append(arcade)

# VARIABLES DEL MUÑECO
player_rect = player_up_image1.get_rect() # Rectángulo que lo delimita
player_speed = 5
initial_player_position = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
# Variables para almacenar las imágenes actuales del muleco y el estado de dirección
current_player_image = player_up_image1
up_direction_state = False
down_direction_state = False
left_direction_state = False
right_direction_state = False


# VARIABLES DE LA ANIMACIÓN
frame_counter = 0
animation_speed = 10


# VARIABLES DE LOS POPUPS
popup_shown = {}
popup_showing = False
instructions_showing = False


### FUNCIONES ###

def fade_transition():
    fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 10):
        fade_surface.set_alpha(alpha)
        window.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(60)

def handle_events():
    global left_direction_state, right_direction_state, up_direction_state, down_direction_state, current_player_image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_direction_state = True
                current_player_image = player_left_image1
            elif event.key == pygame.K_RIGHT:
                right_direction_state = True
                current_player_image = player_right_image1
            elif event.key == pygame.K_UP:
                up_direction_state = True
                current_player_image = player_up_image1
            elif event.key == pygame.K_DOWN:
                down_direction_state = True
                current_player_image = player_down_image1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_direction_state = False
            elif event.key == pygame.K_RIGHT:
                right_direction_state = False
            elif event.key == pygame.K_UP:
                up_direction_state = False
            elif event.key == pygame.K_DOWN:
                down_direction_state = False



def update_player_position():
    global current_player_image, player_rect, frame_counter

    if left_direction_state:
        player_rect.x -= player_speed
        if frame_counter % animation_speed == 0:
            current_player_image = player_left_image2 if current_player_image == player_left_image1 else player_left_image1
    elif right_direction_state:
        player_rect.x += player_speed
        if frame_counter % animation_speed == 0:
            current_player_image = player_right_image2 if current_player_image == player_right_image1 else player_right_image1
    elif up_direction_state:
        player_rect.y -= player_speed
        if frame_counter % animation_speed == 0:
            current_player_image = player_up_image2 if current_player_image == player_up_image1 else player_up_image1
    elif down_direction_state:
        player_rect.y += player_speed
        if frame_counter % animation_speed == 0:
            current_player_image = player_down_image2 if current_player_image == player_down_image1 else player_down_image1

    top_limit = 150 
    if player_rect.top < top_limit:
        player_rect.top = top_limit

    # Verificar si hay colisión con algún cuadrado
    for arcade in arcades:
        if player_rect.colliderect(arcade.rect):
            return

    # Limitar al jugador dentro de los límites de la ventana
    player_rect.x = max(0, min(WINDOW_WIDTH - player_rect.width, player_rect.x))
    player_rect.y = max(0, min(WINDOW_HEIGHT - player_rect.height, player_rect.y))



def check_collisions():
    for arcade in arcades:
        if (player_rect.colliderect(arcade.rect) and not popup_shown[arcade] and arcade.active):
            exit = show_popup(arcade.number)
            if exit:
                return arcade.number
            popup_shown[arcade] = True
        elif not player_rect.colliderect(arcade.rect):
            popup_shown[arcade] = False
    


def draw_out_of_service(arcade):
    inactive_image = pygame.transform.scale(pygame.image.load('Arcade/out.png'), (110, 70)) 
    image_x = arcade.rect.centerx - inactive_image.get_width() // 2
    image_y = arcade.rect.centery - inactive_image.get_height() * 1.7
    window.blit(inactive_image, (image_x, image_y))



def draw():
    window.fill(BLACK)  
    window.blit(background_image, (0, 0)) 
    
    # Cartel de fuera de servicio
    for arcade in arcades:
        window.blit(arcade.image, arcade.rect)
        if not arcade.active:
            draw_out_of_service(arcade)  
    
    # Muñeco
    window.blit(current_player_image, player_rect)
    
     # Actualizar la pantalla



def show_popup(arcade_number):
    global player_rect, up_direction_state, down_direction_state, left_direction_state, right_direction_state

    popup_showing = True
    instructions_showing = False

    # Con esta variables evitamos que el jugador ande automaticamente tras cerrar un popup
    up_direction_state = False
    down_direction_state = False
    left_direction_state = False
    right_direction_state = False

    popup_sound_open.play()
    player_position_before_popup = player_rect.topleft

    rotations = [0, 30]

    minigame_text = [
        Text("Minigame", 20, YELLOW, WINDOW_WIDTH//2 + 180, WINDOW_HEIGHT//3 + 90, True, fuente8Bit)
    ]

    buttons = [
        Boton(WINDOW_WIDTH//2, WINDOW_HEIGHT//3 - 40, 100, 40, "JUGAR", fuenteGP, TRANSPARENT, YELLOW, 40, "JUGAR"),
        Boton(WINDOW_WIDTH//2, WINDOW_HEIGHT//3 + 10, 100, 40, "VOLVER", fuenteGP, TRANSPARENT, YELLOW, 40, "VOLVER"),
        Boton(WINDOW_WIDTH//2, WINDOW_HEIGHT//3 + 60, 100, 40, "INSTRUCCIONES", fuenteGP, TRANSPARENT, YELLOW, 40, "INSTRUCCIONES")
    ]
    # Nombre de cada minijuego
    if arcade_number == 0:
        arcade_text = [
            Text("Cucarachas", 60, YELLOW, WINDOW_WIDTH//2 , WINDOW_HEIGHT//3 - 140, True, fuenteGP)
        ] + minigame_text

        popup = PopUp(WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//3 - 250, 500, 400, 60, BROWN_CUCA, 8, BLACK, buttons, arcade_text, rotations)
    elif arcade_number == 1:
        arcade_text = [
            Text("Garbage Piles", 60, BLACK, WINDOW_WIDTH//2 , WINDOW_HEIGHT//3 - 140, True, fuenteGP)
        ] + minigame_text

        buttons = [
            Boton(WINDOW_WIDTH//2, WINDOW_HEIGHT//3 - 40, 100, 40, "JUGAR", fuenteGP, TRANSPARENT, BLACK, 40, "JUGAR"),
            Boton(WINDOW_WIDTH//2, WINDOW_HEIGHT//3 + 10, 100, 40, "VOLVER", fuenteGP, TRANSPARENT, BLACK, 40, "VOLVER"),
            Boton(WINDOW_WIDTH//2, WINDOW_HEIGHT//3 + 60, 100, 40, "INSTRUCCIONES", fuenteGP, TRANSPARENT, BLACK, 40, "INSTRUCCIONES")
        ]

        popup = PopUp(WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//3 - 250, 500, 400, 60, YELLOW_PILES, 8, BLACK, buttons, arcade_text, rotations)

    elif arcade_number == 2:
        arcade_text = [
            Text("Tetris", 60, YELLOW, WINDOW_WIDTH//2 , WINDOW_HEIGHT//3 - 140, True, fuenteGP)
        ] + minigame_text

        popup = PopUp(WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//3 - 250, 500, 400, 60, BLUE, 8, BLACK, buttons, arcade_text, rotations)

    while popup_showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if popup.get_rect().collidepoint(event.pos):
                    for boton in popup.botones:
                        if boton.rect.collidepoint(event.pos):

                            if boton.accion == "VOLVER":
                                popup_showing = False
                                popup_sound_close.play()
                                player_rect.topleft = player_position_before_popup

                            elif boton.accion == "JUGAR":
                                popup_showing = False
                                arcade.exit = True
                                fade_transition()
                                return arcade.exit
                            
                            elif boton.accion == "INSTRUCCIONES":
                                instructions_showing = True
        
        while instructions_showing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if window.get_rect().collidepoint(event.pos):
                        instructions_showing = False

            #show instructions
            if arcade_number == 0:
                #CUCA
                window.blit(instructions_cuca, ((WINDOW_WIDTH - instructions_cuca.get_width())//2, (WINDOW_HEIGHT - instructions_cuca.get_height())//2 - 49))
            elif arcade_number == 1:
                #PILES
                window.blit(instructions_piles, ((WINDOW_WIDTH - instructions_piles.get_width())//2, (WINDOW_HEIGHT - instructions_piles.get_height())//2 - 35))
            elif arcade_number == 2:
                #TETRIS
                window.blit(instructions_tetris, ((WINDOW_WIDTH - instructions_tetris.get_width())//2, (WINDOW_HEIGHT - instructions_tetris.get_height())//2 - 48))    

            pygame.display.flip() 
            pygame.time.Clock().tick(60)      
        draw()
        popup.draw(window) 
        pygame.display.flip()
        pygame.time.Clock().tick(60)



def main(arcade_popup_flags):
    print(arcade_popup_flags)
    global frame_counter
    pygame.mixer.music.load('Arcade/assets/music/happy.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    player_rect.center = initial_player_position

    for i, arcade in enumerate(arcades):
        arcade.active = arcade_popup_flags[i]

    popup_shown = {arcade: False for arcade in arcades}

    
    while True:
        handle_events()
        update_player_position()
        num = check_collisions()
        draw()
        pygame.display.flip() 
        pygame.time.Clock().tick(60)
        frame_counter += 1
        
        if num is not None:
            arcade_popup_flags[num] = False
            # AQUI SIGUEN SENDO TRES ELEMENTOS
            return arcade_popup_flags, num
                
                    
