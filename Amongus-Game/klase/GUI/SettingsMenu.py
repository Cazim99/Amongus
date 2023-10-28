import pygame
from klase import Game
from ImageLoader import ImageLoader
import os
from klase.GUI.Button import Button
import configparser

class SettingsMenu:
    
    def __init__(self, root:'Game.Game', x, y):
        self.root = root

        self.images = ImageLoader.load_images(f"{os.getcwd()}/data/gui_images/menu/")
        self.bg_image = pygame.transform.scale(self.images['background.png'], (self.root.width/2, self.root.height/2))

        self.x = x
        self.y = y

        self.disabled = False
        self.active = False

        self.color = "white"
        self.title = root.FONT.render(f"Settings", True, self.color)

        self.rect = pygame.Rect(0, 0, self.bg_image.get_width(), self.bg_image.get_height())
        self.rect.center = [x, y]
        
        text = 'Sound on'
        color = 'green'
        if self.root.soundOn == True:
            text = 'Sound off'
            color = 'red'

        self.sound_on_off_btn = Button(root, self.rect.center[0], self.rect.center[1] - self.rect.h/8, text=text, color=color)

        text = 'Fullscreen on'
        color = 'green'
        if self.root.full_screen == True:
            text = 'Fullscreen off'
            color = 'red'

        self.fullscreen_on_off_btn = Button(root, self.rect.center[0], self.rect.center[1] + self.sound_on_off_btn.rect.h, text=text, color=color)

    def save_settings(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        config.set('settings', 'full_screen','True' if self.root.full_screen else 'False')
        config.set('settings', 'sound_on','True' if self.root.soundOn else 'False')

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def pressed(self):
        self.current_image = self.images['button_pressed.png']
        
    def unpressed(self):
        self.current_image = self.images['button.png']

    def mouse_events(self):
        self.root.cursor = self.root.cursor_images['cursor.png']
        if self.root.cursor_pos.colliderect(self.sound_on_off_btn.rect) or self.root.cursor_pos.colliderect(self.fullscreen_on_off_btn.rect):
            self.root.cursor = self.root.cursor_images['cursor_click.png']
       
    def render(self):
        if not self.disabled and self.active:
            self.root.screen.blit(self.bg_image, self.rect)
            self.root.screen.blit(self.title, (self.x - self.title.get_width()/2, self.rect.y + self.title.get_height() * 3)) 

            self.sound_on_off_btn.render()
            self.fullscreen_on_off_btn.render()