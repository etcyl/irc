"""
Some source code modified from: http://net-informations.com/python/net/thread.htm
"""


import socket, threading

SERVER = "127.0.0.1"
PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
#client.sendall(bytes("This is from Client",'UTF-8'))
client.setblocking(True)
in_room = 0

class InputThread(threading.Thread): # Process receiving server data separetely from input from the user
    def __init__(self, client):      # This allows for the most current chatroom messages to display regardless of the user's input 
        threading.Thread.__init__(self)
        self.client = client
		
    def run(self):
        msg = ''
        while True:
          data = self.client.recv(1024)
          msg = data.decode()
          if msg=='EXIT':
            print("Leaving room ... ")
            break
          print (msg)

print("Welcome to the chatroom app.")
print("The following cmds are available: ")
print("/join <str chatroom_name>: connects you to chatroom_name chatroom,")
print("/msg <str chatroom_name>: sends your message to chatroom_name chatroom,")
print("/leave <str chatroom_name>: removes you from chatroom_name chatroom,")
print("/ls <str chatroom_name>: lists all members of chatroom_name chatroom,")
print("/ls_all: lists all available chatrooms,")
print("/dc: disconnects you from the server.")

print("Please enter your username: ")
username = input()
to_server = "name: " + username
client.sendall(bytes(to_server, 'UTF-8'))
print("Username is: ", to_server[0: 0:] + to_server[5 + 1 ::])

"""
while True:
  if out_data == '1': # Client wants to create a room
    print("Create room detected.")
    client.sendall(bytes(out_data,'UTF-8'))
    stream_thread = InputThread(client)
    stream_thread.start()
    while True:
      out_data = input()
      if out_data == 'EXIT':
       break
      client.sendall(bytes(out_data, 'UTF-8'))
  elif out_data == '2': # Client wants to join an existing room
    client.sendall(bytes(out_data,'UTF-8'))
    print("Join room detected. Please enter the room number you want to join: ")
    out_data = input()
    client.sendall(bytes(out_data, 'UTF-8'))
    print("Joining room number ", out_data, ", type EXIT to leave the room")
    stream_thread = InputThread(client)
    stream_thread.start()
    while True:
      out_data = input()
      if out_data == 'EXIT':
        break
      client.sendall(bytes(out_data, 'UTF-8'))
  elif out_data == '3': # Client wants to list the current rooms
    client.sendall(bytes(out_data, 'UTF-8'))
    in_data = client.recv(1024)
    print(in_data.decode())
  if out_data=='exit': # Client wants to exit the program
    break
"""	
client.close()
