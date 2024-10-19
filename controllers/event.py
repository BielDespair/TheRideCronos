import time
import threading
import requests


from models.event import EventModel

class EventController:
    def __init__(self, page, event, view):
        self.page = page
        self.model = EventModel(event)
        self.view = view
        
        self.auto_advance = False
        self.started = False
    
    def search(self, value):
        value = value.lower()
        for row in self.view.register.dt_rows:
            data = row.cells[self.model.search_key].data.lower()
            if data.lower().startswith(value):
                row.visible = True
            else:
                row.visible = False
        self.view.register.dt.update()
        
    def insert_register_dialog(self):
        self.active_dialog = self.view.register.insert_register_dialog
        self.page.open(self.active_dialog)
    def insert_register(self):
        #TODO Insert to the "sheet" and set current index of tag reg to this one.
        pass
    def register_tag(self):
        error, result = self.model.register_tag()
        self.view.register.show_register_text(error, result)
        if error: return
        
        self.view.register.fetch_rows()
        if self.auto_advance:
            self.get_next_athlete()

    def dismiss_message(self, delay):
        time.sleep(delay)
        self.view.register.show_register_text(True, "")
    
    def search_sheet(self, value):
        #open dialog
        ...
    def get_columns(self):
        return self.model.get_columns()
    def get_readings_columns(self):
        return ['Posição', 'Nome', 'Placa', 'Trajeto', 'Categoria']
    def get_readings_rows(self):
        return self.model.get_readings_rows()
    def get_registered_rows(self):
        rows = self.model.get_registered_athletes()
        return rows
    def get_next_athlete(self):
        self.view.register.update_athlete(self.model.get_next_athlete())
    def get_prev_athlete(self):
        self.view.register.update_athlete(self.model.get_prev_athlete())
    
    def edit_register(self):
        pass
    
    def get_event_categories(self):
        return self.model.get_event_categories()
    def get_event_trajectories(self):
        return self.model.get_event_trajectories()
    def get_event_types(self):
        return self.model.get_event_types()
    def get_start_types(self):
        return self.model.get_start_types()
    def get_event_start(self):
        return self.model.get_event_start()
    def get_sheet_name(self):
        return self.model.get_sheet_name()
    def set_event_sheet(self, e):
        files = e.files
        if files:
            self.model.set_event_sheet(files[0].path)
        self.initialize()
    def set_absent_athlete(self):
        self.model.set_absent_athlete()
        if self.auto_advance:
            self.view.register.update_athlete(self.model.get_next_athlete())
        
    def change_event_type(self, value):
        self.model.change_event_type(value)
    def change_start_type(self, value):
        
        self.model.set_start_type(value)
        self.view.info.change_start_type(value)

    def sheet_is_present(self):
        if self.model.sheet_is_present():
            return True
        return False
    
    def import_sheet_dialog(self):
        self.view.info.sheet_import_dialog.pick_files()
        
    def dismiss_dialog(self):
        self.page.close(self.active_dialog)
        
    def initialize(self):
        self.view.register.toggle_sheet()
        df_loaded, error = self.model.load_df()
        if not df_loaded:
            print("Failed to load df")
            #Show error returned by model
            pass
        else:
            #load df and get first athlete, if resumed show registered athletes
            self.get_next_athlete()
            self.view.register.fetch_rows()
            self.view.register.dt.update()
            
    def toggle_auto_advance(self, value):
        self.auto_advance = value
        
    def start_event(self):
        self.model.start_event()
        get_thread = threading.Thread(target=self.get_api_readings_thread)
        endpoint_thread = threading.Thread(target=self.endpoint_thread)
        
        self.started = True
        get_thread.start()
        endpoint_thread.start()
        
        
        self.view.start.toggle_button(self.started)
        
    def end_event(self):
        self.started = False
        self.view.start.toggle_button(self.started)
        #outras rotinas ao finalizar.
        
    def get_api_readings_thread(self):
        event_id = self.model.id
        api_token = self.model.api_token
        while self.started:
            readings, error_ocurred = self.model.api.get_readings(event_id, api_token)
            if error_ocurred:
                self.view.start.show_message(readings, True) #Show error message
            else:
                self.model.add_athletes_readings(readings)
                self.view.start.readings_sheet.update_rows()
                self.view.start.dismiss_message()            
            time.sleep(5)
                
    def endpoint_thread(self):
        while self.started:
            print("Endpoint thread.")
            
            
            
            time.sleep(5)
        
        