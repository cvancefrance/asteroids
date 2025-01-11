import pygame
from circleshape import CircleShape
from constants import SHIELD_RADIUS

class Shield(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHIELD_RADIUS)
        self.active = False
        self.tier = 1

    def draw(self, screen):
        if self.active:
            if self.tier == 1:
                color = "red"
            elif self.tier == 2:
                color = "blue"
            else:  # tier 3
                color = "green"
                
            pygame.draw.circle(screen, color, self.position, self.radius, 2)
        
