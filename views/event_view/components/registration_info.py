import flet as ft
class RegistrationInfo(ft.UserControl):
    def __init__(self, controller, event):
        super().__init__()
        self.controller = controller
        self.event = event

        self.name_athlete = "Raphael Platini amaro da Rocha naves"
        self.name_plate = "Nome Placa um pouco grande ne pra vc"
        self.num_plate = "000-0"
        self.category = "Categoria"
        
        #Layout

    def build(self):
        sheet = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Placa"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Numero"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Categoria"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
            ],
            rows=[
                ft.DataRow(
                cells=[
                ft.DataCell(ft.Text(self.name_athlete, text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(self.name_plate, text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(self.num_plate, text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(self.category, text_align=ft.TextAlign.CENTER)),
                ],
                on_select_changed=lambda e: self.controller.select_athlete(e.control.data)
                
            )

            ],
            
            

        )
        return sheet