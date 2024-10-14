import flet as ft
class StartConfig(ft.Container):
    def __init__(self, page, controller, event):
        super().__init__()
        self.page = page
        self.controller = controller
        self.event = event
        
        self.margin = 5
        
        #Layout
        
        
        
        self.content = ft.Column(controls=[])