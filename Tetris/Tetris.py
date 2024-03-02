import pygame
import random
import time
from block import Block
from TetrisPopUp.popUpClass import PopUp
from TetrisPopUp.textClass import Text
from TetrisPopUp.buttonClass import Boton

pygame.init()

# Dimensiones de la ventana 
WINDOW_WIDTH = 800  
WINDOW_HEIGHT = 800  

# Dimensiones del tablero
BOARD_WIDTH = 200 
BOARD_HEIGHT = 500 

BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2 
BLOCK_SIZE = 20

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED_LIGHT = (255, 128, 128)
FONT_SIZE = 24
YELLOW = (249, 247, 98)
TRANSPARENT = (0, 0, 0, 50)
BLUE = (12, 18, 58)

INITIAL_COUNTDOWN = 30

INITIAL_SPEED = 5
INCREASE_INTERVAL = 5
INCREASE_VAL = 1.125

fuenteGP = "TetrisPopUp/fuentes/game_power.ttf"
fuente8Bit = "TetrisPopUp/fuentes/8Bit.ttf"

background_image = pygame.image.load('assets/background.jpeg')

pygame.mixer.music.load('assets/music/tetris_song.ogg')  

clear_row_sound = pygame.mixer.Sound('assets/music/line.wav')
piece_drop_sound = pygame.mixer.Sound('assets/music/drop.mp3')
win_sound = pygame.mixer.Sound('assets/music/win.mp3')
lose_sound = pygame.mixer.Sound('assets/music/lose.mp3')


def exit_game(score):
    pygame.quit()
    return score


def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, FONT_SIZE)
    score_font = pygame.font.Font(fuente8Bit, FONT_SIZE)
    timer_font = pygame.font.Font(fuente8Bit, FONT_SIZE)

    pygame.mixer.music.play(-1)

    start_time = time.time()

    game_over = False
    game_over_sound_played = False  
    ended = False

    board = [[None] * (BOARD_WIDTH // BLOCK_SIZE) for _ in range(BOARD_HEIGHT // BLOCK_SIZE)]

    blocks = [Block()] # Active blocks

    speed = INITIAL_SPEED  
    last_increase_time = time.time()  

    score = 0
    countdown_timer = INITIAL_COUNTDOWN

    running = True
    while running:
        screen.blit(background_image, (0, 0))  

        pygame.draw.rect(screen, WHITE, (BOARD_OFFSET_X, 0, BOARD_WIDTH, BOARD_HEIGHT))

        pygame.draw.line(screen, BLACK, (BOARD_OFFSET_X, 0), (BOARD_OFFSET_X, BOARD_HEIGHT), 2)
        pygame.draw.line(screen, BLACK, (BOARD_OFFSET_X + BOARD_WIDTH, 0), (BOARD_OFFSET_X + BOARD_WIDTH, BOARD_HEIGHT), 2)

        current_time = time.time()
        elapsed_time = time.time() - start_time

        if current_time >= INCREASE_INTERVAL + last_increase_time:
            speed *= INCREASE_VAL  
            last_increase_time = current_time  

        clock.tick(speed)  

        if elapsed_time >= 1:  
            if not game_over or countdown_timer > 0:  
                countdown_timer = max(countdown_timer - 1, 0)
                start_time = time.time()  

        if not game_over or countdown_timer > 0: 
            timer_text = timer_font.render(f"Time: {countdown_timer}", True, BLACK)
            screen.blit(timer_text, (10, 10))

        score_text = score_font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 30))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        # Move left
                        blocks[-1].move_left(board)
                    elif event.key == pygame.K_RIGHT:
                        # Move right
                        blocks[-1].move_right(board)
                    elif event.key == pygame.K_UP:
                        # Rotate
                        blocks[-1].rotate(board)
                    elif event.key == pygame.K_DOWN:
                        # Lower down
                        while not blocks[-1].collide(board):
                            blocks[-1].move_down()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if final_score_popup.get_rect().collidepoint(mouse_x, mouse_y):
                        for boton in final_score_popup.botones:
                            if boton.rect.collidepoint(mouse_x, mouse_y):
                                if boton.accion == "REINICIAR":
                                    return main()
                                elif boton.accion == "SALIR":
                                    return exit_game(score)

        if not game_over:
            
            current_block = blocks[-1]

            if current_block.falling:
                current_block.move_down()

            if current_block.collide(board):
                for i in range(len(current_block.shape)):
                    for j in range(len(current_block.shape[i])):
                        if current_block.shape[i][j]:
                            board[current_block.y // BLOCK_SIZE + i][(current_block.x - BOARD_OFFSET_X) // BLOCK_SIZE + j] = current_block.color

                # Delete complete rows and increase puntuation
                rows_to_delete = set()
                for i in range(len(board)):
                    if all(board[i]):
                        rows_to_delete.add(i)
                        score += 100  

                for row in rows_to_delete:
                    del board[row]
                    board.insert(0, [None] * (BOARD_WIDTH // BLOCK_SIZE))
                    clear_row_sound.play() 

                if not rows_to_delete:
                    blocks.append(Block())
                    piece_drop_sound.play()

                if any(board[1]): 
                    game_over = True

                if countdown_timer == 0:
                    game_over = True

        # Draw board
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j]:
                    pygame.draw.rect(screen, board[i][j], (j * BLOCK_SIZE + BOARD_OFFSET_X, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        current_block.draw(screen)

        # Load game over screen
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
                game_over_surface.fill((0, 255, 0, 128))  
            else:
                game_over_surface.fill(RED_LIGHT + (128,))  
                ended = True
            screen.blit(game_over_surface, (0, 0))


            popup_width = 400  
            popup_height = 300  
            popup_x = (WINDOW_WIDTH - popup_width) // 2 
            popup_y = (WINDOW_HEIGHT - popup_height) // 2 

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

            final_score_popup.draw(screen)

            countdown_timer = 0 

        pygame.display.flip()
        clock.tick(30)  
    

    pygame.quit()
    return score

if __name__ == "__main__":
    main()