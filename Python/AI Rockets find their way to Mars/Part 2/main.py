from EasyDraw import EasyDraw
from EasyDraw.Vector import *

from EasyDraw.Tools import *

import math, random, os

WIDTH = 800
HEIGHT = 600

IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'images/')

app_hdl = None

POPULATION_SIZE = 10
MARS_COORDS = Vector(WIDTH // 2, 60)
EARTH_COORDS = Vector(WIDTH // 2, HEIGHT + 80)
BLACKHOLES_COUNT = 3

STARSHIP_LIFESPAN = 200
MUTATION_RATE = .1

class Population:
    def __init__(self):
        self.starships = []
        self.mating_pool = []
        for i in range(POPULATION_SIZE):
            self.starships.append(Starship())

    def run(self):
        for s in self.starships:
            s.update()
            s.show()

    def evaluate(self):
        max_fitness = 0
        for i in range(0, POPULATION_SIZE):
            self.starships[i].calc_fitness()
            if self.starships[i].fitness > max_fitness:
                max_fitness = self.starships[i].fitness
        
        if max_fitness == 0: max_fitness = 1

        for i in range(0, POPULATION_SIZE):
            self.starships[i].fitness /= max_fitness

        self.mating_pool = []
        for i in range(0, POPULATION_SIZE):
            n = math.ceil(self.starships[i].fitness * 100)
            if n > 0:
                for j in range(0, n):
                    self.mating_pool.append(self.starships[i])

    def selection(self):
        new_starships = []
        for i in self.starships:
            parent_a = random.choice(self.mating_pool).dna
            parent_b = random.choice(self.mating_pool).dna
            child = parent_a.crossover(parent_b)
            child.mutation()
            new_starships.append(Starship(child))
        self.starships = new_starships

class DNA:
    def __init__(self, genes=None):
        if genes != None:
            self.genes = genes
        else:
            self.genes = []
            for i in range(0, STARSHIP_LIFESPAN):
                self.genes.append(RandomVector())
    
    def crossover(self, parent_b):
        new_genes = []
        mid_point = math.floor(random.randint(0, len(self.genes)))
        for i in range(0, len(self.genes)):
            if i > mid_point:
                new_genes.append(self.genes[i])
            else:
                new_genes.append(parent_b.genes[i])
        return DNA(new_genes)

    def mutation(self):
        for i in range(0, len(self.genes)):
            if random.randint(1, 100) < MUTATION_RATE * 100:
                self.genes[i] = RandomVector()

class Starship:
    def __init__(self, dna=None):
        self.pos = Vector(WIDTH // 2, HEIGHT - 40)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)

        self.reached = False
        self.crashed = False
        self.alive_tick = 0

        if dna == None:
            self.dna = DNA()
        else:
            self.dna = dna

        self.fitness = 0

    def apply_force(self, force):
        self.acc += force

    def update(self):
        dist = self.pos.distance_from(MARS_COORDS)
        self.alive_tick += 1

        if dist < 80:
            self.reached = True
            self.pos = MARS_COORDS

        for bh in app_hdl.blackholes:
            if self.pos.distance_from(bh) < 60:
                self.crashed = True

        if self.pos.x > WIDTH or self.pos.x < 0 or self.pos.y > HEIGHT or self.pos.y < 0:
            self.crashed = True

        self.apply_force(self.dna.genes[app_hdl.cnt])

        if self.reached == False:
            self.vel += self.acc
            self.pos += self.vel
            self.acc *= 0

    def calc_fitness(self):
        dist = self.pos.distance_from(MARS_COORDS)
        self.fitness = map(dist, 0, WIDTH, WIDTH, 0)
        if self.reached:
            self.fitness *= 20
        if self.crashed:
            self.fitness /= 10
        self.fitness *= self.alive_tick

    def show(self):
        if self.crashed:
            return

        c = app_hdl.canvas

        c.push()
        c.translate(self.pos.x, self.pos.y)
        c.rotate(self.vel.heading())

        if self.vel.length() < 1 or self.reached:
            img = 'rocket-idle.png'
        else:
            img = 'rocket-moving.png'

        c.create_image(0, 0, IMAGE_DIR + img)
        c.pop()


def setup(app):
    global app_hdl
    app_hdl = app

    app.cnt = 0

    app.stars = []
    for i in range(200):
        app.stars.append([random.randint(0, WIDTH), random.randint(0, HEIGHT)])

    app.blackholes = []
    for i in range(BLACKHOLES_COUNT):
        app.blackholes.append(Vector(random.randint(100, WIDTH - 100), random.randint(300, HEIGHT - 300)))

    app.pop = Population()

    app.generation_index = 1
    app.canvas.font_family('Tahoma 14')
    app.canvas.font_color('white')
    app.canvas.text_anchor('sw')

def draw(app):
    c = app.canvas

    for star in app.stars:
        c.point(star[0], star[1], 'white')

    for bh in app.blackholes:
        c.push()
        c.translate(bh.x, bh.y)
        c.rotate(app.tick/2)
        c.create_image(0, 0, IMAGE_DIR + 'blackhole.png')
        c.pop()

    c.create_image(EARTH_COORDS, IMAGE_DIR + 'earth.png', scale=.7)
    c.create_image(MARS_COORDS, IMAGE_DIR + 'mars.png', scale=.5)
    
    c.push()
    c.translate(EARTH_COORDS.x, EARTH_COORDS.y)
    c.rotate(-app.tick/2)
    c.create_image(250, 0, IMAGE_DIR + 'moon.png', scale=.2)
    c.pop()

    c.text(16, HEIGHT - 16, f'Generation: {app.generation_index}')

    app.pop.run()

    crashed = 0
    for ship in app.pop.starships:
        if ship.crashed:
            crashed += 1

    app.cnt += 1
    if app.cnt >= STARSHIP_LIFESPAN or crashed == POPULATION_SIZE:
        app.pop.evaluate()
        app.pop.selection()
        app.generation_index += 1
        app.cnt = 0

EasyDraw(width = WIDTH,
        height = HEIGHT,
        fps = 30,
        background = 'black',
        title = 'Starships',
        autoClear = True,
        setupFunc = setup,
        drawFunc = draw)
