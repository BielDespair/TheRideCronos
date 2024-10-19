import configparser
class SettingsModel:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("data/server.ini")
        self.url = config['SERVER']['URL']
        self.create_event_url = config['SERVER']['CREATE_EVENT_URL']
        
        self.local_url = config['LOCAL']['URL']
        self.local_create_event_url = config['LOCAL']['CREATE_EVENT_URL']
    def get_create_event_url(self):
        return self.create_event_url
    def get_url(self):
        return self.url
    def get_local_url(self):
        return self.local_url
    def get_local_create_event_url(self):
        return self.local_create_event_url
