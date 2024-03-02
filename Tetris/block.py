import pygame
import random

BLOCK_SIZE = 20
BOARD_WIDTH = 200 
BOARD_HEIGHT = 500 
WINDOW_WIDTH = 800  
BLACK = (0, 0, 0)

BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2 

blocks = [
    [[[0, 2, 2],
      [2, 2, 0]],  # "S" block
     (0, 0, 255)],  # Blue

    [[[3, 3, 0],
      [0, 3, 3]],  # "Z" block
     (255, 165, 0)],  #  Orange

    [[[4, 4, 4],
      [0, 4, 0]],  # "T" block 
     (150, 75, 0)],  # Brown

    [[[0, 0, 5],
      [5, 5, 5]],  # "L" block
     (0, 255, 0)],  # Green

    [[[6, 6],
      [6, 6]],  # "O" block
     (255, 255, 0)],  # Yellow

    [[[7, 7, 7, 7]],  # "I" block
     (255, 0, 0)]  # Red
]


class Block:

    def __init__(self):
        self.x = random.randint(2, BOARD_WIDTH // BLOCK_SIZE - 4) * BLOCK_SIZE + BOARD_OFFSET_X 
        self.y = 0
        self.shape, self.color = random.choice(blocks)
        self.falling = True
    

    def draw(self, surface):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    pygame.draw.rect(surface, self.color, (self.x + j * BLOCK_SIZE, self.y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(surface, BLACK, (self.x + j * BLOCK_SIZE, self.y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


    def move_down(self):
        self.y += BLOCK_SIZE
    

    def move_left(self, board):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    if self.x + j * BLOCK_SIZE <= BOARD_OFFSET_X or (self.x + j * BLOCK_SIZE) // BLOCK_SIZE - 1 >= 0 and board[self.y // BLOCK_SIZE + i][(self.x + j * BLOCK_SIZE - BOARD_OFFSET_X) // BLOCK_SIZE - 1]:
                        return
        self.x -= BLOCK_SIZE


    def move_right(self, board):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    if (self.x + j * BLOCK_SIZE >= BOARD_WIDTH + BOARD_OFFSET_X - BLOCK_SIZE or
                        (self.x + j * BLOCK_SIZE - BOARD_OFFSET_X) // BLOCK_SIZE + 1 < len(board[0]) and board[self.y // BLOCK_SIZE + i][(self.x + j * BLOCK_SIZE - BOARD_OFFSET_X) // BLOCK_SIZE + 1]):
                        return
        self.x +=  BLOCK_SIZE
    

    def collide(self, board):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    if (self.y + i * BLOCK_SIZE >= BOARD_HEIGHT - BLOCK_SIZE or
                        (self.y // BLOCK_SIZE + i + 1 < len(board) and self.x // BLOCK_SIZE + j - BOARD_OFFSET_X // BLOCK_SIZE < len(board[0]) and board[self.y // BLOCK_SIZE + i + 1][(self.x - BOARD_OFFSET_X + j * BLOCK_SIZE) // BLOCK_SIZE])):
                        self.falling = False
                        return True
        return False


    def can_rotate(self, board):
        current_shape = [row[:] for row in self.shape]
        rotated_shape = [[current_shape[j][i] for j in range(len(current_shape))] for i in range(len(current_shape[0]))]
        rotated_shape.reverse()
        for i in range(len(rotated_shape)):
            for j in range(len(rotated_shape[i])):
                if rotated_shape[i][j]:
                    if (self.y + i * BLOCK_SIZE >= BOARD_HEIGHT or self.x + j * BLOCK_SIZE < BOARD_OFFSET_X or
                        self.x + j * BLOCK_SIZE >= BOARD_WIDTH + BOARD_OFFSET_X or board[self.y // BLOCK_SIZE + i][(self.x - BOARD_OFFSET_X + j * BLOCK_SIZE) // BLOCK_SIZE]):
                        return False
        return True


    def rotate(self, board):
        if self.can_rotate(board):
            current_shape = [row[:] for row in self.shape]
            self.shape = [[current_shape[j][i] for j in range(len(current_shape))] for i in range(len(current_shape[0]))]
            self.shape.reverse()