import pygame
from tetris import main

def run_game():
    pygame.init()
    score = main()  # Obtenemos la puntuación final devuelta por main()
    pygame.quit()
    return score

if __name__ == "__main__":
    final_score = run_game()
    print(f"Puntuación final: {final_score}")
