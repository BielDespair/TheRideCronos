import flet as ft
class RegistrationInfo(ft.UserControl):
    def __init__(self, controller, event):
        super().__init__()
        self.controller = controller
        self.event = event

        self.name_athlete = "Atleta"
        self.name_plate = "Nome Placa"
        self.num_plate = "000-0"
        self.category = "Categoria"

    def build(self):
        sheet = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Placa", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Numero", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Categoria", text_align=ft.TextAlign.CENTER)),
            ],
            rows=[
                ft.DataRow(
                cells=[
                ft.DataCell(ft.Text(self.name_athlete, text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(self.name_plate, text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(self.num_plate, text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(self.category, text_align=ft.TextAlign.CENTER)),
                ]
            )

            ]

        )
        return sheet