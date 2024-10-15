import flet as ft

from views.event_view.components.insert_register_dialog import InsertRegisterDialog
from views.event_view.components.registration_info import RegistrationInfo

class RegisterView(ft.Container):
    def __init__(self, page, controller, event):
        super().__init__()
        self.page = page
        self.controller = controller
        #Atributes
        self.event = event
        self.dt_columns = self.fetch_columns()
        self.dt_rows = []
        self.dt = ft.DataTable(columns=self.dt_columns, rows=self.dt_rows)
        #Layout
        self.expand = True
        self.margin = 5
        
        #Dialog
        self.insert_register_dialog = InsertRegisterDialog(self.controller)
        #Texts
        text1 = ft.Text("Participantes Cadastrados", size=20, text_align=ft.TextAlign.CENTER)
        text2 = ft.Text("Cadastro dos Participantes", size=20, text_align=ft.TextAlign.CENTER)
        
        self.sheet_text = ft.Text(text_align=ft.TextAlign.CENTER)
 
        self.registration_text = ft.Text(value="", visible=False)
        
        #Buttons
        search_bar_text = ft.TextField(label="Pesquisar", on_change=lambda e: self.controller.search(e.control.value), width=200)
        register_search_bar = ft.TextField(label="Pesquisar", on_change=lambda e: self.controller.register_search(e.control.value), width=200)
        
        insert_register = ft.OutlinedButton("Inseririr Participante", on_click=lambda e: self.controller.insert_register_dialog())

        prev_athlete = ft.OutlinedButton("Anterior", on_click=lambda e: self.controller.prev_athlete())
        skip_athlete = ft.OutlinedButton("Pular", on_click=lambda e: self.controller.skip_athlete())
        next_athlete = ft.OutlinedButton("Proximo", on_click=lambda e: self.controller.next_athlete())
        register = ft.OutlinedButton("Cadastrar Tag", on_click=lambda e: self.controller.register())

        #Components
        registers_header = ft.Row([search_bar_text, insert_register])
        self.scroll_column = ft.Column([self.dt], scroll=ft.ScrollMode.ALWAYS, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        scroll_table = ft.Container(ft.Column([text1, registers_header, self.scroll_column], horizontal_alignment=ft.CrossAxisAlignment.CENTER), margin=5)
        self.athlete_register_info = RegistrationInfo(self.controller, self.event)
        registration_row = ft.Row([prev_athlete, skip_athlete, next_athlete], alignment=ft.MainAxisAlignment.CENTER)

        divider = ft.VerticalDivider(width=5)
        #Controls
        left_container = ft.Column([text2, self.sheet_text, self.athlete_register_info, registration_row, register, self.registration_text], expand=True, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        register_container = ft.Row(controls=[left_container, divider, scroll_table, ], expand=True, alignment=ft.MainAxisAlignment.CENTER)
        
        
        self.content = ft.Column([register_container])
        
        

    def toggle_sheet(self):
        if self.controller.sheet_is_present():
            self.sheet_text.value = f"Planilha Participantes: {self.controller.get_sheet_name()}"
            self.sheet_text.color = None
        else:
            self.sheet_text.value = "Nenhuma planilha encontrada"
            self.sheet_text.color = "red"
        self.update()
    def get_next_athlete(self):
        athlete = self.controller.get_next_athlete()
        print(athlete)
        
                
    def fetch_columns(self):
        columns = []
        for column in self.controller.get_columns():
            columns.append(ft.DataColumn(ft.Text(column)))
        return columns

    def fetch_rows(self):
        rows = []
        for row in self.controller.get_rows():
            rows.append(ft.DataRow(cells=self.fetch_cells(row)))
        return rows
    
    def fetch_cells(self, row):
        cells = []
        for data in row:
            cells.append(ft.DataCell(ft.Text(data), data=str(data)))
        return cells