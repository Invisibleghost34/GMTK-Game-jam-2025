import pygame
from config import ROWS, COLS, WIDTH, HEIGHT, YELLOW, RED
from entities import Player, Pill

# Brightness overlay
_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
_current_alpha = 30
_overlay.fill((255, 255, 200, _current_alpha))

# Shared state
player = None
ghost = None
pill = None
score = 0
is_powered = False
powered_timer = 0
ghost_speed = 0.25
normal_player_speed = 0.25
powered_player_speed = normal_player_speed * 4
player_speed = normal_player_speed


def get_level():
    global player, ghost, pill, score, is_powered, powered_timer, ghost_speed, player_speed

    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for r in range(5, 15):
        grid[r][COLS // 2] = 1

    player = Player(0, 0, YELLOW)
    ghost = Player(ROWS - 1, COLS - 1, RED)
    pill = Pill(grid)
    score = 0
    is_powered = False
    powered_timer = 0
    ghost_speed = 0.25
    player_speed = normal_player_speed

    return grid, draw_overlay, handle_collisions


def draw_overlay():
    return _overlay


def increase_brightness():
    global _current_alpha
    _current_alpha = min(255, _current_alpha + 20)
    _overlay.fill((255, 255, 200, _current_alpha))


def handle_collisions(grid):
    global player, ghost, pill, score
    global is_powered, powered_timer, player_speed, ghost_speed

    current_time = pygame.time.get_ticks()

    # Pill collision
    if pill and player.rect.colliderect(pill.rect):
        is_powered = True
        powered_timer = current_time
        player_speed = powered_player_speed
        pill = None
        increase_brightness()

    # Power timeout
    if is_powered and current_time - powered_timer > 5000:
        is_powered = False
        player_speed = normal_player_speed
        if pill is None:
            pill = Pill(grid)

    # Ghost collision
    if player.rect.colliderect(ghost.rect):
        if is_powered:
            score += 1
            ghost_speed += 0.1
            ghost = Player(ROWS - 1, COLS - 1, RED)
            pill = Pill(grid)
            is_powered = False
            player_speed = normal_player_speed
            increase_brightness()
        else:
            return "game_over", score

    return "running", {
        "player": player,
        "ghost": ghost,
        "pill": pill,
        "score": score,
        "player_speed": player_speed,
        "ghost_speed": ghost_speed,
        "is_powered": is_powered
    }