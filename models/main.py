
import os
from models.utils import get_events_paths

from models.database import Database
from models.event_class import Event
from models.settings import SettingsModel #Maybe change
from models.api import API #Could be better


class MainModel:
    def __init__(self):
        self.db = Database()
        self.settings = SettingsModel()
        self.api = API()
        
        self.events = None #TODO self.get_events() -> This should not be on view/controller. Both has eventOBJ. Change it.
    
    def get_events(self):
        event_paths = get_events_paths(self.db.events_path)
        events = []
        #This should all be in the model
        for path in event_paths:
            query = self.db.query_event(path)
            new_event = Event(id=query['api_id'], api_token=query['api_token'], name=query['name'], date=query['date'], icon_path=query['icon_path'],  sheet_path=query['sheet_path'], event_path=query['path'])
            events.append(new_event)
        return events
    
    def create_new_event(self, name, date, icon_path, offline):
        if not offline:
            response = self.api.create_event(name)
            data, error = response[0], response[1]
            if error:
                return data, False
            id = data['id']
            api_token = data['api_token']
        else:
            id = name
            api_token = ""
        event = Event(id, api_token, name, date, icon_path)        
        self.db.new_event(event)
        
        return event, True
    def delete_event(self, event):
        os.remove(event.path)