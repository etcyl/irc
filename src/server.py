"""
Some source code modified from: http://net-informations.com/python/net/thread.htm
"""

import socket, threading

rooms = []
user_list = []
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
    
    def get_username(self):
        return self.username

    def random_string(self, stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

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
        global user_list
        print ("Connection from : ", clientAddress)
        msg = ''
        while True:
            try:
                data = self.csocket.recv(1024)
                msg = data.decode()
            except (KeyboardInterrupt, OSError):
                print("Closing thread.")
                #for i in range(len(threads)):
                    #threads[i].stop()
                exit(0)
                break
            if msg[0:4] == "name":
              user_name = msg[0: 0:] + msg[5 + 1::]
              self.set_username(user_name)
              print("Username is: ", user_name)
              new_user = user(self.caddr, self.csocket, user_name)
              user_list.append(new_user)
            if msg == '/dc' or msg == '':
              print("Server disconnecting ... ")
              for i in range(len(rooms)): # Delete the user from all rooms they were in
                  for j in range(len(rooms[i].rlist)):
                      try:
                          if rooms[i].rlist[j].get_name() == self.username:
                              rooms[i].rlist = [user for user in rooms[i].rlist if user.get_name() != self.username]
                      except IndexError:
                          pass
              self.stop()
              break
            elif msg[0:7] == '/create':
              print("create room detected")
              user_already_in_room = 0
              room_exists = 0
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
               if rooms[i].get_room_name() == msg[0: 0:] + msg[5 + 1::]:
                 new_user = user(self.caddr, self.csocket, user_name)
                 rooms[i].update_rlist(new_user)
                 room_found = 1
                 break
              if room_found == 1:
                pass
              else:
                room_name = msg[0: 0:] + msg[5 + 1::]
                print("Room name is: ", room_name)
                new_room = room(room_name)
                print("New room created.")
                new_user = user(self.caddr, self.csocket, user_name)
                new_room.update_rlist(new_user)
                rooms.append(new_room)
            elif msg[0:6] == '/leave':
                room_found = 0
                room_name = msg[0: 0:] + msg[6 + 1::]
                for i in range(len(rooms)):
                    for j in range(len(rooms[i].rlist)):
                        if rooms[i].rlist[j].get_name() == self.username and rooms[i].room_name == room_name:
                            rooms[i].rlist = [user for user in rooms[i].rlist if user.get_name() != self.username]
                            room_found = 1
                if room_found == 1:
                  to_client = '/leave'
                else:
                  to_client = 'Room not found.'
                self.csocket.send(bytes(to_client, 'UTF-8'))
            elif msg == '/ls_all':
              print("list rooms detected")
              list_rooms = []
              for i in range(len(rooms)):
                room_number = rooms[i].get_room_name()
                list_rooms.append(room_number)
              list_rooms.sort()
              list_rooms = str(list_rooms)
              self.csocket.send(bytes(list_rooms, 'UTF-8'))
            elif msg[0:6] == '/fsend':
              split_msg = msg.split()
              user_to_send = split_msg[1]
              header_len = len(split_msg[0]) + len(split_msg[1])
              file_name = msg[0: 0:] + msg[header_len + 2 ::]
              for i in range(len(rooms)):
                  for j in range(len(rooms[i].rlist)):
                      if rooms[i].rlist[j].get_name() == user_to_send:
                          get_sender = 'Receiving file from user: ' + str(self.get_username())
                          rooms[i].rlist[j].socket.send(bytes(get_sender, 'UTF-8'))
                          rooms[i].rlist[j].socket.send(bytes('/fsend ' + file_name, 'UTF-8'))
                          done = 0
                          while done == 0:
                             print("Receiving ...")
                             data = self.csocket.recv(1024)
                             data = bytes(data)
                             is_done = list(data)
                             if is_done[-5:] == [47, 78, 85, 76, 76]:
                                 done = 1
                                 to_client = b'/NULL'
                                 rooms[i].rlist[j].socket.send(to_client)
                                 print("Finished sending file ...")
                                 get_sender = 'Done receiving file from user: ' + str(self.get_username())
                                 rooms[i].rlist[j].socket.send(bytes(get_sender, 'UTF-8'))
                                 break
                             print("Sending file ... ")
                             rooms[i].rlist[j].socket.send(data)
                          break
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
              room_names.sort()
              room_names = str(room_names)
              self.csocket.send(bytes(room_names, 'UTF-8'))
            elif msg[0:5] == '/pmsg':
              print('private message detected')
              user_found = 0
              split_msg = msg.split()
              user_to_msg = split_msg[1]
              print("user to msg is: ", user_to_msg)
              header_len = len(split_msg[0]) + len(split_msg[1])
              to_send = msg[0: 0:] + msg[header_len + 2 ::]
              for i in range(len(rooms)):
                  for j in range(len(rooms[i].rlist)):
                      if rooms[i].rlist[j].get_name() == user_to_msg:
                          user_found = 1
                          rooms[i].rlist[j].socket.send(bytes("(private message from " + self.username + "): " + to_send, 'UTF-8'))
                          break
              if user_found == 0:
                  to_send = "Username not found."
                  self.csocket.send(bytes(to_send, 'UTF-8'))
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
        try:
            print ("(", user_name, ")", "Client at: ", clientAddress , " disconnected...")
        except UnboundLocalError:
            print("User forced connection to close unexpectedly.")

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
      #for i in range(len(threads)):
          #threads[i].stop()
      to_client = '/DC'
      try: # Close connection to clients by sending the /DC command
          for k in range(len(user_list)):
              print("Sending /DC to user: ", user_list[k].get_name())
              user_list[k].socket.send(bytes(to_client, 'UTF-8'))
              user_list[k].socket.shutdown(socket.SHUT_RDWR)
              user_list[k].socket.close()
      except OSError:
          pass
      exit(0)
