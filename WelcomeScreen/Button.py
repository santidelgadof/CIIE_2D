import pygame as pg

class Button:
    def __init__(self, x=0, y=0, text="", width=200, height=50, elev=6):
        self.font = pg.font.Font('WelcomeScreen/fuente.ttf', 24)
        self.text = self.font.render(text, True, "#000000")
        self.text_rect = self.text.get_rect()

        self.bottom_rect = pg.Rect((x+elev, y+elev), (width, height))
        self.top_rect = pg.Rect((x, y), (width, height))
        self.text_rect.center = self.top_rect.center

        self.hover = False
        self.pressed = False
        self.clicked = False

    ### Updates the look of the button according to the cursor's situation ###
    def update(self):
        # Button is not pressed by default
        self.clicked = False
        # Check if user's cursor is over self
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.hover = True
            # Check if mouse is pressed
            if pg.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                # Check if mouse is unpressed over self
                if self.pressed is True:
                    self.pressed = False
                    self.clicked = True
        else:
            self.pressed = False
            self.hover = False

    ### Draws the button on a surface ###
    def draw(self, surface):
        top_rect_color = "#505D5C" if self.hover else "#C0CFCE"
        if not self.pressed:
            # If self is not pressed
            pg.draw.rect(surface, "#C4FFFE", self.bottom_rect)
            pg.draw.rect(surface, top_rect_color, self.top_rect)
            self.text_rect.center = self.top_rect.center
        else:
            # If self is pressed
            pg.draw.rect(surface, top_rect_color, self.bottom_rect)
            self.text_rect.center = self.bottom_rect.center
        surface.blit(self.text, self.text_rect)