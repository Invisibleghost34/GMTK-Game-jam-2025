import pygame 
from core.player import Player

#constants 
FPS = 60 

def main(): 

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    running = True 
    clock = pygame.time.Clock()
    

    player = Player(0, 0, 30, 30)

    while running:
        dt = clock.tick(FPS) / 1000 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
        screen.fill("blue")

        

        player.input_manager(dt)
        player.render(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
        main()