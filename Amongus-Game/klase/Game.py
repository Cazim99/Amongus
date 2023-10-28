import pygame
import os
from ImageLoader import ImageLoader

# GUI
from klase.GUI.SettingsMenu import SettingsMenu
from klase.GUI.Title import Title
from klase.GUI.Button import Button
from klase.GUI.Message import Message
from klase.GUI.Layout import Layout
from klase.GUI.Chat import Chat

# SERVER
from klase.Server import Server

# Screen Animation
from klase.ScreenAnimation import ScreenAnimation

# Intro
from klase.GameIntro import Intro

class Game:
    
    GAME_VERSION = 1.0
    
    def __init__(self, 
                 gamename:str, 
                 screen_size:tuple, 
                 server:tuple, 
                 user:dict, 
                 full_screen:bool = False, 
                 FPS:int = 60, 
                 dev_mode:bool = False,
                 soundOn = True,   
                 first_time_run = True):    
        
        self.first_time_run = first_time_run # If true you will see game intro first time playing
        self.exit_message = None # if exit message is not none, after game exit you will see exit message
        self.restart = None # if settings apply not None
        self.soundOn = soundOn # Sounds on/off
        self.gamename = gamename # Window titile ( Game name )
        self.screen_size = screen_size # (WIDTH, HEIGHT)
        self.full_screen = full_screen # DEFAULT FALSE
        self.FPS = FPS # DEFAULT 60 Frame per secound
        self.dev_mode = dev_mode  # For developer
        self.server = server # (HOST, PORT)
        self.game_running = False # False until player press play button on screen
        self.user = user # User data

        self.gameicon = pygame.image.load(f"{os.getcwd()}/data/game_icon.png") # Load game icon image
        
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption(f"{self.gamename + ' - ' + str(Game.GAME_VERSION)}") # Window title ( Game title)
        pygame.display.set_icon(self.gameicon) # Apply game icon from data folder
        pygame.mouse.set_visible(False) # Using my own currsor, we hide official windows/linux cursor with this method
        
        # Set up screen type Fullscreen/not fullscreen
        if self.full_screen is False:
            self.screen = pygame.display.set_mode(self.screen_size)
        else:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        
        # Load laptop/desktop pc screen sizes
        self.width = self.screen.get_width()
        self.height = self.screen.get_height() 
        
        self.FramePerSec = pygame.time.Clock()
        self.current_fps = self.FPS
        
        self.init()
          
    def for_developer_game_info(self):
        if self.dev_mode == True:
            font = pygame.font.SysFont("Arial", int(self.width/100) * 2)
            fps_text = font.render(f"FPS: {int(self.current_fps)}", True, "red")
            self.screen.blit(fps_text, (10, 0))  

            counter = 3
            if self.player != None and self.map != None:
                healthtext = font.render(f"Health:{self.player.health}", True, "red")
                self.screen.blit(healthtext, (10, fps_text.get_height() * 2))
                
                for player in self.player.users:
                    playertxt = font.render(f"{(self.player.users[player]['username'],self.player.users[player]['cordinates'])}", True, "blue")
                    self.screen.blit(playertxt, (10, fps_text.get_height()*counter))
                    counter+=1
  
    def init(self):    
        # CONSTANTS
        self.FONT = pygame.font.SysFont("Bradley Hand ITC", 24)
        self.BIG_FONT = pygame.font.SysFont("Bradley Hand ITC", 32)
        self.FONT_ARIAL = pygame.font.SysFont("Arial", 24)
        self.FONT_BIG_ARIAL = pygame.font.SysFont("Arial", 32)
        
        # CURSOR
        self.cursor_images = ImageLoader.load_images(f"{os.getcwd()}/data/gui_images/cursor/")
        self.cursor_current = self.cursor_images['cursor.png']
        self.cursor = self.cursor_current
        self.cursor_pos = self.cursor.get_rect()
        
        # Internet error screen message
        self.internet_error_message = Message(self, self.width/2, self.height/2)  # This dont go in layout, this is always visible

        # Screen message
        self.screen_message = Message(self, self.width/2, self.height/2,)  # This dont go in layout, this is always visible

        # ============================= GUI =========================================  
        self.game_title = Title(self, self.width/2, 40 , f"{self.gamename}")

        # Chat
        chat_w = self.width/2
        chat_h = self.height/4
        chat_margin = 10
        self.game_chat = Chat(self, 0 + chat_margin, (((self.height - chat_h))-70)-chat_margin, chat_w, chat_h)

        # Buttons
        self.play_btn = Button(self, self.width/2, self.height/3, text="PLAY")
        self.settings_btn = Button(self, self.width/2, self.height/3 + self.play_btn.rect.h + 10, text="SETTINGS")
        self.exit_btn = Button(self, self.width/2, self.height/3 + self.play_btn.rect.h*2 + 20, text="EXIT", color="red")

        # --- MENUS ----
        # settings menu
        self.settings_menu = SettingsMenu(self, self.width/2, self.height/2)
        
        # Layout
        self.layout = Layout(self)
        self.layout.add_in_layout("game_title", self.game_title)
        self.layout.add_in_layout("play_btn", self.play_btn, hasEvent=True)
        self.layout.add_in_layout("settings_btn", self.settings_btn, hasEvent=True)
        self.layout.add_in_layout("exit_btn", self.exit_btn, hasEvent=True)
        self.layout.add_in_layout("settings_menu", self.settings_menu)
        
        # ============================= GUI =========================================  

        # Screen Animation
        # Scale images by game widnow size to fit window
        screen_anim_images = ImageLoader.load_images(f"{os.getcwd()}/data/screen_animation/")
        for image in screen_anim_images:
            screen_anim_images[image] = pygame.transform.scale(screen_anim_images[image], (self.width, self.height)) 
        self.screen_animation = ScreenAnimation(self, images=screen_anim_images, anim_speed=50)
        
        # Intro 
        self.game_intro = Intro(self)
        
        # Player
        self.player = None 

        # Map
        self.map = None

        # Internet(Server communication)
        self.internet = Server(self)
        
    def start(self):
        self.game_loop()

    def stop(self, kicked=False):
        if not kicked:
            data_for_server = {
                'disconnected':self.user['username'],
            }
            self.internet.send_to_server(data_for_server)
        self.game_running = False
    
    def update_mouse(self):
        self.cursor_pos.x = pygame.mouse.get_pos()[0]
        self.cursor_pos.y = pygame.mouse.get_pos()[1]
        if not self.settings_menu.active:
            self.layout.mouse_events()
        else:
            self.settings_menu.mouse_events()
        
    def update(self):
        self.update_mouse()

        # WHEN PLAYING UPDATE MAP AND PLAYER
        if self.player != None and self.map != None:
            # Play intro only when first time press play button
            if self.first_time_run and self.game_intro.show == False:
                if not self.game_intro.intro_channel.get_busy():
                    self.game_intro.intro_sound.play()
                    self.game_intro.show = True
                    
            self.map.update()
            self.player.update()
        
        self.screen_animation.update()
        self.game_intro.update()
        
    def render(self):
        # WHEN PLAYING RENDER MAP AND PLAYER
        if self.map != None and self.player != None:
            self.map.render()
            self.player.render()

        # ------------------ ON TOP DRAWINGS -------------------------
        # ------------------------------------------------------------
        # SCREEN ANIMATIONS
        self.screen_animation.render()

        # DRAW LAYOUT
        self.layout.render()
        
        # Screen message
        self.screen_message.render()

        # internet error message DRAW IF EXISTS
        self.internet_error_message.render()
        
        # DRAW MOUSE(CURSOR)
        self.screen.blit(self.cursor, self.cursor_pos)
        
        # DRAW GAME CHAT
        self.game_chat.render()

        # DRAW INTRO
        self.game_intro.render()
        # ------------------ ON TOP DRAWINGS -------------------------
        # ------------------------------------------------------------
    
    def events_handler(self):
        events  = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.stop()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if self.game_chat.show == False and self.player != None and self.map != None:
                        self.game_chat.show = True

                if event.key == pygame.K_ESCAPE:
                    if self.game_chat.show:
                        self.game_chat.show = False
                    elif self.internet.is_alive() == True:
                        if self.layout.hidden == False:
                            if self.layout.elements['settings_menu']['element'].active == True:
                                self.layout.elements['settings_menu']['element'].active = False
                            else:
                                self.layout.hidden = True
                        else:
                            self.layout.hidden = False
                    else:
                        if self.layout.elements['settings_menu']['element'].active == True:
                            self.layout.elements['settings_menu']['element'].active = False

                if self.game_chat.show:
                    if event.key == pygame.K_BACKSPACE:
                        self.game_chat.input = self.game_chat.input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(self.game_chat.input) > 0:
                            self.game_chat.send_chat()
                    else:
                        input_surface = self.game_chat.font.render(self.game_chat.input, 0, 'red')
                        input_width, input_height = input_surface.get_size()
                        if (input_width + self.game_chat.font.get_height() + 15) < self.game_chat.entry_rect.w:
                            self.game_chat.input += event.unicode

            if self.layout.hidden == False and self.settings_menu.active == False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    elements = self.layout.elements
                    for key in elements:
                        if elements[key]['hasEvent']:
                            if elements[key]['element'].rect.collidepoint(self.cursor_pos.x, self.cursor_pos.y):
                                elements[key]['element'].pressed()
                                if key == "play_btn" and elements[key]['element'].disabled == False:
                                    if self.internet.is_alive() == False:
                                        elements[key]['element'].disabled = True
                                        self.layout.hidden = True
                                        self.internet.connect_to_server()
                                elif key == "settings_btn" and elements[key]['element'].disabled == False:
                                    elements['settings_menu']['element'].active = True
                                elif key == "exit_btn" and elements[key]['element'].disabled == False:
                                    self.stop()
                                else:
                                    pass
                                break
                elif event.type == pygame.MOUSEBUTTONUP:
                    elements = self.layout.elements
                    for key in elements:
                        if elements[key]['hasEvent']:
                             elements[key]['element'].unpressed()
                             
            elif self.settings_menu.active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.settings_menu.fullscreen_on_off_btn.rect.collidepoint(self.cursor_pos.x, self.cursor_pos.y):
                        self.settings_menu.fullscreen_on_off_btn.pressed()
                        self.full_screen = False if self.full_screen else True
                        self.settings_menu.save_settings()
                        self.game_running = False
                        self.restart = {'soundOn':self.soundOn,'fullscreen':self.full_screen}
                    elif self.settings_menu.sound_on_off_btn.rect.collidepoint(self.cursor_pos.x, self.cursor_pos.y):
                        self.soundOn = False if self.soundOn else True
                        if self.player != None:
                            if self.soundOn == False:
                                self.player.space_music_channel.stop()
                        self.settings_menu.sound_on_off_btn = Button(self, 
                                                                     x=self.settings_menu.sound_on_off_btn.rect.center[0],
                                                                     y=self.settings_menu.sound_on_off_btn.rect.center[1],
                                                                     text="Sound off" if self.soundOn else "Sound on",
                                                                     color="red" if self.soundOn else "green")
                        self.settings_menu.sound_on_off_btn.pressed()
                        self.settings_menu.save_settings()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.settings_menu.sound_on_off_btn.unpressed()
                    self.settings_menu.fullscreen_on_off_btn.unpressed()

    def game_loop(self):
        self.game_running = True
        while self.game_running:
                
            self.events_handler()
            
            self.screen.fill("black")
            
            self.update()
            self.render()

            self.for_developer_game_info()

            self.FramePerSec.tick(self.FPS)
            self.current_fps = self.FramePerSec.get_fps()
            pygame.display.update()