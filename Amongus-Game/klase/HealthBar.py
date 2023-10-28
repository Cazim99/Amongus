import pygame
from klase import Game
from ImageLoader import ImageLoader
import os
from PIL import Image

class HealthBar:
    
    def __init__(self, game:'Game.Game', player):
        self.game = game
        self.player = player
        
        self.last_health = player.health
        
        #--- Hearth
        self.heart_image = pygame.image.load(f"{os.getcwd()}/data/player_images/health_bar/heart.png")
        #--- Background
        self.background_rect = pygame.Rect(0, 0, game.width/4 -4, 44)
        self.background_rect.center = [game.width/2 , game.height - 30]
        # -- Border
        self.border_rect = pygame.Rect(0, 0, game.width/4 , 50)
        self.border_rect.center = [game.width/2 , game.height - 30]
        pill_resized_image = Image.open(f"{os.getcwd()}/data/player_images/health_bar/health_bar_border.png").resize((int(game.width/4), 50))
        self.bar_border_image = pygame.image.fromstring(pill_resized_image.tobytes(), pill_resized_image.size, pill_resized_image.mode)
        # -- Bar
        self.rect = pygame.Rect(0, 0, game.width/4 , 50)
        self.rect.center = [game.width/2, game.height - 30]
        bar_width = self.player.health
        if self.player.health <= 0:
            bar_width = 2
        pill_resized_image = Image.open(f"{os.getcwd()}/data/player_images/health_bar/health_bar.png").resize((int((bar_width) * ((self.game.width/4)/100)), 50))
        self.bar_image = pygame.image.fromstring(pill_resized_image.tobytes(), pill_resized_image.size, pill_resized_image.mode)
        # -- Health text
        self.health_text = game.FONT_ARIAL.render(f"{player.health}%", True, "white")
        
    def update(self):
        if self.last_health != self.player.health:
            self.last_health = self.player.health
            bar_width = self.player.health
            if self.player.health <= 0:
                bar_width = 2
            pill_resized_image = Image.open(f"{os.getcwd()}/data/player_images/health_bar/health_bar.png").resize((int((bar_width) * ((self.game.width/4)/100)), 50))
            self.bar_image = pygame.image.fromstring(pill_resized_image.tobytes(), pill_resized_image.size, pill_resized_image.mode)
            self.rect.w = int((self.player.health) * ((self.game.width/4)/100))
            
            self.health_text = self.game.FONT_ARIAL.render(f"{self.player.health} %", True, "white")
        
    def render(self):
        # --- Heart
        self.game.screen.blit(self.heart_image, (self.rect.left - self.heart_image.get_width() - 10, self.rect.center[1] - self.heart_image.get_height()/2, self.heart_image.get_width(),self.heart_image.get_height()))
        # --- Background
        pygame.draw.rect(self.game.screen, "red", self.background_rect)
        # --- Bar
        self.game.screen.blit(self.bar_image, self.rect)
        # --- Border
        self.game.screen.blit(self.bar_border_image, self.border_rect)
        # --- Health text
        self.game.screen.blit(self.health_text, (self.background_rect.center[0] - self.health_text.get_width()/2, self.background_rect.center[1] - self.health_text.get_height()/2))