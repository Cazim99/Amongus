import pygame
import os
from PIL import Image

class Message:
    
    def __init__(self, root, x, y):
        self.root = root
        self.x = x
        self.y = y
        self.text = None
        
    def render(self):
        try:
            if self.text != None and self.text.get_width() > 1:
                pill_resized_image = Image.open(f"{os.getcwd()}/data/gui_images/message_bg.png").resize((self.text.get_width(), self.text.get_height()))
                message_bg = pygame.image.fromstring(pill_resized_image.tobytes(), pill_resized_image.size, pill_resized_image.mode)
                self.root.screen.blit(message_bg, ((self.x - message_bg.get_width()/2),self.y, message_bg.get_width(), message_bg.get_height()))
                self.root.screen.blit(self.text, (self.x - self.text.get_width()/2, self.y)) 
        except:
            pass