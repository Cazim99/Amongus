import tkinter as tk
from .LeftFrameLauncherWindow import LeftFrameLauncherWindow
from .RightFrameLauncherWindow import RightFrameLauncherWindow
from .PlayerFrame import PlayerFrame
from screeninfo import screeninfo
import customtkinter


class LauncherWindow(customtkinter.CTk):
    
    LAUNCHER_VERSION = 1.0
    
    LAUNCHER_WIDTH = screeninfo.get_monitors()[0].width
    LAUNCHER_HEIGHT = screeninfo.get_monitors()[0].height

    FONT = ("Arial",30)
    FONT_LABELS = ("Arial",15)
    FONT_LABELS_SMALL = ("Arial",10)
    FONT_ENTRYS = ("Arial",15)
    
    def __init__(self, website):
        super().__init__()
        
        customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
        

        self.configure(bg_color='white', fg_color='white')

        self.user = None 
        self.website = website
        
        self.playerx = 0
        self.playery = screeninfo.get_monitors()[0].height - 95 # 95 = 75 player.gif height + 20 message height(font) and 5 bonus
        
        # widnow title
        self.title(f"Amognus - {LauncherWindow.LAUNCHER_VERSION}")
        self.resizable(False,False)

        # set white color background after that white will be converted in transparent
        self.config(bg="white")

        # Hide the  window drag bar and close button
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        
        # set transparent window
        self.wm_attributes("-transparentcolor", "white")
        
        # center window on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (LauncherWindow.LAUNCHER_WIDTH/2))
        y_cordinate = int((screen_height/2) - (LauncherWindow.LAUNCHER_HEIGHT/2))
        self.geometry("{}x{}+{}+{}".format(LauncherWindow.LAUNCHER_WIDTH, LauncherWindow.LAUNCHER_HEIGHT, x_cordinate, y_cordinate))
        
        # LOGIN LEFT SIDE
        self.left_frame = LeftFrameLauncherWindow(self)
        self.left_frame.place(x=LauncherWindow.LAUNCHER_WIDTH/3, y=LauncherWindow.LAUNCHER_HEIGHT/3)
        
        
        # PLANETS ANIMATION RIGHT SIDE
        self.right_frame = RightFrameLauncherWindow(self)
        self.right_frame.place(x=LauncherWindow.LAUNCHER_WIDTH/3 + self.left_frame.frame_widht, y=LauncherWindow.LAUNCHER_HEIGHT/3)
        
        
        # PLAYER WALKING BOTTOM SIDE OF SCREEN
        self.bottom_frame = PlayerFrame(self)
        self.bottom_frame.place(x=self.playerx,
                                y=self.playery)
        self.bottom_frame.after(30, self.move_player)
    
    def close_launcher(self):
        self.destroy()
        
    def move_player(self):
        self.playerx += 3
        if self.playerx >= LauncherWindow.LAUNCHER_WIDTH:
            self.playerx = 0
    
        self.bottom_frame.place(x=self.playerx, 
                                y=self.playery)
        self.bottom_frame.after(15, self.move_player)