import pygame 
from core.player import Player
from core.maze_generator import *
from core.pathfinding import * 
import pickle


#constants 
FPS = 60 

def main(): 

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    running = True 
    clock = pygame.time.Clock()
    

    player = Player(0, 0, 30, 140)
    DFS_backtracking(grid[0][0])
    maze_data = save_maze(grid)
    enemy = Enemy(10,10,30,150)
    pathfinder = Pathfinder(matrix)

    with open('maze.pkl', 'wb') as file:
        pickle.dump(maze_data, file)
    


    while running:
        dt = clock.tick(FPS) / 1000 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
        screen.fill("blue")
        draw_grid()
        enemy.set_path(pathfinder.path)

        enemy.update_position(dt)
        enemy.draw_enemy(screen)


        player.input_manager(dt)
        player.render(screen)
        


        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
        main()