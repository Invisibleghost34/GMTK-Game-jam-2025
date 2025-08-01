import pygame
import random
import sys
import heapq

# Constants
WIDTH, HEIGHT = 600, 600  # Window size
ROWS, COLS = 20, 20       # Maze size
TILE_SIZE = WIDTH // COLS  # Tile size to fit maze exactly in window
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Chase Game")
clock = pygame.time.Clock()

def generate_maze(rows, cols):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            # Avoid blocking start and end tiles
            if random.random() < 0.2 and (r, c) not in [(0, 0), (rows - 1, cols - 1)]:
                grid[r][c] = 1  # wall
    return grid

def draw_maze(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if grid[r][c] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, BLUE, rect)  # floor color

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
            if grid[new_row][new_col] == 0:  # free cell
                self.row = new_row
                self.col = new_col
                self.rect.topleft = (self.col * TILE_SIZE, self.row * TILE_SIZE)

    def draw(self):
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

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

# A* Algorithm for pathfinding
def a_star(grid, start, goal):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0] + dr, current[1] + dc)
            if (0 <= neighbor[0] < ROWS and
                0 <= neighbor[1] < COLS and
                grid[neighbor[0]][neighbor[1]] == 0):

                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(goal, neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

    path = []
    current = goal
    while current != start:
        if current not in came_from:
            return []
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def draw_score(score):
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Ghosts Caught: {score}", True, BLACK)
    screen.blit(text, (10, 10))

def main():
    grid = generate_maze(ROWS, COLS)

    player = Player(0, 0, YELLOW)
    ghost = Player(ROWS - 1, COLS - 1, RED)
    pill = Pill(grid)

    score = 0
    ghost_speed = 0.25  # tiles per frame (slower start)
    normal_player_speed = 0.25
    powered_player_speed = normal_player_speed * 4  # 4× normal speed when powered
    player_speed = normal_player_speed
    is_powered = False
    powered_timer = 0

    player_move_accumulator = 0
    ghost_move_accumulator = 0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # seconds passed since last frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player_move_accumulator += dt * player_speed * 10
        ghost_move_accumulator += dt * ghost_speed * 10

        if player_move_accumulator >= 1:
            dx, dy = 0, 0
            if keys[pygame.K_UP]:
                dy = -1
            elif keys[pygame.K_DOWN]:
                dy = 1
            elif keys[pygame.K_LEFT]:
                dx = -1
            elif keys[pygame.K_RIGHT]:
                dx = 1

            if dx != 0 or dy != 0:
                player.move(dx, dy, grid)
                player_move_accumulator = 0

        ghost_target = (player.row, player.col) if not is_powered else (ROWS - 1, COLS - 1)
        path = a_star(grid, (ghost.row, ghost.col), ghost_target)

        if path and ghost_move_accumulator >= 1:
            next_pos = path[0]
            ghost.row, ghost.col = next_pos
            ghost.rect.topleft = (ghost.col * TILE_SIZE, ghost.row * TILE_SIZE)
            ghost_move_accumulator = 0

        if pill and player.rect.colliderect(pill.rect):
            is_powered = True
            powered_timer = pygame.time.get_ticks()
            player_speed = powered_player_speed  # much faster now
            pill = None

        if is_powered and pygame.time.get_ticks() - powered_timer > 5000:
            is_powered = False
            player_speed = normal_player_speed
            if pill is None:
                pill = Pill(grid)

        if player.rect.colliderect(ghost.rect):
            if is_powered:
                score += 1
                ghost_speed += 0.1
                ghost = Player(ROWS - 1, COLS - 1, RED)
                pill = Pill(grid)
                is_powered = False
                player_speed = normal_player_speed
            else:
                print(f"Game Over. Total ghosts caught: {score}")
                running = False

        screen.fill(WHITE)
        draw_maze(grid)
        if pill:
            pill.draw()
        player.draw()
        ghost.draw()
        draw_score(score)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
