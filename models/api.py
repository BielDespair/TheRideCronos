import requests
import json
from models.settings import SettingsModel

class API():
    def __init__(self):
        self.settings = SettingsModel()
        self.url = self.settings.get_url()
        self.local = self.settings.get_local()

        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'CronosApp/1.0.0 (Windows)'
        }
    def create_event(self, name):
        # Define the JSON payload
        
        payload = {
            "name": name
        }

        # Make the POST request
        response = requests.post(self.settings.get_create_event_url(), headers=self.headers, data=json.dumps(payload))
        if response.status_code == 200 or response.status_code == 201:
            return response.json(), False
        
        return response.json()['message'], True
    def get_readings(self, id, api_token):
        payload = {
            "api_token": api_token
        }
        url = self.url + f"/{id}/readings"
        
        # Make the GET request
        response = requests.get(url=url, headers=self.headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json(), False
        return response.json()['message'], True
    
    def update_configs(self):
        #Should update its attributes by recalling itself
        self.url = self.settings.get_url()
        self.local = self.settings.get_local()