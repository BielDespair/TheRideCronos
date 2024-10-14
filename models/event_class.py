#TODO this class should be removed and replaced by models/event entirely
#We should remove the eventObj from the event_card, and when enter_event() is called, the EventModel obj should be loaded by getting info from the database.
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
        
        self.sheet_path = None
        self.sheet_format = '.xlsx'

    def set_path(self, path):
        self.path = path