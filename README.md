# irc

This project uses TCP and Python to create a multi-client / single-server interface for chatrooms (i.e. Internet Relay Chat or IRC). 
The user can specify their username before joining multiple chatrooms.

To start, excecute the server process first: 

    $python server.py
    
Next, start a client process: 

    $python client.py

Multiple terminals can exceute the client process to facilitate distinct chatroom users. 
The following client to server commands are available:

    /join <str chatroom_name>: connects you to chatroom_name chatroom
    /msg <str chatroom_name> <str msg>: sends your message to chatroom_name chatroom
    /pmsg <str username> <str msg>: sends your message to the user username
    /leave <str chatroom_name>: removes you from chatroom_name chatroom
    /ls <str chatroom_name>: lists all members of chatroom_name chatroom
    /ls_all: lists all available chatrooms
    /fsend <str username> <str file.extension>: sends a file to the user username
    /dc: disconnects you from the server
    /help: prints these messages again

All current source code can be found under the /src folder; /rev contains older, experimental, and/or non-working source code.
