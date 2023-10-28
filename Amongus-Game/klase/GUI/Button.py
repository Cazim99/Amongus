import pygame
from pygame import mixer
from klase import Game
from ImageLoader import ImageLoader
import os


class Button:
    
    def __init__(self, root:'Game.Game', x, y, text, color="white"):
        self.root = root
        self.id = text

        self.click_channel = pygame.mixer.Channel(6)
        self.click_sound = mixer.Sound(f"{os.getcwd()}/data/sounds/button_click.wav")

        self.disabled = False

        self.images = ImageLoader.load_images(f"{os.getcwd()}/data/gui_images/button/")
        self.current_image = self.images['button.png']

        self.x = x
        self.y = y

        self.color = color
        self.text = root.FONT.render(f"{text}", True, color)

        self.rect = pygame.Rect(0,0, self.images['button.png'].get_width(), self.images['button.png'].get_height())
        self.rect.center = [x, y]
    
    
    def pressed(self):
        if not self.click_channel.get_busy() and self.root.soundOn and self.disabled == False:
            self.click_channel.play(self.click_sound)
        self.current_image = self.images['button_pressed.png']
        
    def unpressed(self):
        self.current_image = self.images['button.png']
       
    def render(self):
        if not self.disabled:
            self.root.screen.blit(self.current_image, self.rect)
            self.root.screen.blit(self.text, (self.x - self.text.get_width()/2, self.y - self.text.get_height()/2)) 