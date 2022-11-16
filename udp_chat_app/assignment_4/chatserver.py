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


# Constants
serverSocket = socket(AF_INET, SOCK_DGRAM)
LOCALHOST = '127.0.0.1'
UTF_8 = 'utf-8'


def initialize_server(server_host, server_port):
    """binds server socket to server port and host address"""

    serverSocket.bind((server_host, server_port))


def is_valid_message(datagram):
    clien_data = datagram[0].decode().partition('|')
    client_msg = clien_data[2].strip()
    return False if len(client_msg) == 0 else True


def process_login(user: User):
    isNewUser = True
    isLoggedIn = False

    data_file = "chat_users.json"
    user_data_file = File(data_file)
    existing_usr_msg = 'Your account exists, send your password to login'
    new_usr_msg = 'Account not found. Send password to register'

    usr_name = user.get_username()
    usr_address = user.get_client_address()

    users = user_data_file.read()

    if usr_name in users.keys():
        isNewUser = False
        send(existing_usr_msg, usr_address)
    else:
        send(new_usr_msg, usr_address)

    password_datagram = serverSocket.recvfrom(1024)

    login_data = process_datagram(password_datagram)
    password = login_data[2].strip()
    print('password: ', password)

    if (isNewUser):
        user.set_password(password)
        update_clients(user_data_file, user)
        isLoggedIn = True
        print('your password is: ', password.strip())
    else:
        if (password == users[usr_name]['password']):
            user.set_session_state(User.SessionState.ACTIVE)
            active_users.update({user.get_username(): user})
            isLoggedIn = True

    # users = user_data_file.read()
    acknowledge(
        usr_address, f'SUCCESS|Login success' if isLoggedIn else 'FAIL|Incorrect Password')
    return isLoggedIn


def process_datagram(datagram):
    client_address = datagram[1]
    client_data_tokens = datagram[0].decode().partition('|')
    message_type = client_data_tokens[0].strip()
    client_message = client_data_tokens[2].strip()
    return (client_address, message_type, client_message)


def broadcast(username, message, active_users):
    message = '>> '.join([username, message])
    users = list(active_users.values())

    for user in users:
        user: User = user
        send(message, user.get_client_address())


def acknowledge(client_address, ack_msg):
    send(ack_msg, client_address)


def direct_msg(message, from_user, to_user):
    if active_users.get(to_user) is not None:
        message = ': '.join(from_user, message)
        send(message, to_user)


def send(message: str, client_address: tuple):
    serverSocket.sendto(message.encode(UTF_8),  client_address)


def listen(datagram, active_users: dict):
    while datagram:
        try:
            print('*** message received ***')

            rcvd_address, rcvd_msg_type, rcvd_msg = process_datagram(datagram)

            # print(f'Received messag:\n{client_message}\n')
            print(f'received client_address: {rcvd_address}')
            print(f'received message_type: {rcvd_msg_type}')

            user: User = None

            if 'LOGIN' in rcvd_msg.upper():
                username = rcvd_msg.split(' ')[1]
                user = User(username, rcvd_address)

            for active_usr in active_users.values():
                active_usr: User = active_usr
                if active_usr.get_client_address() == rcvd_address:
                    user = active_usr

            if rcvd_msg_type == 'PM':
                broadcast(user.get_username(), rcvd_msg, active_users)
                return
            elif rcvd_msg_type == 'C':
                execute_command(user, rcvd_msg, active_users)
                return
            elif rcvd_msg_type == 'DM':
                process_directmsg(user, rcvd_msg, active_users)
                return
            elif rcvd_msg_type == 'EX':
                end_client_session(user, active_users)
                return
        except Exception as e:
            acknowledge(rcvd_address,
                        f'FAIL|Sorry there has been been a problem:\n {e}')
    return


def execute_command(user: User, client_message, active_users: dict):
    username = user.get_username()
    user_address = user.get_client_address()

    if client_message.upper() == 'USERS':
        send(str(list(active_users.keys())), user_address)
        return

    if username in active_users.keys():
        send(f'{username} is logged in', user_address)
        return
    else:
        user.set_session_state(User.SessionState.LOGIN_REQUESTED)
        active_users.update({user.get_username(): user})
        login_result = process_login(user)
        print(
            f'{username} is logged in') if login_result == True else None
    return


def process_directmsg(user: User, client_message, active_users: dict):
    recipient = client_message.partition('|')[0]

    if not recipient:
        send(list(active_users.keys()))

    dm = client_message.partition('|')[2]
    dm = ': '.join([f'direct_msg from {user.get_username()}', dm])

    if recipient in active_users.keys():
        recipient: User = active_users[recipient]
        send(dm, recipient.get_client_address())
        acknowledge(user.get_client_address(),
                    f'SUCCESS|message DM sent to {recipient.get_username()}')


def end_client_session(user: User, active_users: dict):
    active_users.pop(user.get_username())
    user = None


def load_clients(file: File):
    return File.read()


def update_clients(file: File, user: User):
    file.update(user.get_username(), user.user_info())


def main():
    print(f'The server is listening on port {UDP_SERVER_PORT}')

    while True:
        print("online users: ", list(active_users.keys()))
        print('Waiting ...')
        datagram = serverSocket.recvfrom(1024)
        listn_thread = Thread(target=listen, args=[datagram, active_users])
        listn_thread.start()
        listn_thread.join()


if __name__ == "__main__":
    UDP_SERVER_PORT = int(sys.argv[1])
    serverSocket.bind((LOCALHOST, UDP_SERVER_PORT))
    active_users = dict()
    main()
