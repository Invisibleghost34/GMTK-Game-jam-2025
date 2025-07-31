import pygame 
import random 
import pickle 

#Constants 
WIDTH, HEIGHT = 700, 700 
ROWS, COLS = 20, 20 
size = WIDTH // COLS

#Colors 
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (75,75,75)

class Cell: 
    def __init__(self, x,y):
        self.x = x 
        self.y = y 
        self.visited = False
        self.walls = {'up':True, 'right': True, 'down': True, 'left': True}
    def draw(self, surface):
        x = self.x * size 
        y = self.y * size 

        if self.visited: 
            pygame.draw.rect(surface, BLACK, (x,y, size, size))
        if self.walls['up']:
            pygame.draw.line(surface, WHITE, (x,y), (x + size, y), 2)
        if self.walls['down']:
            pygame.draw.line(surface, WHITE, (x, y+size), (x+size, y+size), 2)
        if self.walls['right']:
            pygame.draw.line(surface, WHITE, (x+size, y), (x + size, y+size), 2)
        if self.walls['left']: 
            pygame.draw.line(surface, WHITE, (x,y), (x, y+size),)

        


# class Maze: 
#     def __init__(self, rows, cols):
#         self.rows = rows 
#         self.cols = cols 
#         self.grid = [[(0 for _ in range(cols))] for _ in range(rows)]
#         self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

#     def create_maze(self, walls):
#         #Pick a random starting point 

#         for y in range(self.rows):
#             for x in range(self.cols):
#                 cell_x, cell_y = x*CELL_WIDTH, y*CELL_HEIGHT
                

