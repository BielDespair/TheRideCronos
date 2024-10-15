from models.event import EventModel

class EventController:
    def __init__(self, page, event, view):
        self.page = page
        self.model = EventModel(event)
        self.view = view
    
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
        pass
        
    def search_sheet(self, value):
        #open dialog
        ...
    def get_columns(self):
        return self.model.get_columns()
    def get_rows(self):
        rows = self.model.get_rows()
        return rows
    def get_next_athlete(self):
        return self.model.get_next_athlete()
    
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
    
    def change_event_type(self, value):
        self.model.change_event_type(value)
    def change_start_type(self, value):
        self.model.change_start_type(value)

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
            #Show error returned by model
            pass
        else:
            #load df and get first athlete, if resumed show registered athletes
            self.view.register.get_next_athlete()
            self.view.register.fetch_rows()
            self.view.register.dt.update()