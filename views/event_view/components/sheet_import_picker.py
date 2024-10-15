import flet as ft
class SheetImportPicker(ft.FilePicker):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
          
        self.dialog_title = "Importar Planilha"
        
        self.allow_multiple = False #TODO allow multiple, check if columns match and concat all.
        self.allowed_extensions = ["xlsx", "xls", "csv"] 
        self.on_result = self.controller.set_event_sheet
    