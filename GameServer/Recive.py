import pickle
import threading

class Recive(threading.Thread):
    
    BYTES_LEN_RECIVING = 3072
    
    def __init__(self, root):
        super().__init__(target='run', daemon=True)
        self.root = root
        self.queue = root.Queue
        self.clients = root.clients
        self.users = root.users
        
    def run(self):
        while True:
            try:
                user, address = self.recive_from_client()
                
                # ==================================== DASHBOARD =============================================
                # ==================================== DASHBOARD =============================================
                # acceskey:command:otherdata
                if 'ADMINDASHBOARD' in user:
                    if '[KICK]' in user:
                        kicked_user = user.split(":")[2]
                        self.root.output.append(f"User {kicked_user} kicked !")
                        print(f"User {kicked_user} kicked !")
                        try:
                            self.root.save_user_in_database(kicked_user)
                        except:
                            pass
                        self.users[kicked_user]['kicked'] = True
                    elif '[BAN]' in user:
                        baned_user = user.split(":")[2]
                        self.root.output.append(f"User {baned_user} baned !")
                        print(f"User {baned_user} baned !")
                        self.users[baned_user]['baned'] = True
                        self.root.save_user_in_database(baned_user)
                    elif '[COMMAND]' in user:
                        command = user.split(":")[2]
                        if command.startswith('set health'):
                            command = command.strip()
                            command = command.replace('set health','').strip()
                            try:
                                username = command.split(",")[0]
                                new_health = int(command.split(",")[1])
                                if username in self.users:
                                    self.users[username]['health'] = new_health
                            except Exception as ex:
                                print(ex)
                        elif command.startswith('set cordinates'):
                            command = command.strip()
                            command = command.replace("set cordinates", '').strip()
                            try:
                                username = command.split("/")[0]
                                new_cordinates = command.split("/")[1]
                                self.root.send_to_client(f'[RESPAWN]:{new_cordinates}', self.clients[username])
                            except Exception as ex:
                                print(ex)
                    else:
                        data_for_server_dashboard = {
                            'players':self.root.users,
                            'output':self.root.output,
                        }
                        self.root.send_to_client(data_for_server_dashboard, address)
                        self.root.output = []
                    continue
                # ==================================== DASHBOARD =============================================
                # ==================================== DASHBOARD =============================================

                # DISCONNECT PLAYER
                if 'disconnected' in user:
                    self.users[user['disconnected'] ]['disconnected'] = True
                    print(f"User {user['disconnected']} disconnected !")
                    self.root.output.append(f"User {user['disconnected']} disconnected !")
                    self.root.save_user_in_database(user['disconnected'])
                    continue
                
                # PLAYER IN HOSPITAL
                if 'inhospital' in user:
                    self.users[ user['inhospital'] ]['rehealing'] = True
                    threading.Thread(target=self.root.reheal_player,
                                     args=(user['inhospital'],), 
                                     daemon=True).start()
                    continue
                
                ## CHECK IF PLAYER IS ALREADY CONNECTED OR MAYBE CONNECTED BEFORE 
                if user['username'] in self.users:
                    if 'facing' not in user: # Means player was playing before , but now want to play again we just send him last data
                        self.root.send_to_client({'users':self.users,
                                             'bullets':self.root.bullets}, address)
                        print(f"User {user['username']} connected !")
                        self.root.output.append(f"User {user['username']} connected !")
                    else:
                        # let user continue from where he/she stoped playing
                        self.queue.put((user, address)) 
                else:
                    # INITALIZE USER
                    new_user = {}
                    new_user['username'] = user['username']
                    new_user['cordinates'] = user['cordinates']
                    new_user['health'] = user['health']
                    new_user['movespeed'] = user['movespeed']
                    new_user['facing'] = False
                    new_user['image'] = 'idle.png'
                    new_user['angle'] = user['angle']
                    new_user['inside_ship'] = user['inside_ship']
                    self.users[new_user['username']] = new_user
                    self.root.send_to_client({'users':self.users,
                                             'bullets':self.root.bullets}, address)
                    print(f"User {new_user['username']} connected !")
                    self.root.output.append(f"User {new_user['username']} connected !")
            except Exception as ex:
                pass
    
    def recive_from_client(self):
        data, address = self.root.UDPServerSocket.recvfrom(Recive.BYTES_LEN_RECIVING)
        data = pickle.loads(data)
        return [data, address]