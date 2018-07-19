import os


class Blacklist(object):

    def __init__(self):
        self.blacklist = []

    def add_blackname(self, username):
        self.blacklist.append(username)

    def load_data(self):
        with open('./blacklist.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                self.blacklist.append(line)

    def save_data(self):
        with open('./blacklist.txt', 'w') as f:
            for line in self.blacklist:
                line = line.strip()
                f.write(line + '\n')

    def get_data(self):
        return self.blacklist
