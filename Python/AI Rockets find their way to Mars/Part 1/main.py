from EasyDraw import EasyDraw
from EasyDraw.Vector import *

import math, random, os

WIDTH = 800
HEIGHT = 600

IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'images/')

app_hdl = None

POPULATION_SIZE = 2
MARS_COORDS = Vector(WIDTH // 2, 60)
EARTH_COORDS = Vector(WIDTH // 2, HEIGHT + 80)
BLACKHOLES_COUNT = 3

class Population:
    def __init__(self):
        self.starships = []
        for i in range(POPULATION_SIZE):
            self.starships.append(Starship())

    def run(self):
        for s in self.starships:
            s.update()
            s.show()

class Starship:
    def __init__(self):
        self.pos = Vector(WIDTH // 2, HEIGHT - 40)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)

    def apply_force(self, force):
        self.acc += force

    def update(self):
        self.apply_force(Vector(random.uniform(-1, 1), random.uniform(-1, 1)))

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

    def show(self):
        c = app_hdl.canvas

        c.push()
        c.translate(self.pos.x, self.pos.y)
        c.rotate(self.vel.heading())
        img = 'rocket-moving.png'
        c.create_image(0, 0, IMAGE_DIR + img)
        c.pop()


def setup(app):
    global app_hdl
    app_hdl = app

    app.stars = []
    for i in range(200):
        app.stars.append([random.randint(0, WIDTH), random.randint(0, HEIGHT)])

    app.blackholes = []
    for i in range(BLACKHOLES_COUNT):
        app.blackholes.append(Vector(random.randint(100, WIDTH - 100), random.randint(300, HEIGHT - 300)))

    app.pop = Population()

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

    app.pop.run()

EasyDraw(width = WIDTH,
        height = HEIGHT,
        fps = 30,
        background = 'black',
        title = 'Starships',
        autoClear = True,
        setupFunc = setup,
        drawFunc = draw)
