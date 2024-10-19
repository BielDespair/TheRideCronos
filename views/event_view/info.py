import flet as ft

from views.event_view.components.sheet_import_picker import SheetImportPicker
from views.event_view.components.start_by_category import StartByCategory
class InfoView(ft.Container):
    def __init__(self, page, controller, event):
        super().__init__()
        self.page = page
        self.controller = controller
        
        self.event = event
        
        #Layout
        self.text_size = 18
        self.margin = 5
        
        #Dialog
        self.sheet_import_dialog = SheetImportPicker(self.controller)
        if self.page.overlay:
            self.page.overlay[0] = self.sheet_import_dialog
        else:
            self.page.overlay.append(self.sheet_import_dialog)
        #Texts
        name = ft.Text(self.event.name, size=20, text_align=ft.TextAlign.CENTER)
        sheet_error = ft.Text("Nenhuma planilha carregada", size=18, color="red", text_align=ft.TextAlign.CENTER, visible=False)
        self.event.organizer = "Some Organizer" #TODO: temporary
        organizer = ft.Text(self.event.organizer, size=18, text_align=ft.TextAlign.CENTER)
        event_type = ft.Text("Tipo de Prova", size=self.text_size)
        start_type = ft.Text("Tipo de Largada", size=self.text_size)
        
        #Buttons
        bt_import_sheet = ft.ElevatedButton(text="Importar Planilha", icon=ft.icons.UPLOAD_FILE, on_click=lambda e: self.controller.import_sheet_dialog())
        type_options = [ft.dropdown.Option(option) for option in self.controller.get_event_types()]
        bt_event_type = ft.Dropdown(options=type_options, value=self.controller.get_event_types(), on_change=lambda e: self.controller.change_event_type(e.control.value))
        start_options = [ft.dropdown.Option(option) for option in self.controller.get_start_types()]
        bt_start_type = ft.Dropdown(options=start_options, value=self.controller.get_event_start(), on_change=lambda e: self.controller.change_start_type(e.control.value))
        
        #Components
        self.type_select = ft.Container(ft.Column(controls=[event_type, bt_event_type], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        self.start_select = ft.Container(ft.Column(controls=[start_type, bt_start_type], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        #Rows and Columns
        row1 = ft.Row(controls=[name, organizer], alignment=ft.MainAxisAlignment.CENTER)
        row2 = ft.Row(controls=[bt_import_sheet, sheet_error], alignment=ft.MainAxisAlignment.CENTER)
    
        
        event_configs = ft.Row([self.start_select], alignment=ft.MainAxisAlignment.CENTER)
        
        self.start_type_container = ft.Text()
        self.start_type_container.visible = True
        
        self.content = ft.Column(controls=[row1, row2, event_configs, self.start_type_container], scroll=ft.ScrollMode.ALWAYS, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
    def change_start_type(self, selected):
        if selected == "Intervalo por Categoria":
            self.start_type_container = StartByCategory(self.page, self.controller, self.event)
            self.content.controls[-1] = self.start_type_container
        self.update()