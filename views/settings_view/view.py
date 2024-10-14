import flet as ft

from controllers.settings import SettingsController

class SettingsView(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controller = SettingsController(page, self)

        
        #Layout
        
        
        #Controls
        text_editor = ft.TextField(label="URL da API", value=self.controller.get_url(), width=len(self.controller.get_url())*10)
        
        self.controls = [text_editor]