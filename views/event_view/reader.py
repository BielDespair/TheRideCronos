import flet as ft

from views.event_view.components.sheet_import_picker import SheetImportPicker
class InfoView(ft.Container):
    def __init__(self, page, controller, event):
        super().__init__()
        self.page = page
        self.controller = controller
        
        self.event = event
        
        #Layout
        self.text_size = 18
        self.margin = 5
        

        self.content = ft.Column(controls=[row1, row2], scroll=ft.ScrollMode.ALWAYS, horizontal_alignment=ft.CrossAxisAlignment.CENTER)