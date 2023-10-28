import tkinter as tk
from tkinter import simpledialog
import customtkinter

class PlayerDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title, player):
        self.player = player
        super().__init__(parent, title)
        self.parent = parent

    def body(self, frame):

        self.username_label = customtkinter.CTkLabel(frame, width=25, text='Username: '+self.player['username'], text_color="black")
        self.username_label.pack(anchor='w')

        self.health_label = customtkinter.CTkLabel(frame, width=25, text="Health: " + str(self.player['health']), text_color="black")
        self.health_label.pack(anchor='w')

        self.movespeed_label = customtkinter.CTkLabel(frame, width=25, text="Movespeed: " + str(self.player['movespeed']), text_color="black")
        self.movespeed_label.pack(anchor='w')

        return frame

    def ok_pressed(self):
        self.destroy()

    def kick_pressed(self):
        self.parent.server.send_to_server(f"ADMINDASHBOARD:[KICK]:{self.player['username']}")
        self.destroy()

    def ban_pressed(self):
        self.parent.server.send_to_server(f"ADMINDASHBOARD:[BAN]:{self.player['username']}")
        self.destroy()


    def buttonbox(self):
        kick_button = customtkinter.CTkButton(self, text='KICK', width=5, command=self.kick_pressed, fg_color='blue', hover_color='darkblue')
        kick_button.pack(pady=10)

        ban_button = customtkinter.CTkButton(self, text='BAN', width=5, command=self.ban_pressed, fg_color='red', hover_color='darkred')
        ban_button.pack(pady=10)

        ok_button = customtkinter.CTkButton(self, text='OK', width=5, command=self.ok_pressed)
        ok_button.pack(pady=10,padx=10, fill=tk.BOTH)

        self.bind("<Return>", lambda event: self.ok_pressed())

        self.configure(padx=20)