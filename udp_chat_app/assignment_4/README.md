# ICS 460 Assignment 4 - UDP Chat Application

---

    title: UDP Chat Application
    author: Momodou Jallow
    created on: 10/26/2022

---

## Summary

Implementation of an an online chat application using UDP. In this application, the client determines the operation to be performed: public messaging or direct messaging. The server side handles multiple simultaneous client connections and responds appropriately to the specific commands sent by the clients. The specifics of the protocol are detailed below.

## Included files

server code: chatserver.py
client code: chatclient.py
file: chat_users.json -- data storage for chat client user login info

## Protocol Description

_There are two types of message frames: 1) data message and 2) command message. A data message is exchanged between clients (i.e., the Public and Direct messages described in the following online chat room protocol). A command message is exchanged between a client and the server (e.g., operation, acknowledgment, confirmation messages described below). Define the message format to encode the message type. For example, the first character of the message can be used to distinguish between the two types of messages (e.g., "C" for command message and "D" for data message)._

1.  The server opens a port, creates the UDP socket, goes into the "wait for connection" state, and actively listens for socket connections.
2.  Instruction Section below for details.
3.  The client logs into the system by connecting to the server on the appropriate port.
4.  The client sends the username.
5.  The server checks whether it is a new user or an existing user and requests a password.
6.  The client sends the password.
7.  The server either registers a new user or checks to see if the password matches. The server then sends the acknowledgment to the client.
8.  The server continues to wait for an operation command from a client or a new client connection.
9.  The client goes into the "prompt user for operation" state and prompts the user for operation.
10. The client passes operation (PM: Public Message, DM: Direct Messaging, EX: Exit) to the server.
    Operation is executed as follows:

            PM:

                The client sends an operation (PM) to broadcast a public message to all active clients (i.e., the clients who successfully log in to the system but have not exited yet).
                The server sends the acknowledgment back to the client to prompt for the message to be sent.
                The client sends the broadcast message to the server.
                The server receives the message and sends it to all other clients. Note: The server should keep track of the socket descriptors it has created for each client since the program began running. You can decide how to implement this tracking function.
                The server sends confirmation that the message was sent. Note: You can decide the content/format of the confirmation.
                The client receives the confirmation message.
                The client returns to the "prompt user for operation" state, and the server returns to the "wait for operation from client" state.
            DM:
                The client sends the operation (DM) to send a message to a specific client.
                The server sends the list of currently online users. Note: The server should keep track of all online users. You can decide how to implement this tracking function. We assume that any client can go offline by using operation (EX).
                The client receives the list of online users from the server.
                The client prompts the user to select the username of the target user.
                The client sends the target username and the message to the server.
                The server receives the above information and checks to make sure the target user exists/online.
                If the target user is online, the server forwards the message to the user. The server should do this by sending the message to the corresponding socket descriptor of the target user.
                The target user receives the message and displays it.
                The server sends confirmation that the message was sent or that the user did not exist. Note: You can decide the content/format of the confirmation.
                The client receives the confirmation message from the server.
                The client returns to the "prompt user for operation" state, and the server returns to the "wait for operation from client" state.
            EX:
                The client sends operation (EX) to close its connection with the server and end the program.
                The server receives the operation and closes the socket descriptor for the client.
                The server updates its tracking record on the socket descriptors of active clients and usernames of online users.
                The client should close the socket.

## Usage

First run the server and then run the client.

To star the server: python ./chatserver.py <port-number>
example

```
python ./chatserver.py 65015
```

To start client and make a request
python ./chatclient.py <server-name> <port-number> <username>

example:

```
python ./chatclient localhost 65015 momodou
```
