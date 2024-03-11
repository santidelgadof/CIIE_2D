import pygame
from enum import Enum
from TrashGame.Container import TrashType

# Manages the resources of the game.
# All the resources must be loaded into memory by the resource manager
class ResourceManager:
    def __init__(self):
        # Trash Game Instructions
        self.trash_game_instructions = Resource("WelcomeScreen/InstruccionesTrashGame.png", True)
        # All the trash items
        self.trash_items = [
            (Resource("TrashGame/assets/trash/CajaCarton.png", True), TrashType.PAPER),
            (Resource("TrashGame/assets/trash/Cocacola.png", True), TrashType.GLASS),
            (Resource("TrashGame/assets/trash/Glass.png", True), TrashType.GLASS),
            (Resource("TrashGame/assets/trash/LataAtun.png", True), TrashType.PLASTIC),
            (Resource("TrashGame/assets/trash/LataRefresco.png", True), TrashType.PLASTIC),
            (Resource("TrashGame/assets/trash/Periodicos.png", True), TrashType.PAPER),
            (Resource("TrashGame/assets/trash/Queso.png", True), TrashType.ORGANIC),
            (Resource("TrashGame/assets/trash/Tomate.png", True), TrashType.ORGANIC)
        ]
        # All the containers
        self.organic_container = Resource("TrashGame/assets/containers/OrganicContainer.png", True)
        self.plastinc_container = Resource("TrashGame/assets/containers/PlasticContainer.png", True)
        self.glass_container = Resource("TrashGame/assets/containers/GlassContainer.png", True)
        self.paper_container = Resource("TrashGame/assets/containers/PaperContainer.png", True)
        self.bag = Resource("TrashGame/assets/containers/Bag.png", True)
        # Rest of the media
        self.trash_background = Resource("TrashGame/assets/bg.jpeg")
        self.sad_face = Resource("TrashGame/assets/sadFace.png", True)
        self.tech_piece = Resource("TrashGame/assets/tech.jpeg", True)

        self.popup_animation = Resource("WelcomeScreen/Animacion.jpg")

        # Arcade media
        self.arcade_player_up_image1 = Resource('Arcade/assets/player/up1.png', True)
        self.arcade_player_down_image1 = Resource('Arcade/assets/player/down1.png', True)
        self.arcade_player_left_image1 = Resource('Arcade/assets/player/left1.png', True)
        self.arcade_player_right_image1 = Resource('Arcade/assets/player/right1.png', True)

        self.arcade_player_up_image2 = Resource('Arcade/assets/player/up2.png', True)
        self.arcade_player_down_image2 = Resource('Arcade/assets/player/down2.png', True)
        self.arcade_player_left_image2 = Resource('Arcade/assets/player/left2.png', True)
        self.arcade_player_right_image2 = Resource('Arcade/assets/player/right2.png', True)

        self.arcade_background = Resource('Arcade/assets/arcade_background.jpg')

        #Atrapa_Game
        self.hole = Resource("CucarachaGame/Assets/Agujero.png", True)
        self.hole_slow = Resource("CucarachaGame/Assets/Agujero_slow.png", True)
        self.hole_speed = Resource("CucarachaGame/Assets/Agujero_speed.png", True)
        self.insect = Resource("CucarachaGame/Assets/Insecticida.png", True)
        self.background_image = Resource("CucarachaGame/Assets/back.jpg", True)
        self.background_slow = Resource("CucarachaGame/Assets/back_slow.png", True)
        self.background_speed = Resource("CucarachaGame/Assets/back_speed.png", True)
        self.cucaracha = Resource("CucarachaGame/Assets/cucaracha.png", True)
        self.speed = Resource("CucarachaGame/Assets/speed_item.png", True)
        self.slow = Resource("CucarachaGame/Assets/slow_item.png", True)

        # Tetris media
        self.tetris_background = Resource("Tetris/assets/background.jpeg")

        # GarbagePiles media
        self.arcade_background = Resource('Arcade/assets/arcade_background.jpg')


        # Tetris media
        self.tetris_background = Resource("Tetris/assets/background.jpeg")
        self.tetris_instructions = Resource("Tetris/assets/instructions_tetris.png")

        #GARBAGEPILE media
        self.pile_bg = Resource("GarbageTowers/images/bg.jpg")
        self.pile_floor = Resource("GarbageTowers/images/floor.jpg")
        self.pile_lightOn = Resource("GarbageTowers/images/lightBulbOn.png")
        self.pile_lightOff = Resource("GarbageTowers/images/lightBulbOff.png")

        self.pile_instructions = Resource("GarbageTowers/images/Instructions_GarbagePiles.png")

        self.pile_blocks = [
            Resource("GarbageTowers/images/blocks/bolsa_basura_Amarilla.png"),
            Resource("GarbageTowers/images/blocks/bolsa_basura_Azul.png"),
            Resource("GarbageTowers/images/blocks/bolsa_basura_Negra.png"),
            Resource("GarbageTowers/images/blocks/bolsa_basura_Verde.png")
        ]

        #CUCA
        self.cuca_instructions = Resource("CucarachaGame/Assets/instructions_cuca.png")

        
        

# This class models a resource 
class Resource:
    res = None
    def __init__(self, resource_url, needs_transparency=False) -> None:
        self.resource_url = resource_url
        self.needs_transparency = needs_transparency
    
    def get(self):
        if self.res != None:
            return self.res
        else:
            if self.needs_transparency:
                self.res = pygame.image.load(self.resource_url).convert_alpha()
            else:
                self.res = pygame.image.load(self.resource_url)
            return self.res

#class MediaType(Enum):
#    IMAGE = 1
#    AUDIO = 2