import pygame 

clock = pygame.time.Clock()



class Player: 
    def __init__(self, x, y, size, speed, color=(0, 255,0)):
        self.pos = pygame.Vector2(x,y)
        self.size = size 
        self.speed = speed 
        self.color = color 
    
    def input_manager(self, dt):
        keys = pygame.key.get_pressed()
        position = pygame.Vector2(0,0)

        if keys[pygame.K_UP]:
            position.y -= 1
        if keys[pygame.K_DOWN]: 
            position.y += 1
        if keys[pygame.K_LEFT]:
            position.x -= 1
        if keys[pygame.K_RIGHT]:
            position.x += 1

        self.pos += position * self.speed * dt
    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, self.size, self.size))