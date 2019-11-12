"""
Some source code modified from: http://net-informations.com/python/net/thread.htm
"""

import socket, threading

in_room = 0
rooms = []

class room():
    def __init__(self, room_number):
        self.room_number = room_number
        self.rlist = [] #List to keep track of who is in the room
	
    def update_rlist(self, clientAddr, clientSocket):
        self.rlist.append([clientAddr, clientSocket])

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddr = clientAddress
        print ("New connection added: ", clientAddress)
		
    def run(self):
        print ("Connection from : ", clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(1024)
            msg = data.decode()
            if msg == 'exit':
              break
            elif msg == '1':
              print("create room detected")
              in_room = 1
              room_num = data.decode()
              new_room = room(room_num)
              print("New room created.")
              new_room.update_rlist(self.caddr, self.csocket)
              rooms.append(new_room)
              while True:
                print("In loop")
                data = self.csocket.recv(1024)
                msg = data.decode()
                if msg == 'EXIT':
                  print("EXIT msg")
                  break
                for i in range(len(rooms[0].rlist)):
                  rooms[0].rlist[i][1].send(bytes(msg, 'UTF-8'))
            elif msg == '2':
              print("join room detected")
              rooms[0].update_rlist(self.caddr, self.csocket)
              in_room = 1
              while True:
                data = self.csocket.recv(1024)
                msg = data.decode()
                if msg == 'EXIT':
                  rooms[0].rlist.pop()
                  break
                for i in range(len(rooms[0].rlist)):
                  rooms[0].rlist[i][1].send(bytes(msg, 'UTF-8'))
            elif msg == '3':
              print("list rooms detected")
            """elif msg == '4':
              print("list rooms detected")
              #self.csocket.send(bytes("Here are the current rooms",'UTF-8'))
              if len(rooms) == 0:
                self.csocket.send(bytes("No rooms available.", 'UTF-8'))
              else:
                for i in range(len(rooms)):
                  self.csocket.send(bytes(i, 'UTF-8'))
            #print ("from client", msg)
            #self.csocket.send(bytes(msg,'UTF-8'))"""
        print ("Client at ", clientAddress , " disconnected...")
		
LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")

while True:
    print("Len of rooms is: ", len(rooms))
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
