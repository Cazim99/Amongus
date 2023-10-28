import socket
import pickle
from ConfigLoader import ConfigLoader
import threading
import queue
from Recive import Recive
from Broadcast import Broadcast
import copy
import _thread

import time

# FOR DATABASE
import os,sys
sys.path.append(os.path.abspath(os.path.join('..')))
from db import DBengine
from db.Users import Users



class GameServer(threading.Thread):
    
    def __init__(self):
        super().__init__(target='run')

        config_file_informations = {
            "settings":
                {
                    'items':{
                        'server_host':'str',
                        'server_port':'int',
                    }
                },
            "database":
                {
                    'items':{
                        'db_protocol':'str',
                        'db_lib':'str',
                        'db_name':'str',
                        'user':'str',
                        'host':'str',
                        'port':'int',
                        'echo': 'bool',
                        'password':'str',
                    }
                }
        }

        CONFIGURATIONS = ConfigLoader.Load("config.ini", config_file_informations) # Load all configurations

        # SERVER CONFIG
        SERVER_CONFIGS = CONFIGURATIONS['settings']['items']

        # DB CONFIG
        DBengine.DB_CONFIG = CONFIGURATIONS['database']['items']

        # UDP
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((SERVER_CONFIGS['server_host'], SERVER_CONFIGS['server_port']))

        # TCP
        self.TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.TCPServerSocket.bind((SERVER_CONFIGS['server_host'], SERVER_CONFIGS['server_port']-1))
        self.TCPServerSocket.listen()
        self.chat_list_of_clients = []
        self.chat_log = ""
        threading.Thread(target=self.chat, daemon=True).start()

        self.output = []
        self.clients = {}
        self.users = {}
        self.bullets = {}
        self.Queue = queue.Queue()
        
        self.reciving_data_from_clients = Recive(self).start()
        self.broadcast_data_from_clients = Broadcast(self).start()
        
        self.auto_save_users = threading.Thread(target=self.auto_save_users_in_database,
                                                args=(False,),
                                                daemon=True).start()
        
    ################################################################################
    ################################# FOR TCP CHAT #################################
    ################################################################################
    def chat(self):
        while True:
            try:
                conn, addr = self.TCPServerSocket.accept()

                self.chat_list_of_clients.append(conn)

                print (str(addr[0]) + " connected")

                _thread.start_new_thread(self.clientthread,(conn,addr))
            except:
                pass

    def broadcast(self, message, connection):
        for clients in self.chat_list_of_clients:
            if clients != connection:
                try:
                    clients.send(message.encode())
                except:
                    clients.close()
                    self.remove(clients)

    def remove(self, connection):
        if connection in self.chat_list_of_clients:
            self.chat_list_of_clients.remove(connection)

    def clientthread(self, conn, addr):
        conn.send(b"Hello from ZimCa chat system!")
        while True:
                try:
                    message = conn.recv(2048)
                    if message:
                        message_to_send = message.decode()
                        self.chat_log += message_to_send + '\n'
                        self.broadcast(message_to_send, conn)
                    else:
                        self.remove(conn)
                except:
                    continue
    ################################################################################
    ################################# FOR TCP CHAT #################################
    ################################################################################	

    def auto_save_users_in_database(self, exit_after=False):
        # Every 2 min
        while True:
            users = copy.deepcopy(self.users)
            for user in users:
                try:
                    if 'rehealing' in self.users[user]:
                        self.users[user]['cordinates'] = [-850, -390]
                    Users.update_user_game_data(self.users[user])
                    self.output.append(f"User {user} auto saved in database!")
                    print(f"User {user} auto saved in database!")
                except Exception as ex:
                    print(ex)
            if exit_after:
                break
            time.sleep(120)
            
    def save_user_in_database(self, user):
        try:
            if 'rehealing' in self.users[user]:
                self.users[user]['cordinates'] = [-850, -390]
            Users.update_user_game_data(self.users[user])
            print(f"User {user} saved in database!")
            self.output.append(f"User {user} saved in database!")
        except Exception as ex:
            print(ex)
    
    def reheal_player(self, user):
        while True:
            try:
                self.users[user]['health'] += 1
                time.sleep(0.5)
                if self.users[user]['health'] >= 100:
                    self.users[user]['health'] = 100
                    break
            except:
                try:
                    # If something go wrong remove player from bed
                    if user in self.users:
                        self.users[user]['cordinates'] = [-850, -390]
                except:
                    pass
                break
        print(f"User {user} rehealed successfully.")
        self.output.append(f"User {user} rehealed successfully.")
    
    
    def send_to_client(self, msg, client_addres):
        message =  pickle.dumps(msg)
        self.UDPServerSocket.sendto(message, client_addres)

    def run(self):
        while True:
            time.sleep(1)
            if input("") == "exit":
                break
            
        old_chat_log = []
        try:
            with open('chat_log.txt', 'r') as f:
                old_chat_log = f.readlines()
        except:
            pass
            
        with open('chat_log.txt', 'w') as f:
            for line in old_chat_log:
                f.write(line)
            f.write(self.chat_log)

if __name__ == "__main__":
    server = GameServer()
    server.start()
    
            







