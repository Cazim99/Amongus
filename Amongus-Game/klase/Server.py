import socket
import pickle
import threading
import time
import random
from klase import Game
from .Map import Map
from .Player import Player
from ImageLoader import ImageLoader
import os
import pygame

class Server(threading.Thread):
    
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.settimeout(4) # If reciving data from server take more then 4 secounds try reconnecting 
    BYTES_LEN = 3072
    
    running = True
    freez_game = True
    saveddata = None
    
    def __init__(self, game:'Game.Game'):
        self.game = game
        self.serverAddress = (game.server[0], game.server[1])
        super().__init__(target="run", daemon=True)
        
    def run(self):
        self.send_to_server(self.game.user)
        while self.running:
            try:
                data_from_server = self.recive_from_server()['data']
                if '[KICKED]' in data_from_server:
                    self.running = False
                    self.game.exit_message = "You are kicked by server administrator !"
                    self.game.stop(kicked=True)
                    break
                elif '[BANED]' in data_from_server:
                    self.running = False
                    self.game.exit_message = "You are BANED by server administrator !!!!!!!!!!!!"
                    self.game.stop(kicked=True)
                    break
                elif '[RESPAWN]' in data_from_server:
                    new_cordinates = data_from_server.replace('[RESPAWN]:','').strip()
                    new_cordinates = [int(new_cordinates.split(",")[0]),int(new_cordinates.split(",")[1])]
                    self.game.player.respawn(new_cordinates[0],new_cordinates[1])
                    continue
                
                if 'users' in data_from_server:
                    myself = data_from_server['users'][self.game.user['username']] 
                    
                    # ----------- Inistalize myself(player class) and map(map class) 
                    if self.game.player == None or self.game.map == None:
                        player_images = ImageLoader.load_images(f"{os.getcwd()}/data/player_images/")
                        self.game.player = Player(self.game, 
                                                player_images,
                                                myself['cordinates'][0], myself['cordinates'][1], 
                                                users=data_from_server['users'],
                                                inside_ship=myself['inside_ship'],
                                                health=myself['health'],
                                                movespeed=myself['movespeed'])
                        
                        map_images = ImageLoader.load_images(f"{os.getcwd()}/data/map_images/")
                        map_images['base.png'].set_colorkey("white") # white color remove
                        map_images['base.png'] = map_images['base.png'].convert_alpha()
                        map_images['base_collision_mask.png'].set_colorkey("white") # white color remove
                        map_images['base_collision_mask.png'] = map_images['base_collision_mask.png'].convert_alpha()
                        map_images['base_collision_mask_ship.png'].set_colorkey("white") # white color remove
                        map_images['base_collision_mask_ship.png'] = map_images['base_collision_mask_ship.png'].convert_alpha()
                        self.game.map = Map(self.game,
                                            x=-2500-myself['cordinates'][0], 
                                            y=-1450-myself['cordinates'][1], 
                                            map_images=map_images)
                        
                        self.game.map.bullets = data_from_server['bullets']

                    # -------------------------------------------
                    
                    # Player variables update loaded from server
                    self.game.player.users = data_from_server['users'] # Other players
                    self.game.player.health = myself['health']
                    self.game.map.bullets = data_from_server['bullets']
                                
                    self.game.internet_error_message.text = self.game.FONT_ARIAL.render("", True, "red")
                    self.freez_game = False
                
            except (Exception,TimeoutError) as ex:
                print(ex)
                self.game.internet_error_message.text = self.game.FONT_ARIAL.render(f"Something went wrong, reconnecting...", True, "red")
                self.freez_game = True 
                self.send_to_server(self.game.user)
                time.sleep(1)
                
    def connect_to_server(self):
        self.start()

    def send_to_server(self, msg):
        message = msg
        message = pickle.dumps(message)
        self.UDPClientSocket.sendto(message, self.serverAddress)

    def recive_from_server(self):
        respond = self.UDPClientSocket.recvfrom(Server.BYTES_LEN)
        data = pickle.loads(respond[0])
        address = respond[1]
        return {'data':data, 'address':address}