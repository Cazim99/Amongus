import customtkinter
from player_dialog import PlayerDialog
from ctk_listbox import *
from Server import Server

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Window(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.server = None

        # Window configurations
        self.title("Amongus Server Dashboard")
        self.geometry("800x600")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # --------------------  SIDE BAR ------------------
        # -------------------------------------------------
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0,column=0, rowspan=4, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4,weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Amongus", font=customtkinter.CTkFont('Roboto',size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_btn_connectws = customtkinter.CTkButton(self.sidebar_frame, text="Connect with server", command=self.connect_with_server)
        self.sidebar_btn_connectws.grid(row=1, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))


        # --------------------  TABS ----------------------
        # -------------------------------------------------
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Info")
        self.tabview.tab("Info").grid_columnconfigure(0, weight=1) 

        self.info_tab_started = customtkinter.CTkLabel(self.tabview.tab('Info'), text="", text_color="red")
        self.info_tab_started.grid(row=0,column=0, sticky="w")
        
        self.info_tab_online = customtkinter.CTkLabel(self.tabview.tab('Info'), text="", text_color='blue')
        self.info_tab_online.grid(row=1,column=0,sticky="w")


        # --------------------  PLAYERS LIST ----------------------
        # ---------------------------------------------------------
        self.players_listbox = CTkListbox(self, command=self.show_player, text_color="blue")
        self.players_listbox.grid(row=0, column=2, sticky="nsew",padx=(0, 20), pady=(40,0))

        self.players_listbox_label = customtkinter.CTkLabel(self, text="Online players", font=customtkinter.CTkFont('Roboto',size=10, weight="bold"))
        self.players_listbox_label.grid(row=0, column=2, sticky="n", pady=10)

        # -------------------- SERVER OUTPUT ----------------------
        # ---------------------------------------------------------
        self.output = customtkinter.CTkTextbox(self)
        self.output.configure(state='normal')
        self.output.insert(customtkinter.END, text = "------------------ HELP -----------------\n")
        self.output.insert(customtkinter.END, text = "set health username,new_health\n    - Example: set health Petar,46\n")
        self.output.insert(customtkinter.END, text = "set cordinates x,y\n    - Example: set cordinates 200,300\n")
        self.output.configure(state='disabled')
        self.output.grid(row=1, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")


        # -------------------- SERVER COMMAND SENDER ----------------------
        # -----------------------------------------------------------------
        self.command_entry = customtkinter.CTkEntry(self, placeholder_text="Enter command")
        self.command_entry.grid(row=2, column=1, padx=(20, 20), pady=(0, 20), sticky="nsew")

        self.send_command_btn = customtkinter.CTkButton(master=self,text="send",fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: self.send_command(self.command_entry.get()))
        self.send_command_btn.grid(row=2, column=2, padx=(0, 20), pady=(0, 20), sticky="nsew")
        self.send_command_btn.configure(state=customtkinter.DISABLED)

    def send_command(self, command):
        self.output.configure(state='normal')

        if command.startswith('set health'):
            self.server.send_to_server(f"ADMINDASHBOARD:[COMMAND]:{command}")
            self.output.insert(customtkinter.END, text = f"\n[SERVER-DASHBOARD] Command sent to server ({command})\n")
        elif command.startswith('set cordinates'):
            self.server.send_to_server(f"ADMINDASHBOARD:[COMMAND]:{command}")
            self.output.insert(customtkinter.END, text = f"\n[SERVER-DASHBOARD] Command sent to server ({command})\n")
        elif command == '/help':
            self.output.insert(customtkinter.END, text = "\n - set health username,new_health\n")
            self.output.insert(customtkinter.END, text = "\n - set cordinates x,y\n")
        else:
            self.output.insert(customtkinter.END, text = f"\n[SERVER-DASHBOARD] Unknow command type /help for more info.\n")
        
        self.output.configure(state='disabled')

    def connect_with_server(self):
        if self.server == None:
            self.server = Server(('localhost', 9999))
            self.server.start()
            self.sidebar_btn_connectws.configure(state=customtkinter.DISABLED)
            self.send_command_btn.configure(state=customtkinter.NORMAL)

    def info_tab_update(self):
        if self.server != None and self.server.online:
            self.info_tab_started.configure(text = 'Server: Online', text_color='green')
            self.info_tab_online.configure(text=f"Online players: {len(self.server.data_from_server['players'])}")
        elif self.server != None and self.server.online == False:
            self.info_tab_started.configure(text = 'Server: offline',text_color='red')
        else:
            self.info_tab_started.configure(text = 'Server: Not connected',text_color='red')

        self.tabview.after(1000, self.info_tab_update)

    def players_list_update(self):
        if self.server != None:
            try:
                self.players_listbox.delete('all')
                n = 0
                for player in self.server.data_from_server['players']:
                    self.players_listbox.insert(n, player)
                    n+=1
            except:
                pass

        self.players_listbox.after(1000, self.players_list_update)

    def output_update(self):
        if self.server != None:
            try:
                self.output.configure(state='normal')
                for output in self.server.data_from_server['output']:
                    self.output.insert(customtkinter.END, text = output + '\n')
                self.output.configure(state='disabled')
            except:
                pass
        
        self.output.after(1000, self.output_update)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def show_player(self, selected_player):
        try:
            PlayerDialog(title='Player info', 
                         parent=self, 
                         player=self.server.data_from_server['players'][selected_player])
        except:
            pass

if __name__ == "__main__":
    window = Window()
    window.output_update()
    window.players_list_update()
    window.info_tab_update()
    window.mainloop()
    
            







