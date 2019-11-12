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
          print ("From chatroom: ", msg)

print("Enter 1 to create a room, 2 to join a room, and 3 to list the rooms. Type exit to leave.")
while True:
  #in_data =  client.recv(1024)
  #print("From Server :" ,in_data.decode())
  out_data = input()
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
    print("Joining room number ", out_data, ", enter EXIT to leave the room")
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
	
client.close()
