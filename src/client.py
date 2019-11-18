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
        self._stop_event = threading.Event()
        self.client = client

    def stop(self):
        self._stop_event.set()		

    def run(self):
        msg = ''
        while True:
          try:
            data = self.client.recv(1024)
            msg = data.decode()
            if msg == '/leave':
              print("Leaving room ... ")
            elif msg == '/DC':
              print("Server disconnecting ... ")
              break
            print (msg)
          except:
            break

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

stream_thread = InputThread(client)
stream_thread.start()
while True:
  to_server = input()
  client.sendall(bytes(to_server,'UTF-8'))
  if to_server == '/dc':
    stream_thread.stop()
    print("Disconnecting from server ... ")
    break

client.close()
