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
#Save the maze data 
def save_maze(grid): 
    data = []
    for col in grid: 
        row_data = []
        for cell in col:
            row_data.append({
                'x': cell.x, 
                'y': cell.y, 
                'walls': cell.walls.copy()
            })
        data.append(row_data)
    return data



def pkl_to_matrix(maze_data):
    rows = len(maze_data)
    cols = len(maze_data[0])
    matrix_size_x = rows * 2 + 1 
    matrix_size_y = cols * 2 + 1 

    matrix = [[1 for _ in range(matrix_size_y)] for _ in range(matrix_size_x)]

    for x in range(cols):
        for y in range(rows):
            cell = maze_data[x][y]
            mx, my = x*2 + 1, y*2 + 1

            matrix[mx][my] = 0

            if not cell['walls']['up'] and my >1: #We set the path walkable if there are no walls in the certain directions
                matrix[mx][my - 1] = 0
            if not cell['walls']['down'] and my +1 < matrix_size_y:
                matrix[mx][my+1] = 0
            if not cell['walls']['left'] and mx > 1:
                matrix[mx-1][my] = 0
            if not cell['walls']['right'] and mx + 1 < matrix_size_x:
                matrix[mx+1][my] = 0
    return matrix

with open("maze.pkl", "rb") as fl: 
    maze_data = pickle.load(fl)

# for x in range(len(maze_data)):
#     for y in range(len(maze_data[0])):
#         cell = maze_data[x][y]
#         print(f"Cell ({x}, {y}) walls: {cell['walls']}")

matrix = pkl_to_matrix(maze_data)

for row in matrix:
    print("".join(['.' if x == 0 else '#' for x in row]))

    


              

