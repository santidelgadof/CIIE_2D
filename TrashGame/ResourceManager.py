import pygame
from enum import Enum
from Container import TrashType

# Manages the resources of the game.
# All the resources must be loaded into memory by the resource manager
class ResourceManager:
    def __init__(self):
        # All the trash items
        self.trash_items = [
            (Resource("assets/trash/CajaCarton.png", True), TrashType.PAPER),
            (Resource("assets/trash/Cocacola.png", True), TrashType.GLASS),
            (Resource("assets/trash/LataAtun.png", True), TrashType.PLASTIC),
            (Resource("assets/trash/LataRefresco.png", True), TrashType.PLASTIC),
            (Resource("assets/trash/Periodicos.png", True), TrashType.PAPER),
            (Resource("assets/trash/Queso.png", True), TrashType.ORGANIC),
            (Resource("assets/trash/Tomate.png", True), TrashType.ORGANIC)
        ]
        # All the containers
        self.organic_container = Resource("assets/containers/OrganicContainer.png", True)
        self.plastinc_container = Resource("assets/containers/PlasticContainer.png", True)
        self.glass_container = Resource("assets/containers/GlassContainer.png", True)
        self.paper_container = Resource("assets/containers/PaperContainer.png", True)
        self.bag = Resource("assets/containers/Bag.png", True)
        # Rest of the media
        self.trash_background = Resource("assets/bg.jpeg")
        self.sad_face = Resource("assets/sadFace.png", True)
        self.tech_piece = Resource("assets/tech.jpeg")

        
        

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