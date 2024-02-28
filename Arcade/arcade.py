import pygame
import sys
from Square import Square
from Plantilla_Inicio.popUpClass import PopUp
from Plantilla_Inicio.textClass import Text
from Plantilla_Inicio.buttonClass import Boton


# JAVI
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (12, 18, 58)
AMARILLO = (249, 247, 98 )
TRANSPARENTE = (0, 0, 0, 50)
#AZUL_OSCURO = (71, 21, 136)

# Definir dimensiones de la pantalla
ANCHO = 800
ALTO = 800

fuenteGP = "/Users/clara/Documents/GitHub/CIIE/Arcade/Plantilla_Inicio/fuentes/game_power.ttf"
fuente8Bit = "/Users/clara/Documents/GitHub/CIIE/Arcade/Plantilla_Inicio/fuentes/8Bit.ttf"

# JAVI


# Inicializar Pygame
pygame.init()

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Definir dimensiones de la ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

LIMIT_DOWN_Y = 150

# Crear la ventana
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Arcade')

# Cargar música de fondo
pygame.mixer.music.load('happy.mp3')
pygame.mixer.music.set_volume(0.0)
pygame.mixer.music.play(-1)

# Cargar sonidos para ventana emergente
popup_sound_open = pygame.mixer.Sound('open.mp3')
popup_sound_close = pygame.mixer.Sound('close.mp3')

# Cargar imágenes del muñeco para cada dirección de movimiento y redimensionarlas
player_up_image1 = pygame.transform.scale(pygame.image.load('player/up1.png'), (75, 75))
player_down_image1 = pygame.transform.scale(pygame.image.load('player/down1.png'), (75, 75))
player_left_image1 = pygame.transform.scale(pygame.image.load('player/left1.png'), (75, 75))
player_right_image1 = pygame.transform.scale(pygame.image.load('player/right1.png'), (75, 75))

player_up_image2 = pygame.transform.scale(pygame.image.load('player/up2.png'), (75, 75))
player_down_image2 = pygame.transform.scale(pygame.image.load('player/down2.png'), (75, 75))
player_left_image2 = pygame.transform.scale(pygame.image.load('player/left2.png'), (75, 75))
player_right_image2 = pygame.transform.scale(pygame.image.load('player/right2.png'), (75, 75))

# Crear los cuadrados en posiciones personalizadas
squares_positions = [
    (100, 150),  # posición del primer cuadrado
    (350, 150),  # posición del segundo cuadrado
    (590, 150)   # posición del tercer cuadrado
]

squares_group = pygame.sprite.Group()
for i, (center_x, center_y) in enumerate(squares_positions):
    square = Square(center_x, center_y, i + 1)
    squares_group.add(square)

# Obtener el rectángulo del jugador (posición y tamaño)
player_rect = player_up_image1.get_rect()

# Definir velocidad del jugador
player_speed = 5

# Definir la posición inicial del jugador
player_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

# Variables para almacenar las imágenes actuales del jugador y el estado de dirección
current_player_image = player_up_image1
up_direction_state = False
down_direction_state = False
left_direction_state = False
right_direction_state = False

# Variables para controlar la animación
frame_counter = 0
animation_speed = 10

# Diccionario para controlar si la ventana emergente de un cuadrado ha sido mostrada
popup_shown = {square: False for square in squares_group}

# Variable para controlar si se está mostrando una ventana emergente
popup_showing = False

# Cargar la imagen de fondo y ajustar su tamaño
background_image = pygame.transform.scale(pygame.image.load('arcade_background.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))

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

    # Verificar si la nueva posición del jugador excede el límite superior
    top_limit = 150 
    if player_rect.top < top_limit:
        player_rect.top = top_limit

    # Verificar si hay colisión con algún cuadrado
    for square in squares_group:
        if player_rect.colliderect(square.rect):
            return  # Si hay colisión, no actualizar la posición del jugador

    # Si no hay colisión, actualizar la posición del jugador
    player_rect = player_rect

    # Limitar al jugador dentro de los límites de la ventana
    player_rect.x = max(0, min(WINDOW_WIDTH - player_rect.width, player_rect.x))
    player_rect.y = max(0, min(WINDOW_HEIGHT - player_rect.height, player_rect.y))

def check_collisions():
    global popup_showing

    for square in squares_group:
        # Definir la distancia vertical mínima entre el centro del jugador y el borde inferior del cuadrado
        distance_threshold = 5

        # Verificar si el centro del jugador está un poco por debajo del borde inferior del cuadrado
        if (player_rect.colliderect(square.rect) and
                square.rect.top - player_rect.center[1] <= distance_threshold and
                not popup_shown[square] and square.active):
            exit = show_popup(square.number)
            if exit:
                return square.number
            popup_shown[square] = True
        elif not player_rect.colliderect(square.rect):
            popup_shown[square] = False
    


def draw_out_image(square):
    # Dibujar la imagen "out.png" sobre el cuadrado inactivo
    inactive_image = pygame.transform.scale(pygame.image.load('out.png'), (110, 70)) 
    # Calcular la posición de la imagen en relación con el centro del cuadrado inactivo
    image_x = square.rect.centerx - inactive_image.get_width() // 2
    image_y = square.rect.centery - inactive_image.get_height() * 1.7
    window.blit(inactive_image, (image_x, image_y))

def draw():
    window.fill(BLACK)  # Limpiar la ventana con color negro
    window.blit(background_image, (0, 0))  # Dibujar la imagen de fondo
    
    # Dibujar cuadrados activos y mostrar ventanas emergentes
    for square in squares_group:
        window.blit(square.image, square.rect)
        if not square.active:
            draw_out_image(square)  # Llamar a la función para dibujar la imagen "out.png"
    
    # Dibujar al jugador
    window.blit(current_player_image, player_rect)
    
    pygame.display.flip()  # Actualizar la pantalla





def show_popup(arcade_number):
    global popup_showing, player_rect, up_direction_state, down_direction_state, left_direction_state, right_direction_state

    popup_showing = True
    up_direction_state = False
    down_direction_state = False
    left_direction_state = False
    right_direction_state = False

    # Reproducir sonido de ventana emergente abierta
    popup_sound_open.play()

    # Almacenar la posición del jugador antes de mostrar la ventana
    player_position_before_popup = player_rect.topleft

    # Definir el segundo texto común para todos los cuadrados
    textos_minigame = [
        Text("Minigame", 20, AMARILLO, ANCHO//2 + 120, ALTO//3 + 50, True, fuente8Bit)
    ]

    # Determinar el texto del primer cuadrado según el número del cuadrado
    if arcade_number == 1:
        textos = [
            Text("Cucarachas", 60, AMARILLO, ANCHO//2 - 200 + 400//2, ALTO//3 - 200 + 300//5, True, fuenteGP)
        ] + textos_minigame
    elif arcade_number == 2:
        textos = [
            Text("Wordle", 60, AMARILLO, ANCHO//2 - 200 + 400//2, ALTO//3 - 200 + 300//5, True, fuenteGP)
        ] + textos_minigame
    elif arcade_number == 3:
        textos = [
            Text("Tetris", 60, AMARILLO, ANCHO//2 - 200 + 400//2, ALTO//3 - 200 + 300//5, True, fuenteGP)
        ] + textos_minigame

    rotaciones = [0, 30]

    botones = [
        Boton(ANCHO//2 - 200 + 400//2, ALTO//3 - 40, 100, 40, "JUGAR", fuenteGP, TRANSPARENTE, AMARILLO, 40, "JUGAR"),
        Boton(ANCHO//2 - 200 + 400//2, ALTO//3 + 30, 100, 40, "VOLVER", fuenteGP, TRANSPARENTE, AMARILLO, 40, "VOLVER")
    ]

    # Crear una instancia de PopUp con el texto proporcionado
    popup = PopUp(ANCHO//2-200, ALTO//3-200, 400, 300, 60, AZUL, 8, NEGRO, botones, textos, rotaciones)

    while popup_showing:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if popup.get_rect().collidepoint(event.pos):
                    for boton in popup.botones:
                        if boton.rect.collidepoint(event.pos):
                            if boton.accion == "VOLVER":
                                popup_showing = False
                                # Reproducir sonido de ventana emergente cerrada
                                popup_sound_close.play()
                                # Restaurar la posición del jugador después de cerrar la ventana
                                player_rect.topleft = player_position_before_popup
                            elif boton.accion == "JUGAR":
                                popup_showing = False
                                square.exit = True
                                return square.exit

        window.fill(BLACK)  # Limpiar la ventana con color negro
        window.blit(background_image, (0, 0))  # Dibujar la imagen de fondo
        for square in squares_group:
            window.blit(square.image, square.rect)
        window.blit(current_player_image, player_position_before_popup) 
        draw_out_image(square)
        popup.draw(window)  # Dibujar la ventana emergente
        pygame.display.flip()
        pygame.time.Clock().tick(60)





def main(square_popup_flags):
    global frame_counter

    for i, square in enumerate(squares_group):
        square.active = square_popup_flags[i]

    try:
        while True:
            handle_events()
            update_player_position()
            num = check_collisions()
            draw()

            # Controlar la velocidad de actualización
            pygame.time.Clock().tick(60)

            # Incrementar el contador de fotogramas
            frame_counter += 1

            for square in squares_group:
                if square.exit:
                    pygame.quit()  
                    sys.exit()

    except SystemExit:
        return num




if __name__ == "__main__":
    main()
