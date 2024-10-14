import flet as ft
class InfoView(ft.Container):
    def __init__(self, page, controller, event):
        super().__init__()
        self.page = page
        self.controller = controller
        
        self.event = event
        
        #Layout
        self.text_size = 18
        self.margin = 5
        #Texts
        name = ft.Text(self.event.name, size=20, text_align=ft.TextAlign.CENTER)
        self.event.organizer = "Some Organizer" #TODO: temporary
        organizer = ft.Text(self.event.organizer, size=18, text_align=ft.TextAlign.CENTER)
        event_type = ft.Text("Tipo de Prova", size=self.text_size)
        start_type = ft.Text("Tipo de Largada", size=self.text_size)
        
        #Buttons
        type_options = [ft.dropdown.Option(option) for option in self.controller.get_event_types()]
        bt_event_type = ft.Dropdown(options=type_options, value="Tipo de Prova", on_change=lambda e: self.controller.change_event_type(e.control.value))
        start_options = [ft.dropdown.Option(option) for option in self.controller.get_start_types()]
        bt_start_type = ft.Dropdown(options=start_options, value="Start", on_change=lambda e: self.controller.change_start(e.control.value))
        
        #Components
        type_select = ft.Container(ft.Column(controls=[event_type, bt_event_type], horizontal_alignment=ft.CrossAxisAlignment.CENTER),bgcolor=ft.colors.RED_200)
        start_select = ft.Container(ft.Column(controls=[start_type, bt_start_type], horizontal_alignment=ft.CrossAxisAlignment.CENTER),bgcolor=ft.colors.RED_500)
        #Controls
        row1 = ft.Row(controls=[name, organizer], alignment=ft.MainAxisAlignment.CENTER)
        row2 = ft.Row(controls=[type_select, start_select], alignment=ft.MainAxisAlignment.SPACE_AROUND)
        
        self.content = ft.Column(controls=[row1, row2], scroll=ft.ScrollMode.ALWAYS, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            
            