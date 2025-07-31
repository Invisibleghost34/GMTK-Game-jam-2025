import pygame 
import random 
import pickle 

#Constants 
WIDTH, HEIGHT = 700, 700 
ROWS, COLS = 20, 20 
size = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT))

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

#Create grid 
grid = [[Cell(x,y) for y in range(ROWS)] for x in range(COLS)]

def get_cell(x,y):
    if 0 <= x < COLS and 0 <= y < ROWS:
        return grid[x][y]


def check_neighbours(cell): 
    neighbours = []

    directions = {
        'up' : (0,-1),
        'right' : (1,0),
        'down' : (0,1),
        'left' : (-1, 0)
    }
    for direction, (dx, dy) in directions.items():
        neighbour = get_cell(cell.x + dx, cell.y + dy)
        if neighbour and not neighbour.visited: 
            neighbours.append((direction, neighbour))
    return neighbours
    
def remove_walls(curr_cell, direction, next_cell):
    if direction == 'up':
        curr_cell.walls['up'] = False
        next_cell.walls['down'] = False 
    elif direction == 'down':
        curr_cell.walls['down'] = False
        next_cell.walls['up'] = False 
    elif direction == 'left':
        curr_cell.walls['left'] = False
        next_cell.walls['right'] = False 
    elif direction == 'right':
        curr_cell.walls['right'] = False
        next_cell.walls['left'] = False 

def DFS_backtracking(cell):
    cell.visited = True 

    neighbours = check_neighbours(cell)
    while neighbours: 
        direction, next_cell = random.choice(neighbours)
        remove_walls(cell, direction, next_cell)
        DFS_backtracking(next_cell)
        neighbours = check_neighbours(cell)


def draw_grid():
    for row in grid:
        for cell in row:
            cell.draw(screen)

              

