# **/
# @author: Momodou Jallow
# starId: {MY_STAR_ID}
# A web client that sends UDP requests to a webserver
# and displays response on the console.
# @command_line_args: <serverhost> <serverport> <filename | text>
# see readme file for usage
# */

from datetime import datetime
from email import message
import hashlib
from socket import *
from sqlite3 import Timestamp
import sys
from threading import Thread
from time import sleep
from message_handler import MessageHandler
from getpass import getpass

# constants
UTF_8 = 'utf-8'
CHUNK_SIZE = 1024
HORIZONTAL_LINE = '_' * 50

clientSocket = socket(AF_INET, SOCK_DGRAM)
global UDP_SERVER_HOST
global UDP_SERVER_PORT
global MESSENGER


def get_response():
    """ Receive and decode response from server"""
    response = clientSocket.recvfrom(CHUNK_SIZE)
    return (response)


def print_args():
    """Displays user arguments"""

    required_args = ['<serverHost>', '<serverPort>', '<username>']

    for i, user_arg in enumerate(sys.argv[1:]):
        print(f"{required_args[i]:<12}: {user_arg}")
    print(f"{HORIZONTAL_LINE}\n")


def login_to_server(messsage_sender, username):
    """Sends login request to server

    arguments:
    username -- the username of the chat client user entered as command line argument
    """
    print(f"Welcome {username}\n")
    try:
        messsage_sender.send_command('LOGIN ' + username)
        response_datagram = get_response()
        response_msg = response_datagram[0]
        print(f'server: {response_msg}\n')

        password = getpass("Enter password >> ")
        encrypted_password = hashlib.md5(password.encode(UTF_8)).hexdigest()
        messsage_sender.send_command(encrypted_password)
        print('password sent...')
        login_response = get_response()[0]
        print(f'server: {login_response.decode(UTF_8)}\n')

        if login_response.decode(UTF_8) != 'FAIL':
            return True
    except Exception as e:
        print('there has been an error: ', e)

    return False


def prompt_user(msg_handler):
    msg_type = ""
    while msg_type.upper() != 'EX':

        print('\nPM: public message | DM: direct message | C: command | EX: exit')
        print('to get active users for DM, first send C_Users')

        usr_msg = input(f'{USERNAME} >> ')

        msg_type, msg_content, valid_type, valid_msg = (
            msg_handler.parse_msg(usr_msg))

        if(valid_type and valid_msg):
            msg_handler.send_parsed(msg_type, msg_content)
            print('Message sent\n')
        else:
            print(
                f'Error: invalid type or empty message: \n type: {msg_type} \n message: {msg_content}')
            continue


def main(*args, **kwargs):
    if len(sys.argv) < 3:
        print('Please enter valid arguments:  <server-name> <port-number> <username>')

    # instantiate MessageHandler object
    msg_handler = MessageHandler(
        clientSocket, UDP_SERVER_HOST, UDP_SERVER_PORT, USERNAME)

    # execute login process
    logged_in = False
    while(not logged_in):
        logged_in = login_to_server(msg_handler, USERNAME)

    print('You are now logged in')

    msg_type = ""
    while msg_type.upper() != 'EX':

        print('\nPM: public message | DM: direct message | C: command | EX: exit')
        print('to get active users for DM, first send C_Users')

        usr_msg = input(f'{USERNAME} >> ')

        msg_type, msg_content, valid_type, valid_msg = (
            msg_handler.parse_msg(usr_msg))

        if(valid_type and valid_msg):
            msg_handler.send_parsed(msg_type, msg_content)
            print('Message sent\n')
        else:
            print(
                f'Error: invalid type or empty message: \n type: {msg_type} \n message: {msg_content}')
            continue

        server_response = get_response()[0].decode(UTF_8)
        print(server_response)

    clientSocket.close()


if __name__ == "__main__":
    # Get command line args
    UDP_SERVER_HOST = sys.argv[1]
    UDP_SERVER_PORT = sys.argv[2]
    USERNAME = sys.argv[3]
    print_args()
    main()
