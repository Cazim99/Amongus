import socket
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


server.bind(('localhost', 9999))

server.listen()

list_of_clients = []

def clientthread(conn, addr):
	conn.send(b"Hello from ZimCa chat system!")

	while True:
			try:
				message = conn.recv(2048)
				if message:
					message_to_send = message.decode()
					broadcast(message_to_send, conn)

				else:
					remove(conn)

			except:
				continue

def broadcast(message, connection):
	for clients in list_of_clients:
		if clients != connection:
			try:
				clients.send(message.encode())
			except:
				clients.close()
				remove(clients)

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
	conn, addr = server.accept()

	list_of_clients.append(conn)

	print (addr[0] + " connected")

	start_new_thread(clientthread,(conn,addr))	

conn.close()
server.close()
