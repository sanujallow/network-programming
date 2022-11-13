# **/
# @author: Momodou Jallow
# starId: {MY_STAR_ID}
# A web client that sends UDP requests to a webserver
# and displays response on the console.
# @command_line_args: <serverhost> <serverport> <filename | text>
# see readme file for usage
# */

from datetime import datetime
import hashlib
from socket import *
from sqlite3 import Timestamp
import sys
from time import sleep
from message_handler import Message
from getpass import getpass

# constants
UTF_8 = 'utf_8'
CHUNK_SIZE = 1024
HORIZONTAL_LINE = '_' * 50

clientSocket = socket(AF_INET, SOCK_DGRAM)
global UDP_SERVER_HOST
global UDP_SERVER_PORT


# */
# Send file request to server after appending file data to checksum
# @param filename
# */
def send_file_request(filename):
    f = open(filename, 'rb').read()
    checksum = hashlib.md5(f).hexdigest()
    datagram = checksum + '|'
    datagram = datagram + f.decode()
    datagram = datagram.encode(UTF_8)
    time_stamp = datetime.now()
    clientSocket.sendto(datagram, (UDP_SERVER_HOST, UDP_SERVER_PORT))

    print('checksum sent: ' + checksum)
    return time_stamp

# */
# Calculate checksum and Send text request to server
# @param text
# #*/


def send_text_request(text):

    checksum = hashlib.md5(text.encode(UTF_8)).hexdigest()
    datagram = checksum + '|' + text
    datagram = datagram.encode(UTF_8)
    time_stamp = datetime.now()
    clientSocket.sendto(datagram, (UDP_SERVER_HOST, UDP_SERVER_PORT))

    print('checksum sent: ' + checksum)

    return time_stamp


# */ Receive response from server #*/

def get_response():
    timestamp = datetime.now()
    response = clientSocket.recvfrom(CHUNK_SIZE)
    return (response, timestamp)

# */ print received content to screen from server #*/


def display_response(response, send_time_stamp, received_time_stamp):
    if response[0:3] == 'checksum mismatch error':
        print(response)
    else:
        success_msg = 'server has successfully received the message'
        server_response_msg = response.decode(UTF_8)
        print(f"{success_msg} at {server_response_msg}")
        RTT = received_time_stamp - send_time_stamp
        print(f"RTT: at {RTT.microseconds}us")


# */ print user arguments to screen #*/
def print_args():
    required_args = ['<serverHost>', '<serverPort>', '<username>']

    for i, user_arg in enumerate(sys.argv[1:]):
        print(f"{required_args[i]:<12}: {user_arg}")
    print(f"{HORIZONTAL_LINE}\n")

# */
# Send command message
# @param command message e.g. username or password
# */

# ------------------------------------------------------------------------------------


def send_msg(msg: str):
    # send command message datagram to server
    clientSocket.sendto(msg.encode(
        UTF_8), (UDP_SERVER_HOST, int(UDP_SERVER_PORT)))


def login_to_server(username):
    print(f"Welcome {USERNAME}. Please Enter your password\n")
    msg = Message()
    username_msg = msg.command(USERNAME)

    send_msg(username_msg)
    response_datagram = get_response()
    response_msg = response_datagram[0][0]
    print(f'server: {response_msg.decode(UTF_8)}\n')

    print(f"Please Enter your password\n")
    password = getpass()
    password_msg = msg.command(password)
    send_msg(password_msg)
    print('password sent...')
    login_response = get_response()[0][0]
    print(f'server: {login_response.decode(UTF_8)}\n')


def main(*args, **kwargs):
    # parse user arguments and display args

    print_args()

    # execute login process
    # send username
    login_to_server(USERNAME)

    # determine message type from user input - C for command, D for data, or None

    # send message
    # get response from server

    # get response from clients in new thread


if __name__ == "__main__":
    # parse user arguments
    UDP_SERVER_HOST = sys.argv[1]
    UDP_SERVER_PORT = sys.argv[2]
    USERNAME = sys.argv[3]

    if len(sys.argv) < 3:
        print('Please enter valid arguments:  <server-name> <port-number> <username>')

    # main(UDP_SERVER_HOST, UDP_SERVER_PORT, USERNAME)
    main()

    # TXT_FILE_EXTENSION = '.txt'

    # send_time_stamp = None
    # if (username[-4:] == TXT_FILE_EXTENSION):
    #     send_time_stamp = send_file_request(
    #         username.strip())  # process file request
    # else:
    #     send_time_stamp = send_text_request(
    #         username.strip())  # process text request

    # response_datagram = get_response()
    # response_msg = response_datagram[0][0]
    # received_timestamp = response_datagram[1]
    # display_response(response_msg, send_time_stamp, received_timestamp)
    # clientSocket.close()
