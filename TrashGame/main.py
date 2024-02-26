import random
import pygame, sys
from pygame import mixer
from pygame.locals import *
from Theme import Theme
from Spawner import Spawner
from ClassificationArea import ClassificationArea
from TrashItem import TrashItem
from Container import *
from HealthBar import HealthBar
from AbstractFunctions import *
from FinalWindow import FinalWindow
from ResourceManager import ResourceManager
import os
pygame.init()


### PYGAME CONFIGURATION ###
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Trash Game!')

### GLOBALS ###
theme = Theme()
available_pngs = [f for f in os.listdir('assets/trash') if os.path.isfile(os.path.join('assets/trash', f))]

container_images = ["assets/containers/OrganicContainer.png", 
              "assets/containers/PlasticContainer.png", 
              "assets/containers/PaperContainer.png", 
              "assets/containers/GlassContainer.png" ]
resource_manager = ResourceManager()
### MAIN ###
def main(level): # Level is an int that stablishes the dificulty of the lvl
    try_again = True
    while(try_again):
        ### SetUp each level configuration ###
        mixer.music.load("assets/music/MainMusic.ogg")
        mixer.music.set_volume(0.3)
        mixer.music.play(-1) 
        if level == 1:
            spawn_interval = 2000  # Spawn a new TrashItem every 2 seconds (2000 milliseconds)
            distance_between_items = 120  # Desired distance between each trash item
            velocity = distance_between_items / (spawn_interval / 60) / 2
            firstClasificator = ClassificationArea(100, 350, theme.clasiAreaColor)
            secondClasificator = None
            organicContainer = Container(TrashType.ORGANIC, resource_manager.organic_container.get(), (10, 700))
            plasticContainer = Container(TrashType.PLASTIC, resource_manager.plastinc_container.get(), (650, 700))
            paperContainer = None
            glassContainer = None
            finalWindow = None
            trash_default_items = resource_manager.trash_items
            health_bar = HealthBar(5)
            current_lives = 5
            duration = 0.5 * 60 * 1000 

        if level == 2:
            spawn_interval = 2000  # Spawn a new TrashItem every 2 seconds (2000 milliseconds)
            distance_between_items = 120  # Desired distance between each trash item
            velocity = distance_between_items / (spawn_interval / 60) / 2
            firstClasificator = ClassificationArea(100, 100, theme.clasiAreaColor)
            secondClasificator = ClassificationArea(100, 500, theme.clasiAreaColor)
            organicContainer = Container(TrashType.ORGANIC, resource_manager.organic_container.get(), (10, 700))
            plasticContainer = Container(TrashType.PLASTIC, resource_manager.plastinc_container.get(), (640, 700))
            paperContainer = Container(TrashType.PAPER, resource_manager.paper_container.get(), (150, 700))
            glassContainer = Container(TrashType.GLASS, resource_manager.glass_container.get(), (500, 700))
            trash_default_items = resource_manager.trash_items
            finalWindow = None
            health_bar = HealthBar(5)
            current_lives = 5
            duration = 0.5 * 60 * 1000 
        if level == 3:
            spawn_interval = 1000  # Spawn a new TrashItem every 2 seconds (2000 milliseconds)
            distance_between_items = 120  # Desired distance between each trash item
            velocity = distance_between_items / (spawn_interval / 60) / 2
            firstClasificator = ClassificationArea(100, 100, theme.clasiAreaColor)
            secondClasificator = ClassificationArea(100, 500, theme.clasiAreaColor)
            organicContainer = Container(TrashType.ORGANIC, resource_manager.organic_container.get(), (10, 700))
            plasticContainer = Container(TrashType.PLASTIC, resource_manager.plastinc_container.get(), (640, 700))
            paperContainer = Container(TrashType.PAPER, resource_manager.paper_container.get(), (150, 700))
            glassContainer = Container(TrashType.GLASS, resource_manager.glass_container.get(), (500, 700))
            trash_default_items = resource_manager.trash_items
            finalWindow = None
            health_bar = HealthBar(5)
            current_lives = 5
            duration = 0.5 * 60 * 1000 
            
        ### Lvl independent values ###
        looping = True
        trash_items = []
        spawner = Spawner(spawn_interval, distance_between_items, velocity, trash_default_items)
        start_time = pygame.time.get_ticks()
        finish = False
        won = False
        progress_bar_width = 0

        ### LOOP ###
        while looping:
            
            ### Listen to Events ###
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_o: # Pressed 'o' (organico)
                        current_lives = firstClasificator.classify(trash_items, organicContainer.get_x_position(), organicContainer.get_y_position(), [TrashType.ORGANIC], current_lives)
                    if event.key == K_p: # Pressed 'p' ( plastico)
                        if level == 1:
                            current_lives = firstClasificator.classify(trash_items, plasticContainer.get_x_position(), plasticContainer.get_y_position(), [TrashType.PLASTIC, TrashType.PAPER, TrashType.GLASS], current_lives)
                        else:
                            current_lives = firstClasificator.classify(trash_items, plasticContainer.get_x_position(), plasticContainer.get_y_position(), [TrashType.PLASTIC], current_lives)
                    if secondClasificator != None:
                        if event.key == K_c: # Pressed 'c' (carton)
                            current_lives = secondClasificator.classify(trash_items, paperContainer.get_x_position(), paperContainer.get_y_position(), [TrashType.PAPER], current_lives)
                        if event.key == K_v: # Pressed 'v' (vidrio)
                            current_lives = secondClasificator.classify(trash_items, glassContainer.get_x_position(), glassContainer.get_y_position(), [TrashType.GLASS], current_lives)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if finalWindow != None:
                        pos = pygame.mouse.get_pos()
                        for button in finalWindow.buttons:
                            res = button.is_clicked(pos)
                            if res == "restart":
                                looping = False
                                    


            
            ### Spawning and progress bar update ###
            current_time = pygame.time.get_ticks()
            if not finish:
                trash_items = spawner.update(trash_items, current_time)
            elapsed_time = current_time - start_time
            if not finish:
                progress_bar_width = min((elapsed_time / duration) * WINDOW_WIDTH, WINDOW_WIDTH)
                if progress_bar_width >= 800:
                    finish = True
                    won = True
            if not finish:
            ### Move the TrashItems ###
                for trash_item in trash_items:
                    trash_item.move()  

            ### Remove the already vanished TrashItems ###
                for trash_item in trash_items:
                    if trash_item.dead:
                        if trash_item.for_a_good_reason:
                            trash_items.remove(trash_item)
                        else:
                            current_lives = current_lives - 1
                            trash_items.remove(trash_item)

            ### RENDERING ###
            # Draw the background
            background_image = pygame.image.load("assets/bg.jpeg")
            background_image = pygame.transform.scale(background_image, (800, 800))
            WINDOW.blit(background_image, (0, 0))

            # Draw Containers
            organicContainer.draw(WINDOW)
            plasticContainer.draw(WINDOW)
            if secondClasificator != None:
                paperContainer.draw(WINDOW)
                glassContainer.draw(WINDOW)
            # Draw the bag
            bag = pygame.image.load("assets/containers/Bag.png").convert_alpha()
            scaled_bag = pygame.transform.scale(bag, (bag.get_width() // 2, bag.get_height() // 2))
            WINDOW.blit(scaled_bag, (280, 700))
            # Draw the TrashItems
            for trash_item in trash_items:
                trash_item.draw(WINDOW)
            # Draw the belt
            drawBelt(WINDOW, theme, level, organicContainer, plasticContainer, paperContainer, glassContainer, firstClasificator, secondClasificator)
            # Draw the health bar
            health_bar.draw(WINDOW, current_lives)
            # Draw the TimeLine
            pygame.draw.rect(WINDOW, theme.timelineColor, (0, WINDOW_HEIGHT - 10, progress_bar_width, 10))
            # The user has no more lives ( Game Over )
            if not finish and current_lives == 0:
                finish = True
            if finish:
                if finalWindow == None:
                    finalWindow = FinalWindow(won)
                finalWindow.draw(WINDOW)

            ### UPDATE the WINDOW ###
            pygame.display.update()
            fpsClock.tick(FPS)

main(1)
