import pygame
from pygame.locals import *
import sys
import Pantalla.popup as PopUp
import TrashGame.main as TrashGame
from GameState import GameState, State

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
    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        state = game_state.getState()
        if state == State.InitialScreen:          
            aux = PopUp.main()
            game_state.setState(aux)
        elif state == State.TrashGameLVL1:
            fade_transition()
            (aux, played_minigame) =TrashGame.main(1, game_state, WINDOW)
            game_state.addPlayedMinigame(played_minigame)
            game_state.setState(aux)

            # TODO: Add the returning minigame from TrashGame to GameState
        elif state == State.TrashGameLVL2:
            # TODO: Add Galicia animation. This animation should last a predefined time and then die.
            fade_transition()
            (aux, played_minigame) =TrashGame.main(2, game_state, WINDOW)
            game_state.addPlayedMinigame(played_minigame)
            game_state.setState(aux)
            # TODO: Add the returning minigame from TrashGame to GameState
        elif state == State.TrashGameLVL3:
            # TODO: Add Galicia animation. This animation should last a predefined time and then die.
            fade_transition()
            (aux, played_minigame) =TrashGame.main(3, game_state, WINDOW)
            game_state.addPlayedMinigame(played_minigame)
            game_state.setState(aux)
            # TODO: Add the returning minigame from TrashGame to GameState
        # The logic of the minigames must go inside TrashGame and TrashGame.main() should return the minigame the user chose.
        # TODO: Make a transition animation between the states. ( Black Circle Closing-Opening?)
                           
        pygame.display.update()
        fpsClock.tick(FPS)

main()
