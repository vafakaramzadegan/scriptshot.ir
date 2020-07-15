import pygame

class functions:
    def __init__(self, WINDOW):
        self.WINDOW = WINDOW
        self.best_score = 0
        
    def updateDisplay(self, background, floor, bird, pipes, score):
        background.draw(self.WINDOW)
        for pipe in pipes:
            pipe.draw(self.WINDOW)
        bird.draw(self.WINDOW)
        floor.draw(self.WINDOW)
        
        if score >= 0:
            if score > self.best_score:
                self.best_score = score
            score = str(score)
            best = str(self.best_score)
            
            self.WINDOW.blit(self.scoreboard, (16, 16))
            
            for index, num in enumerate(score[::-1]):
                number = self.numbers[int (num)]
                self.WINDOW.blit(number, (self.scoreboard.get_width() - 20 - (index * number.get_width()), 50))

            for index, num in enumerate(best[::-1]):
                number = self.numbers[int (num)]
                self.WINDOW.blit(number, (self.scoreboard.get_width() - 20 - (index * number.get_width()), 90))

        pygame.display.update()
        
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

    def button(self, image, x, y, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        w = image.get_width()
        h = image.get_height()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            if click[0] == 1 and action != None:
                action()
        self.WINDOW.blit(image, (x, y))

        
        
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
        # FlappyBird Message
        messages = {}
        messages['game_title'] = pygame.Surface((92, 24), pygame.SRCALPHA, 32).convert_alpha()
        messages['game_title'].blit(sprites, (0, 0), (350, 90, 440, 115))
        messages['game_title'] = self.resizeImage(messages['game_title'])
        # Gameover Message
        messages['gameover'] = pygame.Surface((96, 24), pygame.SRCALPHA, 32).convert_alpha()
        messages['gameover'].blit(sprites, (0, 0), (395, 57, 460, 100))
        messages['gameover'] = self.resizeImage(messages['gameover'])
        # Play Button
        buttons = {}
        buttons['play'] = pygame.Surface((52, 29), pygame.SRCALPHA, 32).convert_alpha()
        buttons['play'].blit(sprites, (0, 0), (354, 118, 406, 147))
        buttons['play'] = self.resizeImage(buttons['play'])
        scoreboard = pygame.Surface((113, 57), pygame.SRCALPHA, 32).convert_alpha()
        scoreboard.blit(sprites, (0, 0), (3, 259, 116, 316))
        scoreboard = pygame.transform.scale(scoreboard, (int(113*2), int (57*2)))
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

        self.numbers = numbers
        self.scoreboard = scoreboard

        return world, bird_images, messages, buttons
