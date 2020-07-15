# Tutorial Video available on: https://www.aparat.com/v/OI123
    
import pygame
from functions import functions
import os

pygame.init()
clock = pygame.time.Clock()

WINDOW_WIDTH, WINDOW_HEIGHT = 420, 768
FLOOR_HEIGHT = 150

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird')

toolkit = functions(WINDOW)

world = toolkit.loadSprites(os.path.join('data', 'sprites.png'))


class Background:
    img = world['background']
    width = img.get_width()
    height = img.get_height()
    velocity = 1
    
    def __init__(self):
        self.x1 = 0
        self.x2 = self.width
        
    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, window):
        window.blit(self.img, (self.x1, 0))
        window.blit(self.img, (self.x2, 0))
        
class Floor:
    img = world['floor']
    width = img.get_width()
    height = img.get_height()
    velocity = 5
    
    def __init__(self):
        self.x1 = 0
        self.x2 = self.width
        
    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width        
        
    def draw(self, window):
        window.blit(self.img, (self.x1, WINDOW_HEIGHT - FLOOR_HEIGHT))
        window.blit(self.img, (self.x2, WINDOW_HEIGHT - FLOOR_HEIGHT))

def run():
    background = Background()
    floor = Floor()
    
    while True:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        floor.move()
        background.move()
                
        toolkit.updateDisplay(background, floor)
                
                
if __name__ == '__main__':
    run()
