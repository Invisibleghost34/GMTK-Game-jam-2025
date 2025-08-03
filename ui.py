import pygame 
import sys 
from config import WIDTH, HEIGHT, WHITE, BLACK, GREY, control_scheme

def draw_score(screen, score):
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Ghosts Caught: {score}", True, BLACK)
    screen.blit(text, (10, 10))

# ------------------ OPTIONS MENU ------------------ #
def options_menu(screen):
    global control_scheme
    font_title = pygame.font.SysFont(None, 60)
    font_button = pygame.font.SysFont(None, 40)

    arrows_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50)
    wasd_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 10, 200, 50)

    while True:
        screen.fill(WHITE)
        title_text = font_title.render("Options", True, BLACK)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 150))

        pygame.draw.rect(screen, GREY, arrows_button)
        pygame.draw.rect(screen, GREY, wasd_button)

        arrows_text = font_button.render("Arrow Keys", True, BLACK)
        wasd_text = font_button.render("WASD Keys", True, BLACK)

        screen.blit(arrows_text, (arrows_button.x + 30, arrows_button.y + 10))
        screen.blit(wasd_text, (wasd_button.x + 40, wasd_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if arrows_button.collidepoint(event.pos):
                    control_scheme = "arrows"
                    return
                elif wasd_button.collidepoint(event.pos):
                    control_scheme = "wasd"
                    return

# ------------------ START MENU ------------------ #
def start_menu(screen):
    font_title = pygame.font.SysFont(None, 80)
    font_button = pygame.font.SysFont(None, 40)

    start_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 90, 200, 50)
    options_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 20, 200, 50)
    exit_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)

    while True:
        screen.fill(WHITE)

        title_text = font_title.render("GAME", True, BLACK)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 150))

        pygame.draw.rect(screen, GREY, start_button)
        pygame.draw.rect(screen, GREY, options_button)
        pygame.draw.rect(screen, GREY, exit_button)

        start_text = font_button.render("Start Game", True, BLACK)
        options_text = font_button.render("Options", True, BLACK)
        exit_text = font_button.render("Exit Game", True, BLACK)
        screen.blit(start_text, (start_button.x + 40, start_button.y + 10))
        screen.blit(options_text, (options_button.x + 60, options_button.y + 10))
        screen.blit(exit_text, (exit_button.x + 50, exit_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return
                elif options_button.collidepoint(event.pos):
                    options_menu()
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
