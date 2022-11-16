from enum import Enum


class User:
    class SessionState(Enum):
        OFFLINE = 0
        LOGIN_REQUESTED = 1
        PASSWORD_PENDING = 2
        ACTIVE = 3

    def __init__(self, username: str, client_address: tuple, session_state=SessionState.OFFLINE):
        self.__username = username
        self.__password = None
        self.__client_address = client_address
        self.__session = session_state

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_client_address(self):
        return self.__client_address

    def set_client_address(self, client_address):
        self.__client_address = client_address

    def get_session_state(self):
        return self.__session

    def set_session_state(self, session_state: SessionState):
        self.__session = session_state

    def user_info(self):
        """returns user's client_address and user's password"""
        user_info = {
            'address': self.__client_address,
            'password': self.__password,
        }

        return user_info
