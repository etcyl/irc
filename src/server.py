import socket, threading

rooms = []

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
		
    def run(self):
        print ("Connection from : ", clientAddress)
        #self.csocket.send(bytes("Enter 1 to create a room, 2 to join a room, 3 to leave a room, and 4 to list the rooms.",'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(1024)
            msg = data.decode()
            if msg == 'exit':
              break
            elif msg == '1':
              print("create room detected")
            elif msg == '2':
              print("join room detected")
            elif msg == '3':
              print("leave room detected")
            elif msg == '4':
              print("list rooms detected")
            print ("from client", msg)
            self.csocket.send(bytes(msg,'UTF-8'))
        print ("Client at ", clientAddress , " disconnected...")
		
LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
