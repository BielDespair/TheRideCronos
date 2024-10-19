import flet as ft

from views.event_view.components.readings_sheet import ReadingsSheet
class StartView(ft.Container):
    def __init__(self, page, controller, event):
        super().__init__()
        self.page = page
        self.controller = controller
        self.event = event

        
        #Layout
        self.padding = ft.padding.all(10)
        #Texts
        self.status_text = ft.Text(value="Placeholder", visible=True)
        
        
        #Buttons
        self.start_event_button = ft.ElevatedButton("Iniciar Evento", on_click= lambda e: self.controller.start_event())
    

        #Components
        self.readings_sheet = ReadingsSheet(self.page, self.controller, self.event)
                
        
        self.content = ft.Column([self.start_event_button, self.status_text, self.readings_sheet], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
    
    def show_message(self, message, error):
        color = ft.colors.RED if error else None
        self.status_text.value = message
        self.status_text.color = color
        self.status_text.visible = True
        self.update()
    
    def dismiss_message(self):
        self.status_text.visible = False
        self.update()
    def update_sheet(self):
        self.readings_sheet.update_rows()
        self.update()
    
    def toggle_button(self, started):
        if started:
            self.start_event_button.text="Finalizar Evento"
            self.start_event_button.on_click=lambda e: self.controller.end_event()
        else:
            self.start_event_button.text="Iniciar Evento"
            self.start_event_button.on_click= lambda e: self.controller.start_event()
        self.update()
            
        
        
        