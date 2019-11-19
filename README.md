# irc

This project uses TCP and Python to create a multi-client / single-server interface for chatrooms. 
The user can specify their username before joining multiple chatrooms.

To start, excecute the server process first: $python server.py
Next, start a client process: $python client.py

Multiple terminals can exceute the client process to facilitate distinct chatroom users. 
The following client to server commands are available:

    /join <str chatroom_name>: connects you to chatroom_name chatroom
    /msg <str chatroom_name> <str msg>: sends your message to chatroom_name chatroom
    /leave <str chatroom_name>: removes you from chatroom_name chatroom
    /ls <str chatroom_name>: lists all members of chatroom_name chatroom
    /ls_all: lists all available chatrooms
    /dc: disconnects you from the server
    /help: prints these messages again
