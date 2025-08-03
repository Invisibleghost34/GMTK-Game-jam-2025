import pygame 
import random
from config import TILE_SIZE, GREEN, ROWS, COLS

class Player:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def move(self, dx, dy, grid):
        new_row = self.row + dy
        new_col = self.col + dx
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            if grid[new_row][new_col] == 0:
                self.row = new_row
                self.col = new_col
                self.rect.topleft = (self.col * TILE_SIZE, self.row * TILE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Pill:
    def __init__(self, grid):
        while True:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            if grid[r][c] == 0 and (r, c) not in [(0, 0), (ROWS-1, COLS-1)]:
                self.row, self.col = r, c
                break
        self.rect = pygame.Rect(self.col * TILE_SIZE, self.row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)