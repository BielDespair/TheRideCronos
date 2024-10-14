from views.event_view.view import EventView
from views.home_view.view import HomeView
from views.settings_view.view import SettingsView

class NavController:
    def __init__(self, page, app):
        self.page = page
        self.app = app
        
        
        self.home_view = HomeView(page)
        self.settings_view = SettingsView(page)
        self.views = [self.home_view, self.settings_view]

        self.active_view = self.home_view
    
        
    def change_view(self, e):
        self.active_view = self.views[e.control.selected_index]
        self.app.controls[-1] = self.active_view
        print(self.app.controls)
        self.page.update()
    def enter_event(self, event):
        self.active_view = EventView(self.page, event)
        self.app.controls[-1] = self.active_view
        self.page.sidebar.selected_index = None
        self.page.update()