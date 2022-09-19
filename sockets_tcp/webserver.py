#*/
# @author: Momodou Jallow 
# starId: {MY_STAR_ID}
# A program web server that handles http requests from a client 
# and returns an HTTP response along with requested content if content is available.
#/

from socket import *
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket
#Fill in start
LOCALHOST = '127.0.0.1'
ASSIGEND_PORT = 65015
serverSocket.bind((LOCALHOST, ASSIGEND_PORT))
serverSocket.listen()
#Fill in end

UTF_8 = 'utf_8'
response_header = ''
while True:
    print('The server is ready to receive')

    connectionSocket, addr = serverSocket.accept()

    try:

        message = connectionSocket.recv(1024).decode(UTF_8)

        filename = message.split()[1]

        f = open(filename[1:])

        outputdata = f.readlines()

        # send one http header line in to the socket
        response_header = "HTTP/1.1 200 OK\r\n"
        connectionSocket.send(response_header.encode(UTF_8))

        # the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
        connectionSocket.close()
        f.close()
    except IOError:
        # Send HTTP response code and message for file not found
        response_header = "HTTP/1.1 404 Not Found\r\n\r\n "
        response = f'<h2 style="text-align: center">Oops! 404 <br>file "{filename[1:]}" could not be found </h2>'
        connectionSocket.send(response_header.encode(UTF_8))
        connectionSocket.send(response.encode(UTF_8))
        connectionSocket.send("\r\n".encode(UTF_8))

        # Close the client connection socket
        connectionSocket.close()


serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
