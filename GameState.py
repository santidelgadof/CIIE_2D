from enum import Enum
# This class manages the state of the game
class GameState:
    # Store already played minigames to lock them
    alreadyPlayedMinigames = [True, True, True]
    totalPoints = 0
    
    def __init__(self):
        self.state = State.InitialScreen
    
    def addPlayedMinigame(self, minigame):
        self.alreadyPlayedMinigames = minigame
    
    def getState(self):
        return self.state
    
    def setState(self, state):
        self.state = state
    def getPlayedMinigames(self):
        return self.alreadyPlayedMinigames
    
    def getNextLvl(self):
        if self.state == State.TrashGameLVL1:
            return State.TrashGameLVL2
        elif self.state == State.TrashGameLVL2:
            return State.TrashGameLVL3
        elif self.state == State.TrashGameLVL3:
            return State.FinalScreen
        
    def getTotalPoints(self):
        return self.totalPoints
    
    def addPoints(self, points):
        self.totalPoints += points
# The states the game considers
class State(Enum):
    InitialScreen = 1
    TrashGameLVL1 = 2
    TrashGameLVL2 = 3
    TrashGameLVL3 = 4
    FinalScreen = 5


