import pygame
from pygame.locals import *
import sys
import WelcomeScreen.Menu as WelcomeScreen
import TrashGame.main as TrashGame
from GameState import GameState, State
from FinalScreen import FinalScreen

FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Trash Game!')


def fade_transition():
    fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 10):
        fade_surface.set_alpha(alpha)
        WINDOW.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(60)

def main():
    game_state = GameState()
    final_screen = None
    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        state = game_state.getState()
        if state == State.InitialScreen:          
            aux = WelcomeScreen.main(WINDOW)
            game_state.setState(aux)
        elif state == State.TrashGameLVL1:
            fade_transition()
            (aux, played_minigame, puntuation) = TrashGame.main(1, game_state, WINDOW)
            game_state.addPlayedMinigame(played_minigame)
            game_state.addPoints(puntuation)
            game_state.setState(aux)
        elif state == State.TrashGameLVL2:
            fade_transition()
            (aux, played_minigame, puntuation) = TrashGame.main(2, game_state, WINDOW)
            game_state.addPlayedMinigame(played_minigame)
            game_state.addPoints(puntuation)
            game_state.setState(aux)
        elif state == State.TrashGameLVL3:
            fade_transition()
            (aux, played_minigame, puntuation) = TrashGame.main(3, game_state, WINDOW)
            game_state.addPlayedMinigame(played_minigame)
            game_state.addPoints(puntuation)
            fade_transition()
            game_state.setState(aux)
        elif state == State.FinalScreen:
            if final_screen == None:
                final_screen = FinalScreen(game_state.getTotalPoints())
            final_screen.draw(WINDOW)
                           
        pygame.display.update()
        fpsClock.tick(FPS)

main()
