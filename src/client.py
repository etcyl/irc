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

class InputThread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
		
    def run(self):
        msg = ''
        while True:
          data = self.client.recv(1024)
          msg = data.decode()
          if msg=='EXIT':
            break
          print ("From chatroom: ", msg)

print("Enter 1 to create a room, 2 to join a room, 3 to leave a room, and 4 to list the rooms. Type exit to leave.")
while True:
  #in_data =  client.recv(1024)
  #print("From Server :" ,in_data.decode())
  out_data = input()
  if out_data == '1':
    print("Create room detected.")
    client.sendall(bytes(out_data,'UTF-8'))
    stream_thread = InputThread(client)
    stream_thread.start()
    while True:
      print("in while loop")
      #in_data = client.recv(1024)
      out_data = input()
      client.sendall(bytes(out_data, 'UTF-8'))
      #in_data = client.recv(1024)
      #print("From chatroom :", in_data.decode())
      #if out_data == 'EXIT':
        #break
        #print("Leaving room ... ")
  elif out_data == '2':
    client.sendall(bytes(out_data,'UTF-8'))
    print("Join room detected. Please enter the room number you want to join: ")
    out_data = input()
    client.sendall(bytes(out_data, 'UTF-8'))
    in_room = 1
    print("Joining room number ", out_data, "enter EXIT to leave the room")
    while in_room == 1:
      out_data = input()
      client.sendall(bytes(out_data, 'UTF-8'))
      in_data = client.recv(1024)
      print("From chatroom :", in_data.decode())
      #out_data = input()
      #client.sendall(bytes(out_data, 'UTF-8'))
      if out_data == 'EXIT':
        in_room = 0
        print("Leaving room ... ")
  elif out_data == '3':
    print("Not currently in a room, can't leave room.")
    client.sendall(bytes(out_data,'UTF-8'))
  elif out_data == '4':
    client.sendall(bytes(out_data, 'UTF-8'))
    in_data = client.recv(1024)
    print(in_data.decode())
  #client.sendall(bytes(out_data,'UTF-8'))
  if out_data=='exit':
    break
	
client.close()
