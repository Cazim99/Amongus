import pygame
import os


class Layout:
    
    
    def __init__(self, root, hidden=False):
        self.root = root
        self.hidden = hidden
        self.background = pygame.transform.scale(pygame.image.load(f"{os.getcwd()}/data/gui_images/background.png"),(root.width, root.height))
        self.elements = {}
        
    def add_in_layout(self, key, element, hasEvent = False):
        self.elements[key] = {'element':element, 'hasEvent':hasEvent}
    
    def mouse_events(self):
        if self.hidden == False:
            mouse_hover_element = False
            # ------------ MOUSE HOVER EVENT CHAINGING CURRSOR
            for key in self.elements:
                if self.elements[key]['hasEvent'] == True:
                    if self.root.cursor_pos.colliderect(self.elements[key]['element'].rect):
                        mouse_hover_element = True
                        self.root.cursor = self.root.cursor_images['cursor_click.png']
                        break
                            
            if mouse_hover_element == False:
                self.root.cursor = self.root.cursor_images['cursor.png']
            # ------------ MOUSE HOVER EVENT CHAINGING CURRSOR
                
    def render(self):
        if self.hidden == False:
            if self.root.map == None and self.root.player == None:
                self.root.screen.blit(self.background, (0,0))
            for key in self.elements:
                self.elements[key]['element'].render()