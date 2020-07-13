import pygame

class functions:
    def __init__(self, WINDOW):
        self.WINDOW = WINDOW
        
    def updateDisplay(self, background, floor):
        background.draw(self.WINDOW)
        floor.draw(self.WINDOW)
        
        pygame.display.update()
        
    def resizeImage(self, image):
        w, h = pygame.display.get_surface().get_size()
        width_ratio = w / 120
        height_ratio = h / 256
        new_width = int (image.get_size()[0] * width_ratio)
        new_height = int (image.get_size()[1] * height_ratio)
        
        return pygame.transform.scale(image, (new_width, new_height))
        
        
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
        
        return world
