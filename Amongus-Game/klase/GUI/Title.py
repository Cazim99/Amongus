import pygame
import os

class Title:
    
    def __init__(self, root, x, y, text, color="white"):
        self.root = root
        self.x = x
        self.y = y
        self.color = color
        self.text = root.BIG_FONT.render(f"{text}", True, color)
        self.brandImage = pygame.image.load(f"{os.getcwd()}/data/gui_images/brand.png")
        self.brandImageRect = pygame.Rect((x-self.text.get_width()/2)-self.brandImage.get_width()/2, 
                                           y-self.text.get_height()/2, 
                                           self.brandImage.get_width(), 
                                           self.brandImage.get_height())
        
        
    def render(self):
        self.root.screen.blit(self.brandImage, self.brandImageRect) 
        self.root.screen.blit(self.text, ((self.x - self.text.get_width()/2) + self.brandImage.get_width()/2, self.y)) 