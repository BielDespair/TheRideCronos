from models.settings import SettingsModel
class SettingsController:
    def __init__(self, page, view):
        self.page = page
        self.model = SettingsModel()
        self.view = view
        
    def get_url(self):
        return self.model.url
        