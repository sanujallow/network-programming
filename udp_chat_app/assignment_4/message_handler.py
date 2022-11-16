from collections import namedtuple
from encodings import utf_8

class MessageHandler:
    P = namedtuple('Prefix', ['command', 'direct', 'public', 'exit'])
    __prefix = P('C', 'DM', 'PM', 'EX')

    def __init__(self, client_socket, server_host, server_port, username):
        """A class to encode and send messages of type Command, Direct, Public and Exit
        """
        self.__client_socket = client_socket
        self.__server_host = server_host
        self.__server_port = server_port

    def send_command(self, message):
        message =  "|".join([self.__prefix.command, message])
        self.send_msg(message)


    def send_direct(self, message, recipient_username):
        if recipient_username is None:
            recipient_username = " "
        message =  "|".join([self.__prefix.direct, recipient_username, message])
        self.send_msg(message)

    
    def send_public(self, message):
        message = "|".join([self.__prefix.public, message])
        self.send_msg(message)


    def send_exit(self):
        self.send_msg(self.__prefix.exit)
    
    def parse_msg(self, message:str):
        msg_tokens = message.partition('_')
        msg_type = msg_tokens[0].upper()
        msg_content = msg_tokens[2]
        valid_type = False if not (msg_type.upper() in ({'C', 'DM', 'PM', 'EX'})) else True
        valid_content = False if not (msg_content) and msg_type != 'EX' else True

        return (msg_type, msg_content, valid_type, valid_content)

    def send_parsed(self, msg_type, msg_content, recipient_username = None):
        """determines message type and calls appropriate method to send message"""
        
        if msg_type == self.__prefix.exit:
            self.send_exit()
        elif msg_type == self.__prefix.command:
            self.send_command(msg_content.strip())
        elif msg_type == self.__prefix.direct:
            recipient_username = input("Enter reciepient username: ")
            self.send_direct(msg_content, recipient_username)
        elif msg_type == self.__prefix.public:
            self.send_public(msg_content)
            

    def send_msg(self,  message):
        """Sends udp datagram to chatserver    
        
        arguments:
        msg -- text of message to be sent to chat server
        """
        return self.__client_socket.sendto(message.encode('utf-8'), (self.__server_host, int(self.__server_port)))
