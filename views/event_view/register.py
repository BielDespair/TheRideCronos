import flet as ft

from views.event_view.components.sheet import Sheet
from views.event_view.components.registration_info import RegistrationInfo

class RegisterView(ft.Container):
    def __init__(self, page, controller, event):
        super().__init__()
        self.page = page
        self.controller = controller
        #Atributes
        self.event = event
        self.dt = Sheet(self.page, self.controller, self.event)
        #Layout
        self.expand = True
        self.margin = 5
        
        #Texts
        text1 = ft.Text("Participantes Cadastrados", text_align=ft.TextAlign.CENTER)
        self.sheet_text = ft.Text(f"Planilha Participantes: {self.controller.get_sheet_name()}") if self.controller.sheet_is_present() else ft.Text("Nenhuma planilha encontrada", text_align=ft.TextAlign.CENTER, color=ft.colors.RED)

        
        #Buttons
        search_bar = ft.TextField(label="Pesquisar", on_change=lambda e: self.controller.search(e.control.value), width=200)
        insert_register = ft.OutlinedButton("Inseririr Participante", on_click=lambda e: self.controller.insert())

        prev_athlete = ft.OutlinedButton("Anterior", on_click=lambda e: self.controller.prev_athlete())
        skip_athlete = ft.OutlinedButton("Pular", on_click=lambda e: self.controller.skip_athlete())
        next_athlete = ft.OutlinedButton("Proximo", on_click=lambda e: self.controller.next_athlete())
        register = ft.OutlinedButton("Cadastrar Tag", scale=1.3,on_click=lambda e: self.controller.register())


        
        #Components

        registers_header = ft.Row([search_bar, insert_register])
        scroll_column = ft.Column([self.dt], scroll=ft.ScrollMode.ALWAYS, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        scroll_table = ft.Container(ft.Column([registers_header, scroll_column], horizontal_alignment=ft.CrossAxisAlignment.CENTER), margin=5)
        self.athlete_register_info = RegistrationInfo(self.controller, self.event)
        registration_row = ft.Row([prev_athlete, skip_athlete, next_athlete], alignment=ft.MainAxisAlignment.CENTER)

        
        divider = ft.VerticalDivider(width=5)
        
        #Controls
        left_container = ft.Column([self.sheet_text, self.athlete_register_info, registration_row, register], expand=True, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        register_container = ft.Row(controls=[left_container, divider, scroll_table, ], expand=True, alignment=ft.MainAxisAlignment.CENTER)
        
        
        self.content = ft.Column([register_container])

        def toggle_sheet(present):
            if present:
                self.sheet_text = ft.Text("Planilha Participantes", text_align=ft.TextAlign.CENTER)
            else:
                self.sheet_text = ft.Text("Nenhuma planilha encontrada", text_align=ft.TextAlign.CENTER, color=ft.colors.RED)