import requests
import json
from models.settings import SettingsModel

class API():
    def __init__(self):
        self.settings = SettingsModel()
    
    def create_event(self, name):
        # Define the JSON payload
        
        payload = {
            "name": name
        }

        # Set the Content-Type header to application/json
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'CronosApp/1.0.0 (Windows)'
        }
        
        # Make the POST request
        response = requests.post(self.settings.get_create_event_url(), headers=headers, data=json.dumps(payload))
        if response.status_code == 200 or response.status_code == 201:
            return response.json(), False
        
        return response.json()['message'], True