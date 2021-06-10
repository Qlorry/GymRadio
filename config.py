import json

filename = "config.json"

template = {'token': '', 'admins_chat': ""}


class Config:
    def __init__(self):
        # try read
        try:
            config = open(filename, "r+")
        except FileNotFoundError as e:
            config = open(filename, "w")
            default = json.dumps(template)
            config.write(default)
            print("Config was not found, created new. Please fill it!")
            config.close()
            exit()
        filedata = config.read()
        config.close()
        self.data = json.loads(filedata)
        # Init values
        try:
            self.token = self.data['token']
            self.admins_chat = self.data['admins_chat']
        except KeyError as e:
            print("No parameter " + str(e) + " in config")
            exit()

    def update_config(self):
        self.data['token'] = self.token
        config = open(filename, "w")
        default = json.dumps(self.data)
        config.write(default)
        config.close()
