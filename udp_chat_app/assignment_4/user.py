class User:
    def __init__(self, username: str, password, client_address: tuple):
        self.__username = username
        self.__password = password
        self.__client_address = client_address

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_client_address(self):
        return self.__client_address

    def set_password(self, password):
        self.__password = password

    def set_client_address(self, client_address):
        self.__client_address = client_address

    def user_info(self):
        """returns user's client_address and user's password"""
        user_info = {
            'address': self.__client_address,
            'password': self.__password,
        }

        return user_info
