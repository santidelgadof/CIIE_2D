import pygame
from ArcadeMachinePopup.textClass import Text
from ArcadeMachinePopup.buttonClass import Boton
from ArcadeMachinePopup.popUpClass import PopUp

WHITE = (255, 255, 255)
BLUE = (12, 18, 58)
YELLOW = (249, 247, 98 )
TRANSPARENT = (0, 0, 0, 50)
BLACK = (0, 0, 0)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

fuenteGP = "ArcadeMachinePopup/fuentes/game_power.ttf"
fuente8Bit = "ArcadeMachinePopup/fuentes/8Bit.ttf"

### Draws the final screen of the game displaying the total points ###
class FinalScreen:
    def __init__(self, puntuation) -> None:
        self.puntuation = puntuation
        self.text = [
                Text("Has completado el juego!", 50, YELLOW, WINDOW_WIDTH//2 , WINDOW_HEIGHT//2 - 50 , True, fuenteGP),
                Text("Puntuacion - - - - > " + puntuation.__str__(), 30, WHITE, WINDOW_WIDTH//2 , WINDOW_HEIGHT//2 + 50 , True, fuenteGP)
            ]
        self.rotations = [0, 0]
        self.popup = PopUp(WINDOW_WIDTH//2 - 350, WINDOW_HEIGHT//3, 700, 300, 60, BLUE, 8, WHITE, [], self.text, self.rotations)
    
    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, pygame.rect.Rect(0,0,WINDOW_WIDTH,WINDOW_HEIGHT))
        self.popup.draw(surface)