from pathlib import Path
import json

default_file = Path('./chat_users.json')
backup_file = Path('./chat_users_backup.json')


class File:
    def __init__(self, data_file=default_file):
        self.__data_file = data_file
        # self.save(dict())

    def save(self, data):
        with open(self.__data_file, 'w') as outfile:
            json.dump(data, outfile, indent=2)
            return('custom settings saved')

    def read(self) -> dict:
        with open(self.__data_file, 'r') as f:
            data = json.load(f)
        return data

    def update(self, username, client_info: dict):
        """ updates file by adding username as key to client password and address object"""
        data = self.read()
        data.update({username: client_info})
        self.save(data)

    def print_file_info(self):
        data = self.read()
        for key in data:
            print(f'{key}: {data[key]}')

    def set_file(self, new_file):
        self.__data_file = new_file

    def clear(self):
        self.save(dict())
