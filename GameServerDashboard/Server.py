import socket
import pickle
import threading
import time
import os

class Server(threading.Thread):
    
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    BYTES_LEN = 3072
    
    running = True
    online = False
    data_from_server = ""
    
    def __init__(self, server_configs):
        self.serverAddress = (server_configs[0], server_configs[1])
        super().__init__(target="run", daemon=True)
        
    def run(self):
        self.send_to_server("ADMINDASHBOARD::")
        while self.running:
            try:
                self.online = True
                self.data_from_server = self.recive_from_server()['data']
                time.sleep(1) # Wait 1 secounds before next server data update request
                self.send_to_server("ADMINDASHBOARD::")
            except (Exception,TimeoutError) as ex:
                self.online = False
                print(ex)
                self.send_to_server("ADMINDASHBOARD::")
                time.sleep(1)
                
    def connect_to_server(self):
        self.start()

    def send_to_server(self, msg):
        message = msg
        message = pickle.dumps(message)
        self.UDPClientSocket.sendto(message, self.serverAddress)

    def recive_from_server(self):
        respond = self.UDPClientSocket.recvfrom(Server.BYTES_LEN)
        data = pickle.loads(respond[0])
        address = respond[1]
        return {'data':data, 'address':address}