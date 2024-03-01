from enum import Enum
# This class manages the state of the game
class GameState:
    # Store already played minigames to lock them
    alreadyPlayedMinigames = [True, True, True]
    
    def __init__(self):
        self.state = State.InitialScreen
    
    def addPlayedMinigame(self, minigame):
        self.alreadyPlayedMinigames.append(minigame)
    
    def getState(self):
        return self.state
    
    def setState(self, state):
        self.state = state
# The states the game considers
class State(Enum):
    InitialScreen = 1
    TrashGameLVL1 = 2
    TrashGameLVL2 = 3
    TrashGameLVL3 = 4


