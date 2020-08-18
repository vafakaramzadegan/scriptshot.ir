import pygame
from functions import functions
import os
import random

pygame.init()
clock = pygame.time.Clock()

WINDOW_WIDTH, WINDOW_HEIGHT = 420, 768
FLOOR_HEIGHT = 150

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird')

toolkit = functions(WINDOW)

world, bird_images, messages, buttons = toolkit.loadSprites(os.path.join('data', 'sprites.png'))

class Pipe:
    img = world['pipe']
    GAP = 200
    velocity = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_BOTTOM = self.img
        self.PIPE_TOP = pygame.transform.flip(self.img, False, True)

        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 400)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.velocity

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, window):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        if b_point or t_point:
            return True
        return False

class Bird:
    img = bird_images['idle']
    crashed = False
    FLAPS_ANIMATION_TIME = 5
    ROTATE_VEL = 15

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick = 0
        self.frameIndex = 0
        self.vel = 0
        self.height = self.y

    def jump(self):
        self.vel = -8
        self.tick = 0
        self.height = self.y

    def move(self):
        self.tick += 1

        displacement = self.vel*(self.tick) + 1.5*self.tick**2

        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < 25:
                self.tilt = 25
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATE_VEL

        if self.y + self.img.get_height() >= WINDOW_HEIGHT - FLOOR_HEIGHT:
            self.crashed = True

    def draw(self, window):
        self.frameIndex += 1

        if self.crashed:
            self.img = bird_images['idle']
        else:
            if self.frameIndex < self.FLAPS_ANIMATION_TIME:
                self.img = bird_images['ascend']
            elif self.frameIndex < self.FLAPS_ANIMATION_TIME * 2:
                self.img = bird_images['idle']
            elif self.frameIndex < self.FLAPS_ANIMATION_TIME * 3:
                self.img = bird_images['descend']            
            else:
                self.frameIndex = 0

        rotated_image = pygame.transform.rotate(self.img, self.tilt)

        window.blit(rotated_image, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

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

def gameover():
    WINDOW.blit(messages['game_title'], (WINDOW_WIDTH / 2 - messages['game_title'].get_width() / 2, 100))
    WINDOW.blit(messages['gameover'], (WINDOW_WIDTH / 2 - messages['gameover'].get_width() / 2, 180))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        toolkit.button(buttons['play'], WINDOW_WIDTH/2 - buttons['play'].get_width()/2, 350, run)

        pygame.display.update()
        clock.tick(30)

mainmenu_active = True

def mainmenu():
    WINDOW.blit(messages['game_title'], (WINDOW_WIDTH / 2 - messages['game_title'].get_width() / 2, 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        toolkit.button(buttons['play'],
               WINDOW_WIDTH / 2 - buttons['play'].get_width() / 2,
               300,
               close_mainmenu)

        pygame.display.update()
        clock.tick(30) 

def close_mainmenu():
    global mainmenu_active
    mainmenu_active = False
    run()

def run():
    score = 0

    background = Background()
    floor = Floor()
    bird = Bird(40, 200)
    pipes = [Pipe(500)]
    
    while True:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        if bird.crashed:
            gameover()
        else:   
            floor.move()
            background.move()
            bird.move()
            add_pipe = False
            for pipe in pipes:
                pipe.move()
                if pipe.collide(bird, WINDOW):
                    gameover()
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            
        if add_pipe:
            score += 1
            pipes.append(Pipe(WINDOW_WIDTH))

        if mainmenu_active:
            toolkit.updateDisplay(background, floor, bird, pipes, -1)
            mainmenu()
        else:
            toolkit.updateDisplay(background, floor, bird, pipes, score)
                
                
if __name__ == '__main__':
    run()
