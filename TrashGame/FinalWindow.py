import pygame
from GameState import State
from ArcadeMachinePopup.popUpClass import PopUp
from ArcadeMachinePopup.textClass import Text
from ArcadeMachinePopup.buttonClass import Boton

WHITE = (255, 255, 255)
BLUE = (12, 18, 58)
YELLOW = (249, 247, 98 )
TRANSPARENT = (0, 0, 0, 50)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

fuenteGP = "ArcadeMachinePopup/fuentes/game_power.ttf"
fuente8Bit = "ArcadeMachinePopup/fuentes/8Bit.ttf"

# The final window for the LVL. Different if the user wins or not.
class FinalWindow:
    buttons = []
    def __init__(self, won, lvl) -> None:
        if won:
            self.text = [
                Text("Felicidades!", 60, YELLOW, WINDOW_WIDTH//2 , WINDOW_HEIGHT//3 - 140, True, fuenteGP)  
            ]
            self.buttons = [
                Boton(WINDOW_WIDTH//2, WINDOW_HEIGHT//3 - 40, 100, 40, "CONTINUAR", fuenteGP, TRANSPARENT, YELLOW, 40, "CONTINUAR")
            ]
        else:
            self.text = [
                Text("Derrota!", 60, YELLOW, WINDOW_WIDTH//2 , WINDOW_HEIGHT//3 - 140, True, fuenteGP)
            ]
            self.buttons = [
                Boton(WINDOW_WIDTH//2, WINDOW_HEIGHT//3 - 40, 100, 40, "REINTENTAR", fuenteGP, TRANSPARENT, YELLOW, 40, "REINTENTAR")
            ]
        
        self.rotations = [0]
        self.popup = PopUp(WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT//3 - 200, 400, 300, 60, BLUE, 8, WHITE, self.buttons, self.text, self.rotations)

    def draw(self, surface):
        self.popup.draw(surface)