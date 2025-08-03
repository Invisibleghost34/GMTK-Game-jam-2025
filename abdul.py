import pygame
import random
import sys
import heapq

# Constants
WIDTH, HEIGHT = 700, 600
ROWS, COLS = 20, 20
TILE_SIZE = WIDTH // COLS
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Pacman Chase Game")

# Maze Generation (simple randomized walls)
def generate_maze(rows, cols):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if random.random() < 0.2 and (r, c) not in [(0, 0), (rows-1, cols-1)]:
                grid[r][c] = 1  # wall
    return grid

def draw_maze(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if grid[r][c] == 1:
                pygame.draw.rect(screen, BLACK, rect)

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

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Pill:
    def __init__(self, grid):
        while True:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            if grid[r][c] == 0:
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
            if (0 <= neighbor[0] < len(grid) and
                0 <= neighbor[1] < len(grid[0]) and
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
    screen.blit(text, (WIDTH - 180, 10))

def main():
    grid = generate_maze(ROWS, COLS)
    player = Player(0, 0, YELLOW)
    ghost = Player(ROWS-1, COLS-1, RED)
    pill = Pill(grid)

    print(grid)

    score = 0

    # Cooldowns in milliseconds
    player_move_cooldown = 150
    ghost_move_cooldown = 150

    last_player_move_time = 0
    last_ghost_move_time = 0

    is_powered = False
    powered_timer = 0

    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        # Player moves on cooldown
        if current_time - last_player_move_time > player_move_cooldown:
            if keys[pygame.K_UP]:
                player.move(0, -1, grid)
                last_player_move_time = current_time
            elif keys[pygame.K_DOWN]:
                player.move(0, 1, grid)
                last_player_move_time = current_time
            elif keys[pygame.K_LEFT]:
                player.move(-1, 0, grid)
                last_player_move_time = current_time
            elif keys[pygame.K_RIGHT]:
                player.move(1, 0, grid)
                last_player_move_time = current_time

        # Ghost pathfinding target
        ghost_target = (ROWS-2, COLS-2) if is_powered else (player.row, player.col)

        # Ghost moves on cooldown
        if current_time - last_ghost_move_time > ghost_move_cooldown:
            path = a_star(grid, (ghost.row, ghost.col), ghost_target)
            if path:
                next_pos = path[0]
                ghost.row, ghost.col = next_pos
                ghost.rect.topleft = (ghost.col * TILE_SIZE, ghost.row * TILE_SIZE)
            last_ghost_move_time = current_time

        # Collision: player and pill
        if pill and player.rect.colliderect(pill.rect):
            is_powered = True
            powered_timer = current_time
            pill = None

        # Power mode lasts 5 seconds
        if is_powered and current_time - powered_timer > 10000:
            is_powered = False

        # Collision: player and ghost
        if player.rect.colliderect(ghost.rect):
            if is_powered:
                score += 1
                # Optional: speed ghost up by lowering cooldown, or keep it constant
                # ghost_move_cooldown = max(50, ghost_move_cooldown - 10)  # Uncomment if you want faster ghost
                ghost = Player(ROWS-1, COLS-1, RED)
                pill = Pill(grid)
                is_powered = False
            else:
                print(f"Game Over. Total ghosts caught: {score}")
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_maze(grid)

        if pill:
            pill.draw()
        player.draw()
        ghost.draw()
        draw_score(score)

        pygame.display.flip()

if __name__ == '__main__':
    main()
