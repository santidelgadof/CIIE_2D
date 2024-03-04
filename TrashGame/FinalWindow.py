import pygame
from TrashGame.Button import Button
from GameState import State

class FinalWindow:
    buttons = []
    def __init__(self, won, lvl) -> None:
        self.won = won
        if won:
            def action_function():
                    if lvl == 1:
                        return State.TrashGameLVL2
                    if lvl == 2:
                        return State.TrashGameLVL3
                    if lvl == 3:
                         return "continue4"
            self.buttons.append(Button(300, 600, 200, 75, "CONTINUAR", (255,0,0), (240,240,240), action_function))
        else:
            def action_function():
                    return "restart"
            self.buttons.append(Button(300, 600, 200, 75, "REINTENTAR", (255,0,0), (240,240,240), action_function))
    
    def draw(self, surface):
        window = pygame.Rect(200, 200, 400, 500)
        pygame.draw.rect(surface, (240, 240, 240), window)
        pygame.draw.rect(surface, (255, 255, 255), window, width= 3)
        if self.won:
            font_Congrats = pygame.font.SysFont(None, 48)
            congrats = font_Congrats.render("¡FELICIDADES!", True, (0,0,0),)
            rect = congrats.get_rect()
            rect.center = (400, 250)
            surface.blit(congrats, rect)
            font_Subtitle = pygame.font.SysFont(None, 22)
            subtitle_text = "Has ganado una pieza de los planos\npara la máquina de limpieza."
            subtitle_lines = subtitle_text.split("\n")
            y_offset = 0
            for line in subtitle_lines:
                congrats = font_Subtitle.render(line, True, (0,0,0))
                rect = congrats.get_rect()
                rect.center = (400, 350 + y_offset)
                y_offset += rect.height + 5  # Adjust the vertical spacing between lines
                surface.blit(congrats, rect)
            for button in self.buttons:
                button.draw(surface)
        else:
            font_Congrats = pygame.font.SysFont(None, 48)
            congrats = font_Congrats.render("Has Perdido", True, (0,0,0))
            rect = congrats.get_rect()
            rect.center = (400, 250)
            surface.blit(congrats, rect)
            for button in self.buttons:
                button.draw(surface)