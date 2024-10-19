import flet as ft

class StartByCategory(ft.Container):
    def __init__(self, page, controller, event):
        super().__init__()
        self.page = page
        self.controller = controller
        self.event = event
        
        
        
        #Text
        text_interval = ft.Text("Intervalo (Minutos)")
        
        #Buttons
        self.interval = ft.TextField(width=100)
        
        #Rows and Columns
        self.content = ft.Row(controls=[text_interval, self.interval], alignment=ft.MainAxisAlignment.CENTER)
        
        
        
    
        
        
