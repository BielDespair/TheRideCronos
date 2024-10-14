class Event():
    def __init__(self, id, api_token, name, date, icon_path, path=None):
        self.id = id
        self.api_token = api_token
        self.name = name
        self.date = date
        if not icon_path:
            self.icon_path = "assets/images/default_event_bg.jpg"
        else:
            self.icon_path = icon_path
        self.path = path
    def set_path(self, path):
        self.path = path