import configparser
class SettingsModel:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("data/server.ini")
        self.url = config['SERVER']['URL']
        self.create_event_url = config['SERVER']['CREATE_EVENT_URL']
    def get_create_event_url(self):
        return self.create_event_url
    def get_url(self):
        return self.url
    def get_local(self):
        return True
