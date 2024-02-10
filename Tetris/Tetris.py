import pygame
import random
import time

# Inicializar Pygame
pygame.init()

# Definir las variables globales
WINDOW_WIDTH = 800  # Ancho de la ventana general
WINDOW_HEIGHT = 800  # Alto de la ventana general
BOARD_WIDTH = 200  # Ancho del tablero del juego
BOARD_HEIGHT = 500  # Alto del tablero del juego
BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2  # Desplazamiento X para centrar el tablero
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED_LIGHT = (255, 128, 128)
FONT_SIZE = 24
SCORE_FONT_SIZE = 18
TIMER_FONT_SIZE = 24

# Definir la forma de los bloques de Tetris y sus colores
tetrominoes = [
    [[[0, 2, 2],
      [2, 2, 0]],  # Tetromino "S"
     (0, 0, 255)],  # Color Azul

    [[[3, 3, 0],
      [0, 3, 3]],  # Tetromino "Z"
     (255, 165, 0)],  # Color Naranja

    [[[4, 4, 4],
      [0, 4, 0]],  # Tetromino "T"
     (128, 0, 128)],  # Color Morado

    [[[0, 0, 5],
      [5, 5, 5]],  # Tetromino "L"
     (0, 255, 0)],  # Color Verde

    [[[6, 6],
      [6, 6]],  # Tetromino "O"
     (255, 255, 0)],  # Color Amarillo

    [[[7, 7, 7, 7]],  # Tetromino "I"
     (255, 0, 0)]  # Color Rojo
]

# Clase para representar el bloque de Tetris
class Tetromino:
    def __init__(self):
        self.x = random.randint(2, BOARD_WIDTH // BLOCK_SIZE - 4) * BLOCK_SIZE + BOARD_OFFSET_X  # Limitar la posición inicial
        self.y = 0
        self.shape, self.color = random.choice(tetrominoes)
        self.falling = True
    
    def draw(self, surface):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    pygame.draw.rect(surface, self.color, (self.x + j * BLOCK_SIZE, self.y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(surface, BLACK, (self.x + j * BLOCK_SIZE, self.y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def move_down(self):
        self.y += BLOCK_SIZE
    
    def move_left(self, board):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    if self.x + j * BLOCK_SIZE <= BOARD_OFFSET_X or (self.x + j * BLOCK_SIZE) // BLOCK_SIZE - 1 >= 0 and board[self.y // BLOCK_SIZE + i][(self.x + j * BLOCK_SIZE - BOARD_OFFSET_X) // BLOCK_SIZE - 1]:
                        return
        self.x -= BLOCK_SIZE

    def move_right(self, board):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    if (self.x + j * BLOCK_SIZE >= BOARD_WIDTH + BOARD_OFFSET_X - BLOCK_SIZE or
                        (self.x + j * BLOCK_SIZE - BOARD_OFFSET_X) // BLOCK_SIZE + 1 < len(board[0]) and board[self.y // BLOCK_SIZE + i][(self.x + j * BLOCK_SIZE - BOARD_OFFSET_X) // BLOCK_SIZE + 1]):
                        return
        self.x += BLOCK_SIZE
    
    def collide(self, board):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    if (self.y + i * BLOCK_SIZE >= BOARD_HEIGHT - BLOCK_SIZE or
                        (self.y // BLOCK_SIZE + i + 1 < len(board) and self.x // BLOCK_SIZE + j - BOARD_OFFSET_X // BLOCK_SIZE < len(board[0]) and board[self.y // BLOCK_SIZE + i + 1][(self.x - BOARD_OFFSET_X + j * BLOCK_SIZE) // BLOCK_SIZE])):
                        self.falling = False
                        return True
        return False

    def can_rotate(self, board):
        current_shape = [row[:] for row in self.shape]
        rotated_shape = [[current_shape[j][i] for j in range(len(current_shape))] for i in range(len(current_shape[0]))]
        rotated_shape.reverse()
        for i in range(len(rotated_shape)):
            for j in range(len(rotated_shape[i])):
                if rotated_shape[i][j]:
                    if (self.y + i * BLOCK_SIZE >= BOARD_HEIGHT or self.x + j * BLOCK_SIZE < BOARD_OFFSET_X or
                        self.x + j * BLOCK_SIZE >= BOARD_WIDTH + BOARD_OFFSET_X or board[self.y // BLOCK_SIZE + i][(self.x - BOARD_OFFSET_X + j * BLOCK_SIZE) // BLOCK_SIZE]):
                        return False
        return True

    def rotate(self, board):
        if self.can_rotate(board):
            current_shape = [row[:] for row in self.shape]
            self.shape = [[current_shape[j][i] for j in range(len(current_shape))] for i in range(len(current_shape[0]))]
            self.shape.reverse()

# Función principal del juego
def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, FONT_SIZE)
    score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
    timer_font = pygame.font.Font(None, TIMER_FONT_SIZE)

    game_over = False

    # Inicializar el tablero
    board = [[None] * (BOARD_WIDTH // BLOCK_SIZE) for _ in range(BOARD_HEIGHT // BLOCK_SIZE)]

    # Lista de tetrominos activos
    tetrominos = [Tetromino()]

    start_time = time.time()
    increase_speed_interval = 5  # Aumentar la velocidad cada 5 segundos
    speed_increase_factor = 0  # Factor de aumento de velocidad

    # Contadores
    score = 0
    countdown_timer = 30

    running = True
    while running:
        screen.fill(GRAY)  # Color de fondo de la ventana

        # Dibujar área del tablero
        pygame.draw.rect(screen, WHITE, (BOARD_OFFSET_X, 0, BOARD_WIDTH, BOARD_HEIGHT))

        # Dibujar línea que delimita el tablero del juego
        pygame.draw.line(screen, BLACK, (BOARD_OFFSET_X, 0), (BOARD_OFFSET_X, BOARD_HEIGHT), 2)
        pygame.draw.line(screen, BLACK, (BOARD_OFFSET_X + BOARD_WIDTH, 0), (BOARD_OFFSET_X + BOARD_WIDTH, BOARD_HEIGHT), 2)

        # Obtener el tiempo actual en segundos
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1:  # Restar una unidad cada segundo
            countdown_timer = max(countdown_timer - 1, 0)
            start_time = time.time()  # Reiniciar el tiempo de inicio

        # Dibujar el contador de tiempo
        timer_text = timer_font.render(f"Tiempo: {countdown_timer}", True, BLACK)
        screen.blit(timer_text, (10, 10))

        # Dibujar el contador de puntuación
        score_text = score_font.render(f"Puntuación: {score}", True, BLACK)
        screen.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 10, 10))

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        # Mover el tetromino hacia la izquierda
                        tetrominos[-1].move_left(board)
                    elif event.key == pygame.K_RIGHT:
                        # Mover el tetromino hacia la derecha
                        tetrominos[-1].move_right(board)
                    elif event.key == pygame.K_SPACE:
                        # Rotar el tetromino
                        tetrominos[-1].rotate(board)
                    elif event.key == pygame.K_DOWN:
                        # Mover la pieza hacia abajo rápidamente
                        while not tetrominos[-1].collide(board):
                            tetrominos[-1].move_down()

        if not game_over:
            # Obtener el tetromino actual
            current_tetromino = tetrominos[-1]

            # Mover el tetromino hacia abajo
            if current_tetromino.falling:
                current_tetromino.move_down()

            # Verificar colisión
            if current_tetromino.collide(board):
                # Agregar el tetromino actual al tablero
                for i in range(len(current_tetromino.shape)):
                    for j in range(len(current_tetromino.shape[i])):
                        if current_tetromino.shape[i][j]:
                            board[current_tetromino.y // BLOCK_SIZE + i][(current_tetromino.x - BOARD_OFFSET_X) // BLOCK_SIZE + j] = current_tetromino.color

                # Eliminar filas completas y reorganizar las filas restantes
                rows_to_delete = set()
                for i in range(len(board)):
                    if all(board[i]):
                        rows_to_delete.add(i)
                        score += 100  # Sumar puntos por cada fila eliminada

                for row in rows_to_delete:
                    del board[row]
                    board.insert(0, [None] * (BOARD_WIDTH // BLOCK_SIZE))

                # Crear un nuevo tetromino si no hay filas completas
                if not rows_to_delete:
                    tetrominos.append(Tetromino())

                # Verificar si el juego ha terminado
                if any(board[1]):  # Si hay algún bloque en la segunda fila del tablero
                    game_over = True

                # Mostrar "GAME OVER" con un fondo verde si el tiempo se agota
                if countdown_timer == 0:
                    game_over = True

        # Dibujar el tablero
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j]:
                    pygame.draw.rect(screen, board[i][j], (j * BLOCK_SIZE + BOARD_OFFSET_X, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Dibujar el tetromino actual
        current_tetromino.draw(screen)

        # Mostrar "GAME OVER" si el juego ha terminado
        if game_over:
            game_over_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            if countdown_timer == 0:
                game_over_surface.fill((0, 255, 0, 128))  # Fondo verde
            else:
                game_over_surface.fill(RED_LIGHT + (128,))  # Fondo rojo
            screen.blit(game_over_surface, (0, 0))
            game_over_text = font.render("GAME OVER", True, BLACK)
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - FONT_SIZE))
            screen.blit(game_over_text, game_over_rect)

        pygame.display.flip()
        clock.tick(5)  # Velocidad de caída de los bloques inicial

    pygame.quit()

if __name__ == "__main__":
    main()
