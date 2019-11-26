"""
Some source code modified from: http://net-informations.com/python/net/thread.htm
"""

import socket, threading, sys

# Client-side init
server_dc = 0
SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.setblocking(True)

# Process receiving server data separetely from input from the user
# This allows for the most current chatroom messages to display regardless of the user's input
class InputThread(threading.Thread): # InputThread inherits properties from the Thread class
    def __init__(self, client):
        threading.Thread.__init__(self) # Thread init
        self._stop_event = threading.Event() # Function to stop processing work in this thread
        self.client = client # Client socket to receive data from the sderver

    def stop(self): # Stops the thread from doing further work
        self._stop_event.set()

    def run(self):
        msg = '' # Initialize the variable as a string so it can hold the server response
        while True: # Continuously loop until the client or server stop / crash, receiving server responses
          try: # The socket could be broken if the server crashes
            data = self.client.recv(1024)
            msg = data.decode()
            if msg == '/leave':
              print("Leaving room ... ")
            elif msg == '/DC' or msg == '':
              print("Server disconnecting ... ")
              server_dc = 1
              self.client.shutdown(socket.SHUT_RDWR)
              self.client.close()
              exit(0)
            elif msg[0:6] == '/fsend':
              print("Downloading file ... ")
              split_msg = msg.split()
              file_name = split_msg[1]
              file_to_download = open(file_name, "wb")
              done = 0
              while done == 0:
                  print("Receiving file from user ... ")
                  data = self.client.recv(1024)
                  is_done = list(data)
                  if is_done[-5:] == [47, 78, 85, 76, 76]:
                      print("Done receiving file from user.")
                      done = 1
                      break
                  file_to_download.write(data)
              file_to_download.close()
            else:
              print (msg)
          except socket.error as e:
            print("Socket error, possible server crash detected, enter any alphanumeric value to quit ...")
            server_dc = 1
            exit(0)

# Tells the user what their options are to receive meaningful replies from the server
def print_help_menu():
    print("Welcome to the chatroom app.")
    print("The following cmds are available: ")
    print("/join <str chatroom_name>: connects you to chatroom_name chatroom,")
    print("/msg <str chatroom_name> <str msg>: sends your message to chatroom_name chatroom,")
    print("/pmsg <str username> <str msg>: sends a private message to the user username,")
    print("*note that /pmsg only works for users in chatrooms*")
    print("/leave <str chatroom_name>: removes you from chatroom_name chatroom,")
    print("/ls <str chatroom_name>: lists all members of chatroom_name chatroom,")
    print("/ls_all: lists all available chatrooms,")
    print("/dc: disconnects you from the server.")
    print("/help: prints these messages again.")
    return

print_help_menu() # Show the user what their options are

# Store username for the user's session on the server
print("Please enter your username: ")
username = input()
to_server = "name: " + username
client.sendall(bytes(to_server, 'UTF-8'))
print("Username is: ", to_server[0: 0:] + to_server[5 + 1 ::])

# Start a separate thread to process data received from the server
# This way the user can see messages from the server as they are sent while
# the user is still entering their selection
stream_thread = InputThread(client)
stream_thread.start()

# Continously loop detecting server crashes and the user's selection
while True:
  if server_dc == 1:
    print("Server shutdown detected ... ")
    stream_thread.stop()
    exit(0)
  try:
    to_server = input()
    if to_server[0:5] == '/help':
      print_help_menu()
    elif to_server[0:6] == '/fsend':
      client.sendall(bytes(to_server,'UTF-8'))
      split_msg = to_server.split()
      user_to_send = split_msg[1]
      header_len = len('/fsend') + len(user_to_send)
      file_name = str(to_server[0: 0:] + to_server[header_len + 2 ::])
      print("Filename is: ", file_name)
      file_to_send = open(file_name, "rb")
      data = file_to_send.read(1024)
      while data:
          print("Sending file to server ... ")
          data = bytes(data)
          client.send(data)
          data = file_to_send.read(1024)
      print("Done sending file to sever.")
      file_to_send.close()
      to_server = '/NULL'
      client.sendall(bytes(to_server, 'UTF-8'))
    else:
      client.sendall(bytes(to_server,'UTF-8'))
    if to_server == '/dc' or server_dc == 1:
      stream_thread.stop()
      print("Disconnecting from server ... ")
      stream_thread.stop()
      sys.exit(0)
  except (KeyboardInterrupt, ValueError, BrokenPipeError):
    print("Disconnecting from server ...")
    to_server = '/dc'
    try:
      client.sendall(bytes(to_server,'UTF-8'))
    except BrokenPipeError:
      pass
    finally:
      print("Closing ... ")
      stream_thread.stop()
      client.close()
      exit(0)
