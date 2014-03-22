__author__ = 'erik'

import os

from ConfigParser import ConfigParser


class Parser:
    def __init__(self):
        self.config = ConfigParser()
        self.__cfile = open(os.path.join(os.getcwd(), 'config.ini'), 'r')
        self.config.readfp(self.__cfile)
        self.login = self.config.get('EmailConfigs', 'sender')
        self.password = self.config.get('EmailConfigs', 'password')
        self.to = self.config.get('EmailConfigs', 'to').split(',')
        self.urls = self.config.get('URLS', 'urls')

    def get_login(self):
        return self.login

    def get_password(self):
        return self.password

    def get_to(self):
        return self.to

    def get_urls_as_list(self):
        return self.urls.split(',')