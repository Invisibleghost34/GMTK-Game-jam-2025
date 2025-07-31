import pygame, sys 
from pathfinding.core.grid import Grid 
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from core.maze_generator import * 
from core.player import *

player = Player(0,0,30,140)

class Enemy: 
    def __init__(self, x, y, size, speed,):
        self.pos = pygame.Vector2(x,y)
        self.size = size 
        self.speed = speed 
        self.color = (255,0,0)
        #path 
        self.path = []
        self.path_index = 0 
        self.direction = pygame.Vector2(0,0)
        self.tile_size = size 

    def set_path(self,path):
        self.path = path 
        self.path_index=0
        self.get_direction()

    
 
    def get_direction(self):
        if self.path_index >= len(self.path):
            self.direction = pygame.Vector2(0,0)
            return
        target_tile = self.path[self.path_index]
        target_pos = pygame.Vector2(
            target_tile[0] * self.tile_size + self.tile_size // 2, 
            target_tile[1] * self.tile_size + self.tile_size // 2
        )

        diff = target_pos - self.pos
        if diff.length() > 0: 
            self.direction = diff.normalize()
        else:
            self.direction = pygame.Vector2(0,0)
        

    def update_position(self, dt):
        if self.path_index >= len(self.path):
            return
        target_tile = self.path[self.path_index]
        target_pos = pygame.Vector2(
            target_tile[0] * self.tile_size + self.tile_size // 2,
            target_tile[1] * self.target_tile + self.tile_size //2
        )

        move = self.direction * self.speed * dt 
        distance = (target_pos - self.pos).length()

        if move.length() >= distance: 
            self.pos = target_pos 
            self.path_index += 1 
            self.get_direction()
        else: 
            self.pos += move
        

    def draw_enemy(self, surface): 
        pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, self.size, self.size))

enemy = Enemy(10,10,30,140)
        
class Pathfinder: 
    def __init__(self, matrix):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        
        self.path = []

    def empty_path(self): 
        self.path = []

    def create_path(self):
        #Starting coordinate 
        start_x, start_y = player.pos.x, player.pos.y 
        start = self.grid.node(start_x, start_y)
        #End coordinate 
        end_x, end_y = enemy.pos.x, enemy.pos.y 
        end = self.grid.node(end_x, end_y)
        #path
        finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
        self.path = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        
