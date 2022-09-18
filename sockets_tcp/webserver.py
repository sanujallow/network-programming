# Import socket module
from http.client import HTTPMessage, HTTPResponse
from socket import *
from http import HTTPStatus
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket
#Fill in start
localhost = '127.0.0.1'
assigned_port = 65015
serverSocket.bind((localhost, assigned_port))
serverSocket.listen()
#Fill in end


while True:
    print('The server is ready to receive')

    connectionSocket, addr = serverSocket.accept()

    try:

        message = connectionSocket.recv(1024).decode()

        filename = message.split()[1]

        f = open(filename[1:])

        outputdata = f.read()  # Fill in start             #Fill in end
        # send one http header line in to the socket
        #Fill in start
        serverSocket.recv("201".encode())
        #Fill in end

        # Send the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError:
        # Send HTTP response code and message for file not found
        #Fill in start

        connectionSocket.send(
            f"{HTTPStatus.NOT_FOUND:<10} {filename} not found".encode())
        #Fill in end

        # Close the client connection socket
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
