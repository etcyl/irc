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

    def get_RNum(self):
        return self.room_number

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddr = clientAddress
        self.username = ""
        print ("New connection added: ", clientAddress)
		
    def set_username(self, u_name):
        self.username = u_name

    def run(self):
        print ("Connection from : ", clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(1024)
            msg = data.decode()
            #print("msg is: ", msg)
            #print("msg[0:4] is: ", msg[0:4])
            if msg[0:4] == "name":
              user_name = msg[0: 0:] + msg[5 + 1::]
              self.set_username(user_name)
              print("Username is: ", user_name)
"""
            if msg == 'exit':
              break
            elif msg == '1':
              print("create room detected")
              room_num = len(rooms)
              print("Room num is: ", room_num)
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
                for i in range(len(rooms[room_num].rlist)):
                  rooms[room_num].rlist[i][1].send(bytes(msg, 'UTF-8'))
            elif msg == '2':
              print("join room detected")
              #rooms[0].update_rlist(self.caddr, self.csocket)
              data = self.csocket.recv(1024)
              room_num = data.decode()
              room_num = int(room_num)
              rooms[room_num].update_rlist(self.caddr, self.csocket)
              while True:
                data = self.csocket.recv(1024)
                msg = data.decode()
                if msg == 'EXIT':
                  rooms[room_num].rlist.remove((self.caddr, self.csocket))
                  break
                for i in range(len(rooms[room_num].rlist)):
                  rooms[room_num].rlist[i][1].send(bytes(msg, 'UTF-8'))
            elif msg == '3':
              print("list rooms detected")
              list_rooms = []
              for i in range(len(rooms)):
                room_number = rooms[i].get_RNum()
                list_rooms.append(room_number)
              list_rooms = str(list_rooms)
              self.csocket.send(bytes(list_rooms, 'UTF-8'))
        print ("Client at ", clientAddress , " disconnected...")
"""		
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
