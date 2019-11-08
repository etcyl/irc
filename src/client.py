import socket

SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
#client.sendall(bytes("This is from Client",'UTF-8'))
in_room = 0

print("Enter 1 to create a room, 2 to join a room, 3 to leave a room, and 4 to list the rooms. Type exit to leave.")
while True:
  #in_data =  client.recv(1024)
  #print("From Server :" ,in_data.decode())
  out_data = input()
  if out_data == '1':
    print("Create room detected.")
    client.sendall(bytes(out_data,'UTF-8'))
  if out_data == '2':
    #client.sendall(bytes(out_data,'UTF-8'))
    print("Join room detected. Please enter the room number you want to join: ")
    out_data = input()
    client.sendall(bytes(out_data, 'UTF-8'))
    in_room = 1
    while in_room == 1:
      in_data = client.recv(1024)
      print("From chatroom :", in_data.decode())
      out_data = input()
      client.sendall(bytes(out_data, 'UTF-8'))
      if out_data == 'exit':
        in_room = 0
  #client.sendall(bytes(out_data,'UTF-8'))
  if out_data=='exit':
    break
client.close()
