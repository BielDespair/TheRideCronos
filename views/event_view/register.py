import flet as ft

from views.event_view.components.sheet import Sheet


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
        self.bgcolor = ft.colors.RED
        self.opacity = 1
        self.margin = 5
        
        #Texts
        text1 = ft.Text("Participantes Cadastrados", text_align=ft.TextAlign.CENTER)
        
        #Buttons
        search_bar = ft.TextField(label="Pesquisar", on_change=lambda e: self.controller.search(e.control.value), width=200)
        insert_register = ft.OutlinedButton("Inseririr Participante", on_click=lambda e: self.controller.insert())
        
        #Components
        registers_header = ft.Row([search_bar, insert_register])
        scroll_column = ft.Column([self.dt], scroll=ft.ScrollMode.ALWAYS, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        scroll_table = ft.Container(ft.Column([registers_header, scroll_column], horizontal_alignment=ft.CrossAxisAlignment.CENTER), margin=5)
        
        
        divider = ft.VerticalDivider(width=5)
        
        #Controls
        register_container = ft.Row(controls=[divider, scroll_table, ], expand=True, alignment=ft.MainAxisAlignment.END)
        
        
        self.content = ft.Column([register_container])
