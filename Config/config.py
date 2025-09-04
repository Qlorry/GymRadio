import json
import logging
from os import abort

filename = "config.json"

template = {'token': '', 'admins_chat': "0", 'max_history_size': 100, "lang": "UA", "default_station": "KissFM"}
logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        # defaults:
        self.data = dict()  
        self.token = ""
        self.admins_chat = "0"
        self.max_history_size = 100
        self.lang = "UA"
        self.default_station = "KissFM"
        self.default_stream = "LofiGirl"
        self.streams = dict()
        self.streams = {"LofiGirl": "https://www.youtube.com/watch?v=jfKfPfyJRdk&ab_channel=LofiGirl"}


        # try read
        try:
            self.read_from_file()
            if not self.parse():
                abort()
        except FileNotFoundError:
            logger.error("Config was not found, created new. Please fill it!")
            self.update_config()
            self.write_to_file()
            abort()
       
        logger.info("Token = {}", self.token)
        logger.info("Admins chat ID = {}", self.admins_chat)
        logger.info("Max history size = {}", self.max_history_size)
        logger.info("Default station = {}", self.default_station)
        logger.info(self.lang)

    def write_to_file(self):
        config = open(filename, "w")
        default = json.dumps(self.data, indent=4)
        config.write(default)
        config.close()

    def read_from_file(self):
        config = open(filename, "r+")
        filedata = config.read()
        config.close()
        self.data = json.loads(filedata)

    def update_config(self):
        self.data['token'] = self.token
        self.data['admins_chat'] = self.admins_chat
        self.data['max_history_size'] = self.max_history_size
        self.data['lang'] = self.lang
        self.data['default_station'] = self.default_station
        self.data['default_stream'] = self.default_stream
        self.data['streams'] = self.streams

    def parse(self):
        try:
            self.token = self.data['token']
            self.admins_chat = self.data['admins_chat']
            self.max_history_size = self.data['max_history_size']
            self.lang = self.data['lang']
            if self.lang == "RU":
                self.lang = "UA"
            self.default_station = self.data['default_station']
            self.default_stream = self.data['default_stream']
            self.streams = self.data['streams']

            return True
        except KeyError as e:
            logger.error("No parameter " + str(e) + " in config")
            return False

conf = Config()
