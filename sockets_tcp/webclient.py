#**/
# @author: Momodou Jallow
# starId: {MY_STAR_ID}
# A web client that sends http requests to a webserver 
# and displays response on the console.
# @command_line_args: <serverhost> <serverport> <filename>
# see readme file for usage
#*/

from codecs import utf_8_decode
from ctypes import WinError
from http import HTTPStatus
from http.client import HTTPResponse
from socket import *
import sys
from tkinter import HORIZONTAL

#*/ 
# Define TCP Socket 
# @param address-family transport-type
# #*/
clientSocket = socket(AF_INET, SOCK_STREAM)

# constants
UTF_8 = 'utf_8'
CHUNK_SIZE = 1024
HTTP_STATUS_OK = '200'
HORIZONTAL_LINE = '_' * 50

#*/ 
# Web client setup 
# @param serverHost
# @param serverPort
# */
def initialize(serverHost, serverPort):
    try:
        clientSocket.connect((serverHost, serverPort))
    except ConnectionRefusedError as e:
        print("Connection refused")

#*/  
# Send file request to server specifying filenam 
# @param filename
# #*/
def send_request(filename):
    file_request = '/GET /' + filename
    clientSocket.send(file_request.encode(UTF_8))

#*/ Receive response from server #*/
def get_response():
    response = clientSocket.recv(CHUNK_SIZE)
    return response

#*/ print received content to screen from server #*/
def display_response(response):
    while response:
        print(f"{response.decode(UTF_8).strip(r'ï»¿')}")
        response = get_response()

#*/ print user arguments to screen #*/
def print_args():
    required_args = ['serverHost', 'serverPort', 'filename']

    for i, user_arg in enumerate(sys.argv[1:]):
        print(f"{required_args[i]:<12}: {user_arg}")
    print(f"{HORIZONTAL_LINE}\n")


if __name__ == "__main__":
    # parse user arguments
    serverHost = sys.argv[1]
    serverPort = int(sys.argv[2])
    filename = sys.argv[3]

    # print user arguments
    print_args()

    # process user request
    initialize(serverHost, serverPort)
    send_request(filename.strip())
    response = get_response()
    status_code = response.split()[1].decode(UTF_8)
    display_response(response) if (
        status_code == HTTP_STATUS_OK) else print(response.decode().strip('/r/n'))
    print()
