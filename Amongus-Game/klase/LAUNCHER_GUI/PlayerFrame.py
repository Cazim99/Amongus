import tkinter as tk
from PIL import Image, ImageTk
import os
from itertools import count, cycle
import random

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

class PlayerFrame(tk.Frame):
    
    def __init__(self, master):
        super().__init__(master)

        self.messages = ['1 + 1 = 3', 
                         'I like your taskbar', 
                         'Hey login, and lets travel together', 
                         'am i dumb ?',
                         'Im not a liar',
                         'i cant stop talking...']
        
        self.master = master
        self.config(bg="white")
        
        self.message_label = tk.Label(self, text="Enter password, I won't tell anyone, don't worry :D",background="white", foreground="#00FFFF")
        self.message_label.pack(anchor="center")
        self.message_label.after(3000, self.update_message)
        
        self.planet_gif_image = AnimatedGif(self)
        self.planet_gif_image.pack(anchor="w")
        self.planet_gif_image.load(f"{os.getcwd()}" + "/data/launcher_images/player.gif")
        
    def update_message(self):
        rand_message_index = random.randint(0,len(self.messages))
        if rand_message_index >= len(self.messages):
            if len(self.master.left_frame.password_entry.get()) > 0:
                message = f"Your password is {(len(self.master.left_frame.password_entry.get()))*'*'}"
            else:
                message = f"Enter password, I won't tell anyone, don't worry :D"
        else:
            message = self.messages[rand_message_index]
        self.message_label.config(text=f"{message}")
        self.message_label.after(2000, self.update_message)
        
    