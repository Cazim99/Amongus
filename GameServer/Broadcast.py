import threading
from Bullet import Bullet


class Broadcast(threading.Thread):
    
    BYTES_LEN_RECIVING = 3072
    
    def __init__(self, root):
        super().__init__(target='run', daemon=True)
        self.root = root
        self.queue = root.Queue
        self.clients = root.clients
        self.users = root.users
    

    def update_user(self, user):
        if user['username'] in self.users:
            self.users[user['username']]['cordinates'] = user['cordinates']
            self.users[user['username']]['image'] = user['image']
            self.users[user['username']]['facing'] = user['facing']
            self.users[user['username']]['angle'] = user['angle']
            self.users[user['username']]['movespeed'] = user['movespeed']
            self.users[user['username']]['inside_ship'] = user['inside_ship']

            if 'bullets' in user:
                for bullet in user['bullets']:
                    bullet_thread = Bullet(self.root, bullet['x'], bullet['y'], user['username'], bullet['angel'])
                    bullet_thread.start()
    
    def run(self):
        while True:
            while not self.root.Queue.empty():
                try:
                    user, address = self.queue.get()
                    
                    try: # becaus maybe player before kick/ban send some other data, we will try this until all user data from queue will be loaded
                        if 'kicked' in self.users[user['username']]:
                            self.users.pop(user['username'])
                            self.root.send_to_client('[KICKED]', address)
                            continue # Skip because player is kicked
                        elif 'baned' in self.users[user['username']]:
                            self.users.pop(user['username'])
                            self.root.send_to_client('[BANED]', address)
                            continue # Skip because player is baned
                    except:
                        continue 


                    if 'disconnected' in self.users[user['username']]:
                        try: # becaus maybe player before disconnect message send some other data, we will try this until all user data from queue will be loaded
                            self.users.pop(user['username'])
                        except:
                            pass
                        continue # Skip because player is disconnected
                    
                    if user is not None and 'username' in user:
                        if user['username'] not in self.clients: # Add user ip addres in clients if dont exists
                            self.clients[user['username']] = address
                        else:
                            if self.clients[user['username']] != address: # Check if player maybe changed ip address
                                self.clients[user['username']] = address
                        
                        self.update_user(user)# Update player new position, facing, and current image
                        
                        for client in self.clients:
                            self.root.send_to_client({'users':self.users,
                                                      'bullets':self.root.bullets}, self.clients[client])

                except Exception as ex:
                    self.root.output.append(ex)