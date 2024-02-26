import pygame
from pygame.locals import *
import sys
import Pantalla.popup as PopUp
import TrashGame.main as TrashGame


####### STATE ########
## 0 -> Initial State
## 1 -> TrashGame LVL 1


FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Trash Game!')

def main():
    isPopUP = False
    state = 0
    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if state == 0:             
            state = PopUp.main()
        if state == 1:
            TrashGame.main(1)
        

                            
        pygame.display.update()
        fpsClock.tick(FPS)

main()
