import pygame
import os
from PIL import Image, ImageSequence

class functions:
    def __init__(self, WINDOW):
        self.WINDOW = WINDOW
        self.best_score = 0
        self.loadSprites(os.path.join(os.path.dirname(__file__), 'data', 'sprites.png'))

    # updates game screen    
    def updateDisplay(self, background, floor, birds, pipes, score, show_scores, pipe_ind, generation_index, draw_line):
        # draw background
        background.draw(self.WINDOW)
        # draw pipes
        for pipe in pipes:
            pipe.draw(self.WINDOW)
        # draw floor
        floor.draw(self.WINDOW)
        # draw birds
        for bird in birds:
            # draw guid lines
            if draw_line:
                try:
                    pygame.draw.line(self.WINDOW, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 2)
                    pygame.draw.line(self.WINDOW, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom_pipe_top), 2)
                except:
                    pass
            bird.draw(self.WINDOW)
        # show information on screen
        if show_scores:

            self.WINDOW.blit(self.sprites['titles']['scores'], (16, self.WINDOW.get_height() - self.sprites['titles']['scores'].get_height() - 16))
            self.WINDOW.blit(self.sprites['titles']['gen'], (240, self.WINDOW.get_height() - self.sprites['titles']['gen'].get_height() - 16))
            self.WINDOW.blit(self.sprites['titles']['alive'], (240, self.WINDOW.get_height() - self.sprites['titles']['scores'].get_height() - 24))

            if score > self.best_score:
                self.best_score = score
            score = str(score)
            best = str(self.best_score)

            for index, num in enumerate(score):
                number = self.sprites['numbers'][int (num)]
                self.WINDOW.blit(number, (128 + (index * number.get_width()), self.WINDOW.get_height() - self.sprites['titles']['scores'].get_height() - 18))

            for index, num in enumerate(best):
                number = self.sprites['numbers'][int (num)]
                self.WINDOW.blit(number,  (128 + (index * number.get_width()), self.WINDOW.get_height() - self.sprites['titles']['scores'].get_height() + 16))

            for index, num in enumerate(str(generation_index)):
                number = self.sprites['numbers'][int (num)]
                self.WINDOW.blit(number, (320 + (index * number.get_width()), self.WINDOW.get_height() - self.sprites['titles']['scores'].get_height() + 16))

            for index, num in enumerate(str(len(birds))):
                number = self.sprites['numbers'][int (num)]
                self.WINDOW.blit(number, (350 + (index * number.get_width()), self.WINDOW.get_height() - self.sprites['titles']['scores'].get_height() - 20))

        pygame.display.update()

    # resize sprite based on screen size. also keep aspect ratio
    def resizeImage(self, image, ratio=1):
        w, h = pygame.display.get_surface().get_size()
        if ratio == 1:
            width_ratio = w / 120
            height_ratio = h / 256
        else:
            width_ratio = ratio
            height_ratio = ratio
        new_width = int (image.get_size()[0] * width_ratio)
        new_height = int (image.get_size()[1] * height_ratio)
        
        return pygame.transform.scale(image, (new_width, new_height))

    # a method for handling button click
    def button(self, image, x, y, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        w = image.get_width()
        h = image.get_height()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            if click[0] == 1 and action != None:
                action()
        self.WINDOW.blit(image, (x, y))

    # loads sprites from png file 
    def loadSprites(self, path):
        sprites = pygame.image.load(path).convert_alpha()
        
        world = {}
        # Background Image
        world['background'] = pygame.Surface((140, 256))
        world['background'].blit(sprites, (0, 0), (0, 0, 140, 256))
        world['background'] = self.resizeImage(world['background'])
        # Floor Image
        world['floor'] = pygame.Surface((145, 56))
        world['floor'].blit(sprites, (0, 0), (292, 0, 432, 56))
        world['floor'] = self.resizeImage(world['floor'])
        # Pipe Image
        world['pipe'] = pygame.Surface((26, 160), pygame.SRCALPHA, 32).convert_alpha()
        world['pipe'].blit(sprites, (0, 0), (84, 323, 110, 483))
        world['pipe'] = self.resizeImage(world['pipe'])
        # Bird Images (Descending, Idle and Ascending)
        bird_images = {}
        bird_images['descend'] = pygame.Surface((20, 14), pygame.SRCALPHA, 32).convert_alpha()
        bird_images['descend'].blit(sprites, (0, 0), (1, 490, 20, 504))
        bird_images['descend'] = self.resizeImage(bird_images['descend'])
        bird_images['idle'] = pygame.Surface((20, 14), pygame.SRCALPHA, 32).convert_alpha()
        bird_images['idle'].blit(sprites, (0, 0), (29, 490, 48, 504))
        bird_images['idle'] = self.resizeImage(bird_images['idle'])
        bird_images['ascend'] = pygame.Surface((20, 14), pygame.SRCALPHA, 32).convert_alpha()
        bird_images['ascend'].blit(sprites, (0, 0), (57, 490, 76, 504))
        bird_images['ascend'] = self.resizeImage(bird_images['ascend'])
        # Titles
        titles = {}
        titles['game_title'] = pygame.Surface((125, 24), pygame.SRCALPHA, 32).convert_alpha()
        titles['game_title'].blit(sprites, (0, 0), (350, 90, 475, 115))
        titles['game_title'] = self.resizeImage(titles['game_title'], 3)
        titles['scriptshot'] = pygame.Surface((103, 14), pygame.SRCALPHA, 32).convert_alpha()
        titles['scriptshot'].blit(sprites, (0, 0), (395, 168, 498, 182))
        titles['scriptshot'] = self.resizeImage(titles['scriptshot'], 2)
        titles['scores'] = pygame.Surface((65, 33), pygame.SRCALPHA, 32).convert_alpha()
        titles['scores'].blit(sprites, (0, 0), (366, 212, 431, 245))
        titles['scores'] = self.resizeImage(titles['scores'], 1.6)
        titles['gen'] = pygame.Surface((45, 14), pygame.SRCALPHA, 32).convert_alpha()
        titles['gen'].blit(sprites, (0, 0), (366, 256, 411, 270))
        titles['gen'] = self.resizeImage(titles['gen'], 1.6)
        titles['alive'] = pygame.Surface((65, 15), pygame.SRCALPHA, 32).convert_alpha()
        titles['alive'].blit(sprites, (0, 0), (366, 282, 431, 297))
        titles['alive'] = self.resizeImage(titles['alive'], 1.6)
        # Play Button
        buttons = {}
        buttons['play'] = pygame.Surface((52, 29), pygame.SRCALPHA, 32).convert_alpha()
        buttons['play'].blit(sprites, (0, 0), (354, 118, 406, 147))
        buttons['play'] = self.resizeImage(buttons['play'])
        # Numbers
        numbers = {}
        numbers[0] = pygame.Surface((7, 10), pygame.SRCALPHA, 32).convert_alpha()
        numbers[0].blit(sprites, (0, 0), (137, 306, 144, 316))
        numbers[0] = self.resizeImage(numbers[0], 2)
        numbers[1] = pygame.Surface((7, 10), pygame.SRCALPHA, 32).convert_alpha()
        numbers[1].blit(sprites, (0, 0), (137, 477, 144, 488))
        numbers[1] = self.resizeImage(numbers[1], 2)
        numbers[2] = pygame.Surface((7, 10), pygame.SRCALPHA, 32).convert_alpha()
        numbers[2].blit(sprites, (0, 0), (137, 489, 144, 499))
        numbers[2] = self.resizeImage(numbers[2], 2)
        numbers[3] = pygame.Surface((7, 10), pygame.SRCALPHA, 32).convert_alpha()
        numbers[3].blit(sprites, (0, 0), (131, 501, 138, 511))
        numbers[3] = self.resizeImage(numbers[3], 2)   
        numbers[4] = pygame.Surface((7, 10), pygame.SRCALPHA, 32).convert_alpha()
        numbers[4].blit(sprites, (0, 0), (502, 0, 509, 10))
        numbers[4] = self.resizeImage(numbers[4], 2)   
        numbers[5] = pygame.Surface((7, 10), pygame.SRCALPHA, 32).convert_alpha()
        numbers[5].blit(sprites, (0, 0), (502, 12, 509, 22))
        numbers[5] = self.resizeImage(numbers[5], 2)      
        numbers[6] = pygame.Surface((7, 10), pygame.SRCALPHA, 32).convert_alpha()
        numbers[6].blit(sprites, (0, 0), (505, 26, 512, 36))
        numbers[6] = self.resizeImage(numbers[6], 2) 
        numbers[7] = pygame.Surface((7, 10), pygame.SRCALPHA, 32).convert_alpha()
        numbers[7].blit(sprites, (0, 0), (505, 42, 512, 52))
        numbers[7] = self.resizeImage(numbers[7], 2) 
        numbers[8] = pygame.Surface((7, 10), pygame.SRCALPHA, 32).convert_alpha()
        numbers[8].blit(sprites, (0, 0), (293, 242, 300, 252))
        numbers[8] = self.resizeImage(numbers[8], 2) 
        numbers[9] = pygame.Surface((7, 10), pygame.SRCALPHA, 32).convert_alpha()
        numbers[9].blit(sprites, (0, 0), (311, 206, 318, 216))
        numbers[9] = self.resizeImage(numbers[9], 2)

        self.sprites = {'world': world, 'bird': bird_images, 'titles': titles, 'buttons': buttons, 'numbers': numbers}

        return True
