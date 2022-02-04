import socket
from _thread import *
import signal

ADDR = '127.0.0.1'
PORT = 9999

clients = []
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind((ADDR, PORT))
server_sock.listen()
def handle_client(client_sock, addr) :
	name = client_sock.recv(1024).decode()
	print("Connected by: %s at %s" %(name, addr[0]))
	while True :
		try :
			data = client_sock.recv(1024).decode()
			if not data :
				print("Disconnected by " + name)
				break
			print("%s > %s" %(name, data))
			send_data = "%s > %s" %(name, data)
			for client in clients:
				if(client!=client_sock):
					client.send(send_data.encode())
		except ConnectionResetError as e :
			print("Disconnected by %s" % name)
			break
	if client_sock in clients :
		clients.remove(client_sock)
		print('나간 참가자 : ',len(clients))
	client_sock.close()
def sigint_handler(signo, frame) :
	server_sock.close()
	print("Server Closed...\n")
	exit()
signal.signal(signal.SIGINT, sigint_handler)
print("서버 시작")
try:
	while True :
		client_socket, addr = server_sock.accept()
		clients.append(client_socket)
		start_new_thread(handle_client, (client_socket, addr))
		print("현재 참가자는 "+str(len(clients))+"명 입니다")
finally:
	server_sock.close()
