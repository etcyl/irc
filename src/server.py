"""
Some source code modified from: http://net-informations.com/python/net/thread.htm
"""

import socket, threading

rooms = []
threads = []

class user():
    def __init__(self, clientAddress, clientsocket, name):
        self.clientAddress = clientAddress
        self.socket = clientsocket
        self.name = name

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def get_name(self):
        return self.name

class room():
    def __init__(self, room_name):
        self.room_name = room_name
        self.rlist = [] #List to keep track of who is in the room
	
    def update_rlist(self, user):
        self.rlist.append(user)

    def get_room_name(self):
        return self.room_name

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddr = clientAddress
        self.username = ""
        self._stop_event = threading.Event()
        print ("New connection added: ", clientAddress)

    def stop(self):
        self._stop_event.set()
    
    def set_username(self, u_name):
        self.username = u_name

    def print_help_menu(self):
        print("Welcome to the chatroom app.")
        print("The following cmds are available: ")
        print("/join <str chatroom_name>: connects you to chatroom_name chatroom,")
        print("/msg <str chatroom_name> <str msg>: sends your message to chatroom_name chatroom,")
        print("/leave <str chatroom_name>: removes you from chatroom_name chatroom,")
        print("/ls <str chatroom_name>: lists all members of chatroom_name chatroom,")
        print("/ls_all: lists all available chatrooms,")
        print("/dc: disconnects you from the server.")
        print("/help: prints these messages again.")
        return

    def run(self):
        print ("Connection from : ", clientAddress)
        msg = ''
        while True:
            try:
                data = self.csocket.recv(1024)
                msg = data.decode()
            except KeyboardInterrupt:
                print("KeyboardInterrupt also detected")
                to_client = '/DC'
                #self.csocket.send(bytes(to_clien, 'UTF-8'))
                for i in range(len(rooms)):
                    for j in range(len(rooms[i].rlist)):
                        print("Sending message to client: ", rooms[i].rlist[i].get_name())
                        rooms[i].rlist[j].send(bytes(to_client, 'UTF-8'))
                self.stop()
                exit(0)
                break
            if msg[0:4] == "name":
              user_name = msg[0: 0:] + msg[5 + 1::]
              self.set_username(user_name)
              print("Username is: ", user_name)
            if msg == '/dc':
              print("Server disconnecting ... ")
              for i in range(len(rooms)):
                  for j in range(len(rooms[i].rlist)):
                      if rooms[i].rlist[j].get_name() == self.username:
                          rooms[i].rlist = [user for user in rooms[i].rlist if user.get_name() != self.username]
              self.stop()
              break
            elif msg[0:7] == '/create':
              print("create room detected")
              room_name = msg[0: 0:] + msg[7 + 1::]
              print("Room name is: ", room_name)
              new_room = room(room_name)
              print("New room created.")
              new_user = user(self.caddr, self.csocket, user_name)
              new_room.update_rlist(new_user)
              rooms.append(new_room)
            elif msg[0:5] == '/join':
              print("join room detected")
              room_found = 0
              for i in range(len(rooms)):
               print("Room name is: ", rooms[i].get_room_name())
               if rooms[i].get_room_name() == msg[0: 0:] + msg[5 + 1::]:#msg[7:-1]:
                 new_user = user(self.caddr, self.csocket, user_name)
                 rooms[i].update_rlist(new_user)
                 room_found = 1
                 break
              if room_found == 1:
                pass
              else:
                room_name = msg[0: 0:] + msg[5 + 1::]#msg[7:-1]
                print("Room name is: ", room_name)
                new_room = room(room_name)
                print("New room created.")
                new_user = user(self.caddr, self.csocket, user_name)
                new_room.update_rlist(new_user)
                rooms.append(new_room)
            elif msg[0:6] == '/leave':
                
            elif msg == '/ls_all':
              print("list rooms detected")
              list_rooms = []
              for i in range(len(rooms)):
                room_number = rooms[i].get_room_name()
                list_rooms.append(room_number)
              list_rooms = str(list_rooms)
              self.csocket.send(bytes(list_rooms, 'UTF-8'))
            elif msg[0:3] == '/ls':
              print('list names detected')
              room_names = []
              room_name = msg[0: 0:] + msg[3 + 1::]
              for i in range(len(rooms)):
                  if rooms[i].get_room_name() == room_name:
                    for j in range(len(rooms[i].rlist)):
                      person = rooms[i].rlist[j].get_name()
                      room_names.append(person)
                    break
              room_names = str(room_names)
              self.csocket.send(bytes(room_names, 'UTF-8'))
            elif msg[0:4] == '/msg':
              print('send message detected')
              user_is_in_chatroom = 0
              split_msg = msg.split()
              room_name = split_msg[1]
              #Check that the user is in the chatroom
              for i in range(len(rooms)):
                  if rooms[i].get_room_name() == room_name:
                      for j in range(len(rooms[i].rlist)):
                          if rooms[i].rlist[j].get_name() == self.username:
                              user_is_in_chatroom = 1
              header_len = len(split_msg[0]) + len(split_msg[1])
              to_send = msg[0: 0: ] + msg[header_len + 2 ::]
              for i in range(len(rooms)):
                  if rooms[i].get_room_name() == room_name and user_is_in_chatroom == 1:
                      for j in range(len(rooms[i].rlist)):
                          rooms[i].rlist[j].socket.send(bytes("(" + room_name + ") " + self.username + ": " + to_send, 'UTF-8'))
                      break
        print ("(", user_name, ")", "Client at: ", clientAddress , " disconnected...")

LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started.")
print("Waiting for client request..")

while True:
    try:
      server.listen(1)
      clientsock, clientAddress = server.accept()
      newthread = ClientThread(clientAddress, clientsock)
      newthread.start()
      threads.append(newthread)
    except KeyboardInterrupt:
      print("KeyboardInterrupt detected ...")
      for i in range(len(threads)):
          threads[i].stop()
      to_client = '/DC'
      print("help message")
      #clientsock.send(bytes(to_client, 'UTF-8'))
      for i in range(len(rooms)):
          for j in range(len(rooms[i].rlist)):
              print("Sending '/DC' to user: ", rooms[i].rlist[j].get_name())
              rooms[i].rlist[j].socket.send(bytes(to_client, 'UTF-8'))
              rooms[i].rlist[j].socket.shutdown(socket.SHUT_RDWR)
              rooms[i].rlist[j].socket.close()
      exit(0)
