import pygame
from config import * 
from entities import Player, Pill
from pathfinding import a_star
from ui import start_menu, draw_score
import random
import sys
import heapq



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Chase Game")
clock = pygame.time.Clock()



# ------------------ MAZE GENERATION ------------------ #
def generate_maze(rows, cols):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if random.random() < 0.2 and (r, c) not in [(0, 0), (rows - 1, cols - 1)]:
                grid[r][c] = 1
    return grid

def draw_maze(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if grid[r][c] == 1:
                pygame.draw.rect(screen, BLACK, rect)

def main():
    grid = generate_maze(ROWS, COLS)
    player = Player(0, 0, YELLOW)
    ghost = Player(ROWS - 1, COLS - 1, RED)
    pill = Pill(grid)
    
    print(grid)
    score = 0
    ghost_speed = 0.25
    normal_player_speed = 0.25
    powered_player_speed = normal_player_speed * 4
    player_speed = normal_player_speed

    is_powered = False
    powered_timer = 0

    player_move_accumulator = 0
    ghost_move_accumulator = 0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Determine movement keys based on control scheme
        if control_scheme == "arrows":
            up_key, down_key, left_key, right_key = pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
        else:
            up_key, down_key, left_key, right_key = pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d

        player_move_accumulator += dt * player_speed * 10
        ghost_move_accumulator += dt * ghost_speed * 10

        if player_move_accumulator >= 1:
            dx, dy = 0, 0
            if keys[up_key]:
                dy = -1
            elif keys[down_key]:
                dy = 1
            elif keys[left_key]:
                dx = -1
            elif keys[right_key]:
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
            player_speed = powered_player_speed
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

        # Change background color based on powered mode
        if is_powered:
            screen.fill(BLUE)
        else:
            screen.fill(WHITE)

        draw_maze(grid)
        if pill:
            pill.draw(screen)
        player.draw(screen)
        ghost.draw(screen)
        draw_score(screen, score)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# ------------------ RUN GAME ------------------ #
if __name__ == '__main__':
    start_menu(screen)
    main()
