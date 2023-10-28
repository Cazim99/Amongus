import tkinter as tk
from PIL import Image, ImageTk
import os
from itertools import count, cycle
import customtkinter

class AnimatedGif(tk.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()
            
    def unload(self):
        self.config(image=None)
        self.frames = None
        
    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames),bg="white", fg="#00FFFF")
            self.after(self.delay, self.next_frame)

class RightFrameLauncherWindow(customtkinter.CTkFrame):
    
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg_color="white", fg_color='white')
        
        exit_btn = customtkinter.CTkButton(self, text="Leave",border_width=2, command=master.close_launcher,cursor="hand2")
        exit_btn.pack(pady=10,anchor="center")
        
        planet_gif_image = AnimatedGif(self)
        planet_gif_image.pack()
        planet_gif_image.load(f"{os.getcwd()}" + "/data/launcher_images/planets.gif")
    