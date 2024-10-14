from models.event import EventModel

class EventController:
    def __init__(self, page, view):
        self.page = page
        self.model = EventModel()
        self.view = view
        
        
        
        
    def search(self, value):
        value = value.lower()
        for row in self.view.register.dt.rows:
            data = row.cells[self.model.search_key].data.lower()
            if data.lower().startswith(value):
                row.visible = True
            else:
                row.visible = False
        self.view.dt.update()
    def get_columns(self):
        return self.model.get_columns()
    def get_rows(self):
        rows = self.model.get_rows()
        return rows
    def get_next_register(self):
        pass
    
    def edit_register(self):
        pass
    
    def get_event_types(self):
        return self.model.get_event_types()
    def get_start_types(self):
        return self.model.get_start_types()
    
    def change_event_type(self, value):
        
        self.view.update()
    def change_start_type(self, value):
        
        self.view.update()