'''
    FlappyBird AI
    ---------------------------------
        AI plays FlappyBird using Genetic Algorithm, implemented in
        Tensorflow and Keras.

    Author:
        Scriptshot.ir
        https://github.com/vafakaramzadegan/scriptshot.ir
'''

import pygame
from functions import functions
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

'''
    init PyGame
'''
pygame.init()
clock = pygame.time.Clock()
WINDOW_WIDTH, WINDOW_HEIGHT = 420, 768
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('FlappyBird AI')

FLOOR_HEIGHT = 150

# tools for loading sprites and drawing on screen
toolkit = functions(WINDOW)

'''
    default settings for AI
'''
# number of birds in each generation
BIRDS_COUNT = 50
# number of neurons to mutate in each generation
MUTATION_RATE = .2
# draw the guide lines
SHOW_LINES = False


# the data of the best brain
BEST_BRAIN = None
# the fittness of the best bird
BEST_FITNESS = 0.0
# the index of current generation
GENERATION_INDEX = 1


'''
    Pipe object
'''
class Pipe:
    img = toolkit.sprites['world']['pipe']
    # the gap between two pipes (in pixels)
    GAP = 150
    # how fast the pipes move
    velocity = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top_pipe_top = 0
        self.bottom_pipe_top = 0

        self.PIPE_BOTTOM = self.img
        # we build the top pipe by flipping the bottom pipe
        self.PIPE_TOP = pygame.transform.flip(self.img, False, True)
        
        self.passed = False

        self.set_height()

    def set_height(self):
        # random height for pipes
        self.height = random.randrange(50, 400)
        self.top_pipe_top = self.height - self.PIPE_TOP.get_height()
        self.bottom_pipe_top = self.height + self.GAP
    
    def move(self):
        self.x -= self.velocity

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top_pipe_top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom_pipe_top))

    def collide(self, bird, window):
        # we check for collision by using masks
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top_pipe_top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom_pipe_top - round(bird.y))
        # check for overlap
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        # return True if there is a collision
        return True if b_point or t_point else False

'''
    The Brain of a bird
'''
class Brain:
    def __init__(self):
        # a Keras.Sequential model is needed for our DNN
        self.model = Sequential()
        # this is the hidden layer with four neurons.
        # we have these three inputs:
        #   1) bird's y position
        #   2) bird's vertical distance to the top pipe
        #   3) bird's vertical distance to the bottom pipe
        # so the input_shape for the hidden layer is a tensor with three elements
        self.model.add(Dense(units=4, input_shape=(3, ), activation='sigmoid'))
        # the output layer has two neurons:
        #   1) jump
        #   2) no jump
        self.model.add(Dense(units=2, activation='softmax'))

    def loadFromFile(self, fn):
        data = np.load(fn, allow_pickle=True)
        self.setData(data)

    def saveToFile(self, fn):
        np.save(fn, self.model.get_weights())

    # set the weights and biases of neurons
    def setData(self, brainData):
        brain = np.array(brainData)
        # mutation happens here
        for index, data in enumerate(brain):
            if random.uniform(0, 1) <= MUTATION_RATE:
                brain[index] = data + random.uniform(-1, 1)
        # set mutated weights
        self.model.set_weights(brain)

    def decide(self, data):
        return self.model.predict(data)

    def copy(self):
        return self.model.get_weights()

'''
    Bird object
'''
class Bird:
    img = toolkit.sprites['bird']['idle']
    crashed = False
    # number of frames it takes for the bird to change the position of its wing
    FLAPS_ANIMATION_TIME = 2
    # how fast the bird rotates
    ROTATE_VEL = 15

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick = 0
        self.frameIndex = 0
        self.vel = 0
        self.height = self.y
        self.brain = Brain()
        # indicates how long the bird survived
        self.fitness = .0

    def jump(self):
        self.vel = -8
        self.tick = 0
        self.height = self.y

    def move(self):
        self.tick += 1
        # the bird has survived for one more frame, so the fitness increases.
        # the fitness could be altered in various ways.
        self.fitness += .01

        # calculate the displacement based on the time of freefall
        self.displacement = self.vel*(self.tick) + 1.5*self.tick**2
        if self.displacement >= 16: self.displacement = (self.displacement/abs(self.displacement)) * 16
        # change the vertical position by displacement value
        self.y = self.y + self.displacement

        # bird is ascending
        if self.displacement < 0 or self.y < self.height + 50:
            if self.tilt < 25:
                self.tilt = 25
        else: # bird is descending
            if self.tilt > -90:
                self.tilt -= self.ROTATE_VEL

        # the bird crashes by moving out of the screen or hitting the floor
        if (self.y + self.img.get_height() < 0 or self.y + self.img.get_height() >= WINDOW_HEIGHT - FLOOR_HEIGHT):
            self.crashed = True

    def draw(self, window):
        self.frameIndex += 1
        if self.frameIndex < self.FLAPS_ANIMATION_TIME:
            self.img = toolkit.sprites['bird']['ascend']
        elif self.frameIndex < self.FLAPS_ANIMATION_TIME * 2:
            self.img = toolkit.sprites['bird']['idle']
        elif self.frameIndex < self.FLAPS_ANIMATION_TIME * 3:
            self.img = toolkit.sprites['bird']['descend']            
        else:
            self.frameIndex = 0

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        window.blit(rotated_image, (self.x, self.y))

    # returns the mask of the bird for detecting collisions
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

'''
    Background object
'''
class Background:
    img = toolkit.sprites['world']['background']
    width = img.get_width()
    height = img.get_height()
    # how fast the background moves
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
        # the background moves infinitely, so we need a sequence of two images
        window.blit(self.img, (self.x1, 0))
        window.blit(self.img, (self.x2, 0))

'''
    Floor object
'''     
class Floor:
    img = toolkit.sprites['world']['floor']
    width = img.get_width()
    height = img.get_height()
    # the floor moves as fast as pipes
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

'''
    The main menu
'''   
mainmenu_active = True
def mainmenu():
    WINDOW.blit(toolkit.sprites['titles']['game_title'], (WINDOW_WIDTH / 2 - toolkit.sprites['titles']['game_title'].get_width() / 2, 100))
    WINDOW.blit(toolkit.sprites['titles']['scriptshot'], (WINDOW_WIDTH / 2 - toolkit.sprites['titles']['scriptshot'].get_width() / 2, 180))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # play button
        toolkit.button(toolkit.sprites['buttons']['play'],
               WINDOW_WIDTH / 2 - toolkit.sprites['buttons']['play'].get_width() / 2,
               300,
               close_mainmenu)

        pygame.display.update()
        clock.tick(30) 

def close_mainmenu():
    global mainmenu_active
    mainmenu_active = False
    run()

'''
    the main function
'''
def run():
    global BEST_BRAIN, BEST_FITNESS, GENERATION_INDEX

    # the number of pipes passed in the current generation
    score = 0

    # objects
    background = Background()
    floor = Floor()
    birds = []
    pipes = [Pipe(500)]

    # all the birds in a generation have the same random starting position
    startPosX = random.randint(20, 100)
    startPosY = random.randint(20, WINDOW_HEIGHT - FLOOR_HEIGHT - 40)
    for i in range(BIRDS_COUNT):
        bird = Bird(startPosX, startPosY)
        if BEST_BRAIN is not None: bird.brain.setData(BEST_BRAIN)
        birds.append(bird)
    
    while True:
        clock.tick(30)

        # the last alive bird in a generation is the best one
        if len(birds) == 1:
            if birds[0].fitness > BEST_FITNESS:
                BEST_FITNESS = birds[0].fitness
                BEST_BRAIN = birds[0].brain.copy()
        # the current generation went extinct, and the next one
        # must start
        elif len(birds) == 0:
            GENERATION_INDEX += 1
            run()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
 
        floor.move()
        background.move()

        pipe_ind = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1 

        for x, bird in enumerate(birds):
            bird.move()
            # bird decides whether to jump or not
            res = bird.brain.decide([[bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom_pipe_top)]])
            # the first output neuron represents jump action
            if np.argmax(res) == 0: bird.jump()

        add_pipe = False

        pipes_to_remove = []
        for pipe in pipes:
            pipe.move()
            for bird in birds:
                if (bird.crashed or pipe.collide(bird, WINDOW)):
                    # remove crashed birds
                    birds.pop(birds.index(bird))
            # a pipe is destroyed after moving out of screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes_to_remove.append(pipe)
            # add new pipe if the current one has been passed by the birds
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        for r in pipes_to_remove:
            pipes.remove(r)

        if add_pipe:
            score += 1
            pipes.append(Pipe(WINDOW_WIDTH))

        toolkit.updateDisplay(background, floor, birds, pipes, score, not mainmenu_active, pipe_ind, GENERATION_INDEX, SHOW_LINES)
        
        if mainmenu_active:
            mainmenu()



if __name__ == '__main__':
    run()
