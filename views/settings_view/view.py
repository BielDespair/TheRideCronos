import flet as ft

from controllers.settings import SettingsController

class SettingsView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controller = SettingsController(page, self)

        
        #Layout
        self.padding = ft.padding.all(5)
        self.margin = ft.margin.all(5)
        
        
        #Controls
        toggle_local = ft.Switch(label="Local", on_change=lambda e: self.controller.set_local(e.control.value))
        text_editor = ft.TextField(label="URL da API", value=self.controller.get_url(), width=len(self.controller.get_url())*12)
        
        self.content = ft.Column([toggle_local, text_editor])