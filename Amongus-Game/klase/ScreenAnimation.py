from klase import Game
import pygame

class ScreenAnimation:
    
    def __init__(self, game:'Game.Game', images, anim_speed = 7):
        self.game = game
        self.images = images
        
        # ANIMS
        self.anims ={
            'weakup':['weakup1.png','weakup2.png','weakup1.png','weakup1.png'],
            'first_time_run':['first_time_run.png','first_time_run2.png','first_time_run.png'],
        }
        
        # ANIMATION
        self.anim = None
        self.current_image = 'weakup1.png'
        self.anim_index = 0 
        self.anim_speed = anim_speed 
        self.animation_colldown = 0 
        
        self.rect = pygame.Rect(0, 0, game.width, game.height)
        
    def update_animation(self):
        if self.animation_colldown >= self.anim_speed:
            self.animation_colldown = 0
            self.anim_index += 1
            if self.anim_index >= len(self.anim): 
                self.anim_index = 0
            
            if self.anim != None:
                self.current_image = self.anim[self.anim_index]
                
        self.animation_colldown += 1 
    
    def update(self):
        if self.anim != None:
            self.update_animation()
        
    def render(self):
        if self.anim != None:
            self.game.screen.blit(self.images[self.current_image], self.rect)