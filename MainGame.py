import pygame
from pygame.locals import *
import sys
import Pantalla.popup as PopUp
import TrashGame.main as TrashGame
import CucarachaGame.Atrapa as CucarachaGame
from GameState import GameState, State, Minigame

FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Trash Game!')

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
            # TODO: Add Galicia animation. This animation should last a predefined time and then die.
            TrashGame.main(1)
            # TODO: Add the returning minigame from TrashGame to GameState
        elif state == State.TrashGameLVL2:
            # TODO: Add Galicia animation. This animation should last a predefined time and then die.
            TrashGame.main(2)
            # TODO: Add the returning minigame from TrashGame to GameState
        elif state == State.TrashGameLVL3:
            # TODO: Add Galicia animation. This animation should last a predefined time and then die.
            TrashGame.main(3)
            # TODO: Add the returning minigame from TrashGame to GameState
        elif state == Minigame.CucarachaGame:
            CucarachaGame.main()

        # The logic of the minigames must go inside TrashGame and TrashGame.main() should return the minigame the user chose.
        # TODO: Make a transition animation between the states. ( Black Circle Closing-Opening?)
                           
        pygame.display.update()
        fpsClock.tick(FPS)

main()
