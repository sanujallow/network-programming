from socket import *
import sys
from datetime import datetime
from time import time
import hashlib
import traceback

serverSocket = socket(AF_INET, SOCK_DGRAM)
LOCALHOST = '127.0.0.1'
UTF_8 = 'utf_8'

# Prepare a sever socket


def initialize_server(server_port):
    SERVER_PORT = server_port
    serverSocket.bind((LOCALHOST, SERVER_PORT))


def calculate_checksum(message):
    return hashlib.md5(message.encode(UTF_8)).hexdigest()


def main():
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

            # if (calculated_checksum == received_checksum):
            #     server_response = received_timestamp.ctime()
            #     serverSocket.sendto(server_response.encode(UTF_8),  client_address)
            # else:
            #     error_msg = 'checksum mismatch error'
            #     error_msg += '\nACK 0'
            #     serverSocket.sendto(error_msg.encode(UTF_8),  client_address)

            print()

        except Exception as e:
            sys.exit()


if __name__ == "__main__":
    # parse user arguments
    UDP_SERVER_PORT = int(sys.argv[1])
    initialize_server(UDP_SERVER_PORT)
    print(f'The server is listening on port {UDP_SERVER_PORT}')
    main()
