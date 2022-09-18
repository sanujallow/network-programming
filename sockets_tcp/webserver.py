# Import socket module
from base64 import encode
from socket import *
from http import HTTPStatus
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket
#Fill in start
LOCALHOST = '127.0.0.1'
ASSIGEND_PORT = 65015
serverSocket.bind((LOCALHOST, ASSIGEND_PORT))
serverSocket.listen()
#Fill in end

FORMAT = 'utf_8'
response_header = ''
while True:
    print('The server is ready to receive')

    connectionSocket, addr = serverSocket.accept()

    try:

        message = connectionSocket.recv(1024).decode(FORMAT)

        filename = message.split()[1]

        f = open(filename[1:])
        outputdata = f.readlines()

        # send one http header line in to the socket
        response_header = "HTTP/1.1 200 OK\r\n"
        connectionSocket.send(response_header.encode())

        # the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode(FORMAT))
            connectionSocket.send("\r\n".encode(FORMAT))
        connectionSocket.close()
        f.close()
    except IOError:
        # Send HTTP response code and message for file not found
        response_header = "HTTP/1.1 404 Not Found \r\n\r\n "
        response = f'<h2 style="text-align: center">Oops! 404 <br>file "{filename[1:]}" could not be found </h2>'
        connectionSocket.send(response_header.encode())
        connectionSocket.send(response.encode())

        # Close the client connection socket
        connectionSocket.close()
        break

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
