from socket import *
import sys
from datetime import datetime
from time import time
import hashlib
import traceback
from threading import Thread
from filehandler import File
from user import User
import traceback
from collections import namedtuple


serverSocket = socket(AF_INET, SOCK_DGRAM)
LOCALHOST = '127.0.0.1'
UTF_8 = 'utf_8'

active_users = {}
# Prepare a sever socket


def initialize_server(server_port):
    SERVER_PORT = server_port
    serverSocket.bind((LOCALHOST, SERVER_PORT))


def calculate_checksum(message):
    return hashlib.md5(message.encode(UTF_8)).hexdigest()


def process_datagram(datagram):
    client_address = datagram[1]
    print('client_address_line31: ', client_address)
    client_data = datagram[0].decode().partition('|')
    print('client_data_line33: ', client_data)
    message_type = client_data[0].strip()
    client_message = client_data[2].strip()
    return (client_address, client_data, message_type, client_message)


def process_login(user: User):
    data_file = "chat_users.json"
    user_data_file = File(data_file)
    existing_usr_msg = 'Your account exists, send your password to login'
    new_usr_msg = 'Account not found. Send password to register'

    usr_name = user.get_username()
    usr_address = user.get_client_address()

    users = user_data_file.read()

    isNewUser = True
    isLoggedIn = False

    if usr_name in users.keys():
        isNewUser = False
        send(existing_usr_msg, usr_address)
    else:
        send(new_usr_msg, usr_address)

    password_datagram = serverSocket.recvfrom(1024)

    login_data = process_datagram(password_datagram)

    print('password: ', login_data[3])

    if (isNewUser):
        user.set_password(login_data[3])
        isLoggedIn = True
        update_clients(user_data_file, user)
        users = user_data_file.read()

    if (login_data[3] == users[usr_name]['password']):
        send('200| Login success', usr_address)
        isLoggedIn = True
    else:
        send('401| Incorrect Password', usr_address)

    return isLoggedIn


def broadcast(message):
    user_addresses = active_users.values
    for address in user_addresses:
        send(message, address)


def direct_msg(message, from_user, to_user):
    if active_users.get(to_user) is not None:
        message = ': '.join(from_user, message)
        send(message, to_user)


def add_active_user(username, client_address):
    active_users.update({username: client_address})


def send(message: str, client_address: tuple):
    serverSocket.sendto(message.encode(UTF_8),  client_address)


def listen():
    while True:
        print('Waiting ...')

        try:
            datagram = serverSocket.recvfrom(1024)
            print('*** new message ***')

            received_timestamp = datetime.now()
            client_data = datagram[0].decode()
            message_type = client_data.split('|')[0].strip()
            client_message = client_data.split('|')[1]
            client_address = datagram[1]
            calculated_checksum = calculate_checksum(client_message)

            # prints the date and time
            print(f'Received time: {received_timestamp.ctime()}')
            print(f'Received messag:\n{client_message}\n')
            print(f'received client_address: {client_address}')
            print(f'received message_type: {message_type}')
            print(f'calculated checksum: {calculated_checksum}')

            user = User(client_message, None, client_address)
            isLoggedIn = process_login(user)

            print(
                f'{user.get_username()} is logged in') if isLoggedIn == True else None
            print()
        except Exception as e:
            traceback.print_exc()
            # sys.exit()
            return

        # process_msg_thread = Thread(target = process_client_msg, args=(received_timestamp, message_type, client_message, client_address, calculated_checksum)

            # if (calculated_checksum == received_checksum):
            #     server_response = received_timestamp.ctime()
            #     serverSocket.sendto(server_response.encode(UTF_8),  client_address)
            # else:
            #     error_msg = 'checksum mismatch error'
            #     error_msg += '\nACK 0'
            #     serverSocket.sendto(error_msg.encode(UTF_8),  client_address)


# def process_client_msg(received_timestamp, message_type, client_message, client_address, calculated_checksum):
def load_clients(file: File):
    return File.read()


def update_clients(file: File, user: User):
    file.update(user.get_username(), user.user_info())


def main():
    listn_thread = Thread(target=listen)

    listn_thread.start()


if __name__ == "__main__":
    # parse user arguments
    UDP_SERVER_PORT = int(sys.argv[1])
    initialize_server(UDP_SERVER_PORT)
    print(f'The server is listening on port {UDP_SERVER_PORT}')
    main()
