import pygame
import sys

from WelcomeScreen.Button import Button 
from ResourceManager import ResourceManager
from GameState import State

resource_manager = ResourceManager()

### Draws a rounded rectangle ###
def draw_rounded_rectangle(surface):
    s = pygame.Surface((400, 200), pygame.SRCALPHA)
    s.fill((218, 255, 252, 90))
    surface.blit(s, (200, 355))
    #pygame.draw.rect(surface, (218, 255, 252, 60), (200, 355, 400, 200), 0, 50)

### Draws the Trash Game Rules on a surface ###
def drawTrashGameRules(surface):
    background_image = resource_manager.trash_game_instructions.get()
    surface.blit(background_image, (175, 100))

### Loads and plays the music ###
def play_music():
    pygame.mixer.music.load("WelcomeScreen/WelcomeScreenMusic.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    
def main(WINDOW):
    play_music()
    clock = pygame.time.Clock()
    animation_background_asset = resource_manager.popup_animation.get()
    x, y = 0, 0
    ## Declare Game Name ###
    gameName = resource_manager.game_name.get()
    ### Declare the buttons to be used ###
    playButton = Button(300, 375, "JUGAR")  
    instructionsButton = Button(300, 475, "INSTRUCCIONES")  
    backButton = Button(300, 675, "VOLVER")
    ### Declare out loop variables ###
    past_time = 0
    menu_show_time = 2000 
    showing_rules = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.top_rect.collidepoint(event.pos):
                    # Game State should change to TrashGameLVL1
                    return State.TrashGameLVL1
                elif instructionsButton.top_rect.collidepoint(event.pos):
                    # Show Instructions
                    showing_rules = True
                elif backButton.top_rect.collidepoint(event.pos):
                    # Hide Instructions
                    showing_rules = False
        
        ### Draw the background animation ###
        relative_x = x % animation_background_asset.get_rect().height
        WINDOW.blit(animation_background_asset, (relative_x - animation_background_asset.get_rect().height, y))
        if relative_x < 800:
            WINDOW.blit(animation_background_asset, (relative_x, 0))
        x += 1
        past_time += clock.get_time()

        ### Draw the content ###
        WINDOW.blit(gameName, (400-gameName.get_width()//2, 50))
        if not showing_rules:
            if past_time >= menu_show_time:
                draw_rounded_rectangle(WINDOW) 
                playButton.update()  
                instructionsButton.update()  
                playButton.draw(WINDOW)  
                instructionsButton.draw(WINDOW)  
        else:
            drawTrashGameRules(WINDOW)
            backButton.update()
            backButton.draw(WINDOW)

        pygame.display.update()
        clock.tick(60)


