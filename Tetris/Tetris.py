import pygame
import random
import time
from block import Block

pygame.init()

# Dimensións ventá 
WINDOW_WIDTH = 800  
WINDOW_HEIGHT = 800  

# Dimensións tableiro 
BOARD_WIDTH = 200 
BOARD_HEIGHT = 500 

BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2 
BLOCK_SIZE = 20

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED_LIGHT = (255, 128, 128)
FONT_SIZE = 24

# Cargar imagen de fondo  
background_image = pygame.image.load('assets/background.jpeg')

# Música
pygame.mixer.music.load('assets/music/tetris_song.ogg')
pygame.mixer.music.play(-1)  

# Efectos de sonido
clear_row_sound = pygame.mixer.Sound('assets/music/line.wav')
piece_drop_sound = pygame.mixer.Sound('assets/music/drop.mp3')
win_sound = pygame.mixer.Sound('assets/music/win.mp3')
lose_sound = pygame.mixer.Sound('assets/music/lose.mp3')



def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, FONT_SIZE)
    score_font = pygame.font.Font(None, FONT_SIZE)
    timer_font = pygame.font.Font(None, FONT_SIZE)

    start_time = time.time()

    game_over = False
    game_over_sound_played = False  
    ended = False

    # Inicializar tableiro
    board = [[None] * (BOARD_WIDTH // BLOCK_SIZE) for _ in range(BOARD_HEIGHT // BLOCK_SIZE)]

    # Lista de bloques activos
    blocks = [Block()]

    # Velocidade
    speed = 5  # Velocidad inicial de caída das pezas
    increase_interval = 5  # Intervalo de tempo no que aumenta a velocidade
    last_increase_time = time.time()  

    # Contadores
    score = 0
    countdown_timer = 60

    running = True
    while running:
        screen.blit(background_image, (0, 0))  

        # Área tableiro
        pygame.draw.rect(screen, WHITE, (BOARD_OFFSET_X, 0, BOARD_WIDTH, BOARD_HEIGHT))

        # Límite tableiro
        pygame.draw.line(screen, BLACK, (BOARD_OFFSET_X, 0), (BOARD_OFFSET_X, BOARD_HEIGHT), 2)
        pygame.draw.line(screen, BLACK, (BOARD_OFFSET_X + BOARD_WIDTH, 0), (BOARD_OFFSET_X + BOARD_WIDTH, BOARD_HEIGHT), 2)

        current_time = time.time()
        elapsed_time = time.time() - start_time

        if current_time >= increase_interval + last_increase_time:
            speed *= 1.125  # Aumentar velocidade
            last_increase_time = current_time  

        clock.tick(speed)  

        if elapsed_time >= 1:  
            if not game_over or countdown_timer > 0:  
                countdown_timer = max(countdown_timer - 1, 0)
                start_time = time.time()  

        # Mostrar tempo restante
        if not game_over or countdown_timer > 0: 
            timer_text = timer_font.render(f"Tiempo: {countdown_timer}", True, BLACK)
            screen.blit(timer_text, (10, 10))

        # Mostrar puntuación
        score_text = score_font.render(f"Puntuación: {score}", True, BLACK)
        screen.blit(score_text, (10, 30))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        # Mover peza á esquerda
                        blocks[-1].move_left(board)
                    elif event.key == pygame.K_RIGHT:
                        # Mover peza á dereita
                        blocks[-1].move_right(board)
                    elif event.key == pygame.K_UP:
                        # Rotar peza 
                        blocks[-1].rotate(board)
                    elif event.key == pygame.K_DOWN:
                        # Baixar peza
                        while not blocks[-1].collide(board):
                            blocks[-1].move_down()

        if not game_over:
            
            current_block = blocks[-1]

            if current_block.falling:
                current_block.move_down()

            # Comprobar colisión
            if current_block.collide(board):
                # Engadimos a peza actual ao tableiro
                for i in range(len(current_block.shape)):
                    for j in range(len(current_block.shape[i])):
                        if current_block.shape[i][j]:
                            board[current_block.y // BLOCK_SIZE + i][(current_block.x - BOARD_OFFSET_X) // BLOCK_SIZE + j] = current_block.color

                # Eliminar as filas que estén completas
                rows_to_delete = set()
                for i in range(len(board)):
                    if all(board[i]):
                        rows_to_delete.add(i)
                        score += 100  

                for row in rows_to_delete:
                    del board[row]
                    board.insert(0, [None] * (BOARD_WIDTH // BLOCK_SIZE))
                    clear_row_sound.play() 

                # Lanzar unha nova peza cando non queden máis liñas por limpar
                if not rows_to_delete:
                    blocks.append(Block())
                    piece_drop_sound.play()

                # Parar o xogo se unha peza chega ao límite superior
                if any(board[1]): 
                    game_over = True

                # Parar o xogo se o tempo chega a 0
                if countdown_timer == 0:
                    game_over = True

        # Debuxar tableiro
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j]:
                    pygame.draw.rect(screen, board[i][j], (j * BLOCK_SIZE + BOARD_OFFSET_X, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Debuxar peza
        current_block.draw(screen)

        # Cargar pantalla de GAME OVER ao rematar o xogo
        if game_over:
            pygame.mixer.music.stop()  

            if not game_over_sound_played:
                game_over_sound_played = True
                if countdown_timer == 0:
                    win_sound.play()  
                else: 
                    lose_sound.play()
                

            game_over_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            if countdown_timer == 0 and not ended:
                game_over_surface.fill((0, 255, 0, 128))  # Fondo verde
            else:
                game_over_surface.fill(RED_LIGHT + (128,))  # Fondo vermello 
                ended = True
            screen.blit(game_over_surface, (0, 0))

            # Ventá emerxente coa mensaxe de GAME OVER e a Puntuación Final
            game_over_surface = pygame.Surface((300, 100), pygame.SRCALPHA)
            game_over_surface.fill(WHITE)  
            game_over_rect = game_over_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

            game_over_text = font.render("GAME OVER", True, BLACK)
            game_over_text_rect = game_over_text.get_rect(center=(150, 30))
            game_over_surface.blit(game_over_text, game_over_text_rect)

            final_score_text = font.render(f"Puntuación Final: {score}", True, BLACK)
            final_score_text_rect = final_score_text.get_rect(center=(150, 70))
            game_over_surface.blit(final_score_text, final_score_text_rect)

            screen.blit(game_over_surface, game_over_rect)

            countdown_timer = 0 # Paramos o tempo

        pygame.display.flip()
        clock.tick(30)  # Velocidade de fotogramas 
    

    pygame.quit()
    return score

if __name__ == "__main__":
    main()
