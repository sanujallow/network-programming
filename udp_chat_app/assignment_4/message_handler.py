class Message:
    def __init__(self):
        self.__command = 'C'
        self.__direct_msg = 'DM'
        self.__public_msg = 'PM'
        self.__direct_msg = 'DM'
        self.__exit = 'E'

    def command(self, message):
        return "|".join([self.__command, message])

    def direct(self, message):
        return "|".join([self.__direct_msg, message])

    def public(self, message):
        return "|".join([self.__public_msg, message])

    def exit(self):
        return "|".join([self.__command, self.__exit])
