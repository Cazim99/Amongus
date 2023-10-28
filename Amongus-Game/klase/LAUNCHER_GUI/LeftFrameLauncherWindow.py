import tkinter as tk
import webbrowser
import requests
import ast
import threading
import customtkinter


class LeftFrameLauncherWindow(customtkinter.CTkFrame):
    
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.configure(corner_radius=30, border_width=5)

        self.login_request_thread = None
        
        game_title_label = customtkinter.CTkLabel(self, text=f"Amongus",font=master.FONT)
        game_title_label.pack(pady=20, anchor="center")

        self.email_entry = customtkinter.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10,anchor="center")

        self.password_entry = customtkinter.CTkEntry(self, show='*', placeholder_text='Password')
        self.password_entry.pack(pady=10,anchor="center")
        
        self.error_label = customtkinter.CTkLabel(self, text='')
        self.error_label.pack(pady=10,anchor="center")
        
        login_btn = customtkinter.CTkButton(self, text="Login", cursor="hand2", command=self.login)
        login_btn.pack(pady=10, anchor="center")
        
        self.createAccount_label = customtkinter.CTkLabel(self, text="Dont have account? Register now", cursor="hand2")
        self.createAccount_label.bind("<Button-1>", lambda event:self.open_website())
        self.createAccount_label.bind("<Enter>", lambda event:self.mouse_over_crtacc_lbl())
        self.createAccount_label.bind("<Leave>", lambda event:self.mouse_not_over_crtacc_lbl())
        self.createAccount_label.pack(padx=30,pady=10,anchor="center")

        # when we calculate email_entry width * font_entry size and add 20 padx == frame width 5 is bonus 
        self.frame_widht = (self.cget('width')) + 60
    
    def login(self):
        if threading.activeCount() < 3:
           self.login_request_thread = threading.Thread(target=self.send_login_request, daemon=True).start()
    
    def send_login_request(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        try:
            respond = requests.get(f"http://{self.master.website[0]}:{self.master.website[1]}/login-application?email={email}&password={password}")
            respond = respond.json()
        except ConnectionError as ce:
            print(ce)
        
        if respond['status-code'] == 200:
            self.error_label.configure(text=respond['message'])
            user = ast.literal_eval(respond['user'])

            self.master.user = {
                'username':user['username'],
                'cordinates':[int(user['cordinates'].split(",")[0]), # x
                              int(user['cordinates'].split(",")[1])], # y
                'health': user['health'],
                'movespeed': user['movespeed'],
                'inside_ship': user['inside_ship'],
                'angle':0,
            }

            self.master.close_launcher()
        else:
            self.error_label.configure(text=respond['message'], text_color='red')
    
    def mouse_over_crtacc_lbl(self):
        self.createAccount_label.configure(text_color="green")
        
    def mouse_not_over_crtacc_lbl(self):
        self.createAccount_label.configure(text_color="gray")
        
    def open_website(self):
        webbrowser.open(f"http://{self.master.website[0]}:{self.master.website[1]}")