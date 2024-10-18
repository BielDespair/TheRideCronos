import flet as ft
class RegistrationInfo(ft.UserControl):
    def __init__(self, controller, event):
        super().__init__()
        self.controller = controller
        self.event = event

        self.name_athlete = ""
        self.name_plate = ""
        self.num_plate = ""
        self.category = ""
        self.columns = [               
                ft.DataColumn(ft.Text("Nome"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Placa"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Numero"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Categoria"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ]
        self.row = [ft.DataRow(
                cells=[
                ft.DataCell(ft.Text(self.name_athlete, text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(self.name_plate, text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(self.num_plate, text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(self.category, text_align=ft.TextAlign.CENTER)),
                ],
                on_select_changed=lambda e: self.controller.get_next_athlete(e.control.data)
            )]
        #Layout
    def build(self):
        self.sheet = ft.DataTable(
            columns=self.columns,
            rows=self.row,
        )
        return self.sheet
    
    def update_row(self, athlete):
        if not athlete:
            athlete = ["", "", "", ""]        
        self.sheet.rows[0].cells[0].content.value = athlete[0]
        self.sheet.rows[0].cells[1].content.value = athlete[1]
        self.sheet.rows[0].cells[2].content.value = athlete[2]
        self.sheet.rows[0].cells[3].content.value = athlete[3]
        self.sheet.update()
        self.update()
        