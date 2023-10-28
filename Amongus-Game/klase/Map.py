import pygame
from klase import Game
import random

class Map:
    
    def __init__(self, game:'Game.Game',map_images:pygame.image, x:int , y:int):
        self.game = game
        
        x += game.width/2
        y += game.height/2
        
        self.images = map_images
        self.map_image = map_images['base.png']
        
        if self.game.player.inside_ship:
            self.mask = pygame.mask.from_surface(self.images['base_collision_mask_ship.png'])
        else:
            self.mask = pygame.mask.from_surface(map_images['base_collision_mask.png'])
        self.maskrect = self.mask.get_rect()
        self.maskrect.x = x
        self.maskrect.y = y

        self.rect = pygame.Rect(0, 0, self.map_image.get_width(), self.map_image.get_height())
        self.rect.x = x
        self.rect.y = y

        self.ship_entry_rect = pygame.Rect(0, 0, 100, 100)
        self.ship_entry_rect.center = [x + 3710, y + 380]

        self.bullets = {}

        # KEYBOARD
        self.kbColldown = 20
        self.keyboard_colldown = self.kbColldown

                
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if self.ship_entry_rect.colliderect(self.game.player.rect):
            if not self.game.player.inside_ship:
                self.game.screen_message.text = self.game.FONT_ARIAL.render(f"Press E to drive ship", True, "green")
            else:
                self.game.screen_message.text = self.game.FONT_ARIAL.render(f"Press E to leave ship", True, "red")
            
            if key_pressed[pygame.K_e]:
                if self.keyboard_colldown >= self.kbColldown:
                    self.keyboard_colldown = 0
                    if self.game.player.inside_ship:
                        self.mask = pygame.mask.from_surface(self.images['base_collision_mask.png'])
                        mask_pos = [self.maskrect.x, self.maskrect.y]
                        self.maskrect = self.mask.get_rect()
                        self.maskrect.x = mask_pos[0]
                        self.maskrect.y = mask_pos[1]
                        self.game.player.movespeed = 3
                        self.game.player.inside_ship = False
                    else:
                        self.mask = pygame.mask.from_surface(self.images['base_collision_mask_ship.png'])
                        mask_pos = [self.maskrect.x, self.maskrect.y]
                        self.maskrect = self.mask.get_rect()
                        self.maskrect.x = mask_pos[0]
                        self.maskrect.y = mask_pos[1]
                        self.game.player.movespeed = 6
                        self.game.player.inside_ship = True
        else:
            self.game.screen_message.text = None

        self.keyboard_colldown += 1


    def move_map(self, x, y):
        self.rect.x += x
        self.rect.y += y
        self.maskrect.x += x
        self.maskrect.y += y
        self.ship_entry_rect.x += x
        self.ship_entry_rect.y += y

        
    def render(self):
        # --------------- MAP ---------------------
        self.game.screen.blit(self.map_image, self.rect)

        # Ship entry
        pygame.draw.rect(self.game.screen, 'red', self.ship_entry_rect, width=2, border_radius=int(self.ship_entry_rect.w/2))
        ship_txt = self.game.FONT.render(f"Ship", True, "green")
        self.game.screen.blit(ship_txt, (self.ship_entry_rect.centerx - ship_txt.get_width()/2, self.ship_entry_rect.bottom + 10))

        # Bullets
        for bullet_key in self.bullets.keys():
            x = self.bullets[bullet_key][0]
            y = self.bullets[bullet_key][1]
            cordinates = self.game.player.calculate_cords_by_my_position([x,y]) 
            bullet_rect = pygame.Rect(cordinates[0],cordinates[1], 20,20)
            if not bullet_rect.colliderect(self.rect):
                pygame.draw.rect(self.game.screen, 'red', bullet_rect,border_radius=10)

                    