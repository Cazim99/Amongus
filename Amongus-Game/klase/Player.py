from klase import Game
from . import Map
import math
import pygame
import copy
import os
from pygame import mixer
from .HealthBar import HealthBar

class Player:
    
    def __init__(self, game:'Game.Game' , images:pygame.image, camx:int, camy:int, users, inside_ship:bool, health:int, movespeed:int, anim_speed=5, playing=True, inhospital=False):
        
        self.game = game
        self.images = images
        self.laying = 'laying.png'
        self.current_image = 'idle.png' 
        self.idle_image = f'idle.png'
        self.walk_images_list = [f'walkcolor{str(i).zfill(4)}.png' for i in range(1,13)]
        self.dead_images_list = [f'Dead{str(i).zfill(4)}.png' for i in range(1,33)]
        self.spawn_images_list = [f'spawn{str(i).zfill(4)}.png' for i in range(1,7)]

        # ship images
        self.idle_drive_image = f'spaceShips_001-1.png'
        self.ship_images_list = ['spaceShips_001-1.png','spaceShips_001-2.png','spaceShips_001-3.png','spaceShips_001-4.png','spaceShips_001-5.png','spaceShips_001-6.png']
        self.ship_images_left_rotate_list = ['spaceShips_001-2r.png','spaceShips_001-2r.png','spaceShips_001-3r.png','spaceShips_001-4r.png','spaceShips_001-5r.png','spaceShips_001-6r.png']
        self.ship_images_right_rotate_list = ['spaceShips_001-2l.png','spaceShips_001-2l.png','spaceShips_001-3l.png','spaceShips_001-4l.png','spaceShips_001-5l.png','spaceShips_001-6l.png']
        
        self.username = self.game.FONT_ARIAL.render(f"{self.game.user['username']}", True, "blue")
        
        self.playing = playing
        self.camx = camx
        self.camy = camy
        self.facing_left = False
        self.health = health
        self.movespeed = movespeed
        self.users = users
        self.spawned = False
        self.angel = 0
        self.rotation_speed = 3
        self.inside_ship = inside_ship
        self.bullets = []
        
        self.user = {
            'username':self.game.user['username'],
            'cordinates':[self.camx, self.camy],
            'image': self.current_image,
            'facing':self.facing_left,
            'movespeed':self.movespeed,
            'inside_ship':self.inside_ship,
            'angle':self.angel,
        }
        
        # ANIMATION
        self.anim = self.spawn_images_list
        if inhospital:
            self.current_image = self.laying
            self.anim = [self.laying]
            
        self.anim_index = 0 
        self.anim_speed = anim_speed 
        self.animation_colldown = 0 
        
        #SOUNDS
        self.walk_channel = pygame.mixer.Channel(1)
        self.walk_sound = mixer.Sound(f"{os.getcwd()}/data/sounds/player/walking.ogg")

        self.hospital_channel = pygame.mixer.Channel(2)
        self.hospital_sound = mixer.Sound(f"{os.getcwd()}/data/sounds/player/hospital.mp3")

        self.ship_shoot_channel = pygame.mixer.Channel(5)
        self.ship_shoot_sound = mixer.Sound(f"{os.getcwd()}/data/sounds/player/ship_shoot.wav")

        self.space_music_channel = pygame.mixer.Channel(6)
        self.space_music_sound = mixer.Sound(f"{os.getcwd()}/data/sounds/player/space_music.mp3")

        if inhospital:
            if not self.hospital_channel.get_busy() and self.game.soundOn:
                self.hospital_channel.play(self.hospital_sound,loops=2)
        
        # KEYBOARD
        self.kbColldown = 10
        self.keyboard_colldown = self.kbColldown

        # RECT AND COLLISION
        self.mask = pygame.mask.from_surface(self.images['idlec.png'])
        self.rect = self.mask.get_rect()
        self.rect.center = [game.width/2, game.height/2]
        
        self.health_bar = HealthBar(self.game, self)
        self.inhospital = inhospital
    
    def update_animation(self):
        if self.animation_colldown >= self.anim_speed:
            self.animation_colldown = 0
            self.anim_index += 1
            if self.anim_index >= len(self.anim): 
                self.anim_index = 0
                self.spawned = True
                    
            self.current_image = self.anim[self.anim_index]
        self.animation_colldown += 1 

    def respawn(self, new_x, new_y, screen_animation=None, inhospital=False):
        if screen_animation != None:
            self.game.screen_animation.anim = screen_animation

        if inhospital:
            self.movespeed = 3
            self.inside_ship = False

        self.__init__(self.game, 
                      self.images,
                      camx=new_x, camy=new_y,
                      users=self.users,
                      health=self.health,
                      inside_ship=self.inside_ship,
                      movespeed=self.movespeed, 
                      inhospital=inhospital)
        
        self.game.map.__init__(self.game, 
                               x=-2500-new_x, 
                               y=-1450-new_y, 
                               map_images=self.game.map.images)

    def update(self):
        if self.game.internet.freez_game == False and self.playing:

            if self.inhospital == False and self.game.game_intro.show == False and self.game.game_chat.show is not True:
                if self.inside_ship:
                    self.keyboard_events_driver()
                else:
                    self.keyboard_events()

            self.update_animation()
            self.health_bar.update()
            
            # Check if player is dead
            if self.health <= 0: # if ded respawn in hospital bed
                self.respawn(-780, -390, inhospital=True) # -790, -390 = Hospital location on bed
                data_for_server = {
                    'inhospital': self.game.user['username']
                }
                self.game.internet.send_to_server(data_for_server)
                self.game.screen_animation.anim = self.game.screen_animation.anims['weakup']
                
            if self.inhospital:
                if self.health == 100:
                    self.respawn(-850, -390)
                    self.game.screen_animation.anim = None
                elif self.health >= 30:
                    self.game.screen_animation.anim = None

            self.user = {
                'username':self.game.user['username'],
                'cordinates':[self.camx, self.camy],
                'image': self.current_image,
                'facing':self.facing_left,
                'movespeed':self.movespeed,
                'inside_ship':self.inside_ship,
                'angle':self.angel,
                'bullets':self.bullets,
            }

            self.bullets = []
            
            self.game.internet.send_to_server(self.user)

            if self.game.soundOn and not self.inhospital and not self.space_music_channel.get_busy() and not self.game.game_intro.show:
                self.space_music_channel.play(self.space_music_sound)

    def keyboard_events_driver(self):
        key_pressed = pygame.key.get_pressed()
        
        if not True in key_pressed:
            self.anim = [self.idle_drive_image] 
        
        if key_pressed[pygame.K_d]:
            self.anim = self.ship_images_right_rotate_list
            self.angel -= self.rotation_speed
            if self.angel < -360:
                self.angel = 0
                
        if key_pressed[pygame.K_a]:
            self.anim = self.ship_images_left_rotate_list
            self.angel += self.rotation_speed
            if self.angel > 360:
                self.angel = 0
                
        if key_pressed[pygame.K_w]:
            self.anim = self.ship_images_list
            before_move_campos = [self.camx,self.camy]
            before_move_base_rectpos = [self.game.map.rect.x,self.game.map.rect.y]
            before_move_base_maskrectpos = [self.game.map.maskrect.x,self.game.map.maskrect.y]
            before_move_base_shipentryrectpos = [self.game.map.ship_entry_rect.x, self.game.map.ship_entry_rect.y]

            self.camx = (self.camx + round((self.movespeed * -math.sin(math.radians(self.angel)))))
            self.camy = (self.camy + round((self.movespeed * -math.cos(math.radians(self.angel)))))

            # MAP
            self.game.map.rect.x = (self.game.map.rect.x - round((self.movespeed * -math.sin(math.radians(self.angel)))))
            self.game.map.rect.y = (self.game.map.rect.y - round((self.movespeed * -math.cos(math.radians(self.angel)))))
            # MAP MASK
            self.game.map.maskrect.x = (self.game.map.maskrect.x - round((self.movespeed * -math.sin(math.radians(self.angel)))))
            self.game.map.maskrect.y = (self.game.map.maskrect.y - round((self.movespeed * -math.cos(math.radians(self.angel)))))

            # Map ship entry
            self.game.map.ship_entry_rect.x = (self.game.map.ship_entry_rect.x - round((self.movespeed * -math.sin(math.radians(self.angel)))))
            self.game.map.ship_entry_rect.y = (self.game.map.ship_entry_rect.y - round((self.movespeed * -math.cos(math.radians(self.angel)))))

            if self.collide_mask(self.mask, self.game.map.mask, self.rect, self.game.map.maskrect):
                self.camx = before_move_campos[0]
                self.camy = before_move_campos[1]
                # map
                self.game.map.rect.x = before_move_base_rectpos[0]
                self.game.map.rect.y = before_move_base_rectpos[1]
                # map mask
                self.game.map.maskrect.x = before_move_base_maskrectpos[0]
                self.game.map.maskrect.y = before_move_base_maskrectpos[1]
                # map ship entry
                self.game.map.ship_entry_rect.x = before_move_base_shipentryrectpos[0]
                self.game.map.ship_entry_rect.y = before_move_base_shipentryrectpos[1]
                            
        if key_pressed[pygame.K_SPACE]:
            if self.keyboard_colldown >= self.kbColldown and not self.rect.colliderect(self.game.map.rect):
                self.keyboard_colldown = 0
                self.bullets.append({
                                    "x":(self.camx) + round(self.rect.w/2 * -math.sin(math.radians(self.angel))),
                                    "y":(self.camy) + round(self.rect.w/2 * -math.cos(math.radians(self.angel))),
                                    "angel":self.angel,
                                    }
                                    )
                if self.game.soundOn:
                    self.ship_shoot_channel.play(self.ship_shoot_sound)
                
        self.keyboard_colldown += 1

    def keyboard_events(self):        
        key_pressed = pygame.key.get_pressed()
        
        if True not in key_pressed and self.spawned == True:
            self.anim = [self.idle_image]
        else:
            self.spawned = True
   
        if key_pressed[pygame.K_LCTRL]:
            self.anim = [self.spawn_images_list[-1]]

        if key_pressed[pygame.K_d]:
            self.facing_left = False
            self.anim = self.walk_images_list
            self.camx += self.movespeed
            self.game.map.move_map(-self.movespeed, 0)
            if self.collide_mask(self.mask, self.game.map.mask, self.rect, self.game.map.maskrect):
                self.camx -= self.movespeed
                self.game.map.move_map(self.movespeed, 0)
                
            if not self.walk_channel.get_busy() and self.game.soundOn:
                self.walk_channel.play(self.walk_sound)
        
        if key_pressed[pygame.K_s]:
            self.facing_left = False
            self.anim = self.walk_images_list
            self.camy += self.movespeed
            self.game.map.move_map(0, -self.movespeed)
            if self.collide_mask(self.mask, self.game.map.mask, self.rect, self.game.map.maskrect):
                self.camy -= self.movespeed
                self.game.map.move_map(0, self.movespeed)
                
            if not self.walk_channel.get_busy() and self.game.soundOn:
                self.walk_channel.play(self.walk_sound)
            
        if key_pressed[pygame.K_w]:
            self.facing_left = False
            self.anim = self.walk_images_list
            self.camy -= self.movespeed 
            self.game.map.move_map(0, self.movespeed)
            if self.collide_mask(self.mask, self.game.map.mask, self.rect, self.game.map.maskrect):
                self.camy += self.movespeed
                self.game.map.move_map(0, -self.movespeed)
                
            if not self.walk_channel.get_busy() and self.game.soundOn:
                self.walk_channel.play(self.walk_sound)
        
        if key_pressed[pygame.K_a]:
            self.facing_left = True
            self.anim = self.walk_images_list
            self.camx -= self.movespeed  
            self.game.map.move_map(self.movespeed, 0)
            if self.collide_mask(self.mask, self.game.map.mask, self.rect, self.game.map.maskrect):
                self.camx += self.movespeed
                self.game.map.move_map(-self.movespeed, 0)
            
            if not self.walk_channel.get_busy() and self.game.soundOn:
                self.walk_channel.play(self.walk_sound)

        if key_pressed[pygame.K_e] and self.keyboard_colldown >= self.kbColldown:
            self.keyboard_colldown = 0
                    
        self.keyboard_colldown += 1
    
    def collide_mask(self, left, right, leftrect, rightrect):
        xoffset = rightrect.x - leftrect.x
        yoffset = rightrect.y - leftrect.y      
        return left.overlap(right, (xoffset, yoffset))
    
    def calculate_cords_by_my_position(self, cordinates):
        new_x = cordinates[0] + self.rect.center[0] - self.camx
        new_y = cordinates[1] + self.rect.center[1] - self.camy
        return [new_x, new_y]
    
    def render_other_players(self):
        users = copy.deepcopy(self.users) # Becaus of garbage collector
        for player in users: # draw all players
            if users[player]['username'] != self.game.user['username']: # Skip my self

                cordinates = self.calculate_cords_by_my_position(users[player]['cordinates'])
                angle = users[player]['angle']
                inside_ship = users[player]['inside_ship']
                username_str = users[player]['username'] # Player username
                health = users[player]['health'] # Player health
                facing = users[player]['facing'] # Current player facing
                image = users[player]['image'] # Current player image displaying

                rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
                rect.center = [cordinates[0], cordinates[1]]

                # Draw player
                if not inside_ship:
                    self.game.screen.blit(self.images[image] if facing == False else pygame.transform.flip(self.images[image], True, False), rect)
                else:
                    self.draw_image(self.game.screen, 
                            self.images[image] if facing == False else pygame.transform.flip(self.images[image], True, False), 
                            [rect.center[0], rect.center[1]], (self.images['spaceShips_001-1.png'].get_width()/2, self.images['spaceShips_001-1.png'].get_height()/4), angle)
                
                # Draw player username
                username = self.game.FONT_ARIAL.render(username_str, True, "yellow")
                self.game.screen.blit(username,(rect.center[0] - username.get_width()/2, rect.y - username.get_height() - (10 if not inside_ship else 35)))

                # Draw player health bar
                health_background_rect = pygame.Rect(0, 0, 100, 10)
                health_background_rect.center = [rect.center[0], rect.y - (5 if not inside_ship else 30)]
                health_rect = pygame.Rect(0, 0, 100, 10)
                health_rect.center = [rect.center[0], rect.y - (5 if not inside_ship else 30)]
                health_rect.w = health
                pygame.draw.rect(self.game.screen, "black", health_background_rect)
                pygame.draw.rect(self.game.screen, "green", health_rect)

    def draw_image(self, surf, image, pos, originPos, angle):
        # offset from pivot to center
        image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        
        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        rotated_image_center = (pos[0] - rotated_offset.x, (pos[1] - rotated_offset.y))

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
        
        # rotate and blit the image
        surf.blit(rotated_image, rotated_image_rect)

    def render(self):
        if self.playing:
            # ----------- Other players --------------
            # ----------------------------------------
            self.render_other_players()
        
            # -------------- My self ------------------  
            # ----------------------------------------- 
            if not self.inside_ship:
                self.game.screen.blit(self.images[self.current_image] if self.facing_left == False else pygame.transform.flip(self.images[self.current_image], True, False), self.rect)
            else:
                self.draw_image(self.game.screen, 
                            self.images[self.current_image] if self.facing_left == False else pygame.transform.flip(self.images[self.current_image], True, False), 
                            [self.rect.center[0], self.rect.center[1]], (self.images['spaceShips_001-1.png'].get_width()/2, self.images['spaceShips_001-1.png'].get_height()/4), self.angel)

            if self.game.dev_mode:
                pygame.draw.rect(self.game.screen, "red", self.rect, width=1)
                
            # username
            self.game.screen.blit(self.username, (self.health_bar.background_rect.center[0] - self.username.get_width()/2, self.health_bar.background_rect.y - self.username.get_height()))

            # Health bar
            self.health_bar.render()
            # -------------- My self ------------------  
            # -----------------------------------------