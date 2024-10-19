#TODO this class should be removed and replaced by models/event entirely (maybe)
#We should remove the eventObj from the event_card, and when enter_event() is called, the EventModel obj should be loaded by getting info from the database.
#TODO If this is not  removed, this class is incomplete. Upon loading from the path, it should load the not db file (.ini, .json, something)
#TODO i think a database is overkill at this point. We should use a .csv/.xlsx, because we can them export readings and print on paper. the only reason
# a database is being used is for data integrity


#THIS CLASS IS USELESS
class Event():
    def __init__(self, id, api_token, name, date, icon_path, sheet_path, net_mode, event_path=None):
        self.id = id
        self.api_token = api_token
        self.name = name
        self.date = date
        self.net_mode = net_mode
        if not icon_path:
            self.icon_path = "assets/images/default_event_bg.jpg"
        else:
            self.icon_path = icon_path
        self.event_path = event_path
        
        self.sheet_path = sheet_path
        self.sheet_format = '.xlsx'

    def set_path(self, path):
        self.event_path = path