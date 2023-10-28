from klase import Game
import pygame
import os
from pygame import mixer
import configparser

class Intro:
    
    def __init__(self, game:'Game.Game'):
        self.game = game

        self.intro_channel = pygame.mixer.Channel(3)
        self.intro_sound = mixer.Sound(f"{os.getcwd()}/data/sounds/intro_voice.mp3")

        self.typing_channel = pygame.mixer.Channel(4)
        self.typing_sound = mixer.Sound(f"{os.getcwd()}/data/sounds/intro_typing.mp3")
        
        self.typing_sound.set_volume(0.1)
        
        self.full_speach = """Ten years ago the earth lost its protective shell completely@ there was no longer any possible life, we had to leave the earth as soon as possible @ building a base with which we can survive in space for a long time until we find a new planet for life...@ Space has become dangerous place for us, the only place where we feel safe is the base where you just arrived (The skeld)@ it has a protective cover and a very advanced defense system. @########## If you leave the base, be careful of the people AMONGUS#########################################################"""
        self.last_text = ""
        self.char_index = 0
        
        self.animation_colldown = 0.0
        self.anim_speed = 3.8
        
        self.x = 20
        self.y = game.height/2
        
        self.text = game.BIG_FONT.render(f"", True, "green")
        
        self.show = False
        
    def update_animation(self):
        if self.show:
            if self.animation_colldown >= self.anim_speed:
                self.animation_colldown = 0
                
                #if not self.typing_channel.get_busy() and self.game.soundOn:
                #    self.typing_channel.play(self.typing_sound)
                
                if self.full_speach[self.char_index] == '@': # '@' Clear text
                    self.last_text = ""
                elif self.full_speach[self.char_index] == '#': # '#' Pause
                    self.typing_sound.stop()
                else:
                    self.text = self.game.BIG_FONT.render(f"{self.last_text}{self.full_speach[self.char_index]}", True, "green")
                    self.last_text += self.full_speach[self.char_index]
                
                if self.text.get_width() >= self.game.width - 40:
                    self.last_text = " "
                    
                self.char_index += 1
                if self.char_index >= len(self.full_speach):
                    self.show = False
                    self.game.first_time_run = False
                    config = configparser.ConfigParser()
                    config.read('config.ini')
                    config.set('settings', 'first_time_run','False')

                    with open('config.ini', 'w') as configfile:
                        config.write(configfile)
                    
                    #self.game.screen_animation.anim = self.game.screen_animation.anims['first_time_run']
                
            self.animation_colldown += 1.0
    
    def save_settings(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        config.set('settings', 'full_screen','True' if self.root.full_screen else 'False')
        config.set('settings', 'sound_on','True' if self.root.soundOn else 'False')

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def update(self):
        self.update_animation()
        
    def render(self):
        if self.show:
            self.game.screen.fill("black")
            self.game.screen.blit(self.text, (self.x, self.y))    
    