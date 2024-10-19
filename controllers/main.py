import time

from models.main import MainModel

class MainController:
    def __init__(self, page, view):
        self.page = page
        self.model = MainModel()
        self.view = view
    
    def add_event(self, name, date, offline, icon_path=None, sheet_path=None):
        self.active_dialog.disabled = True
        self.active_dialog.toggle_waiting()
        
        time.sleep(0.5)
        data, response = self.model.create_new_event(name, date, icon_path, sheet_path, offline)
        #Falha na API
        if not response:
            self.active_dialog.disabled = False
            self.active_dialog.show_error(data)
            self.active_dialog.toggle_waiting()
            
        #Sucesso
        else:
            self.view.append_event(data)
            self.page.close(self.active_dialog)
            self.view.update()
            
    def add_event_dialog(self):
        self.active_dialog = self.view.add_event_dialog(self.view, self)
        self.page.open(self.active_dialog)
        
    def get_events(self):
        events = self.model.get_events()
        return events
    def delete_event(self, event_card):
        self.page.close(self.active_dialog)
        
        for index, view_event in enumerate(self.view.events.controls):
            if view_event.id == event_card.id:
                self.view.events.controls.pop(index)
                break
        
        self.model.delete_event(event_card.EventObj)
        self.view.update()
    def delete_event_confirmation(self, event_card):
        self.active_dialog = event_card.delete_dialog
        self.page.open(self.active_dialog)
    def dismiss_dialog(self):
        self.page.close(self.active_dialog)
        
    def search(self, value):
        for event_card in self.view.events.controls:
            if not event_card.name.lower().startswith(value.lower()):
                event_card.hide()
            else:
                event_card.show()
            self.view.update()
    def enter_event(self, event):
        self.page.sidebar.controller.enter_event(event)