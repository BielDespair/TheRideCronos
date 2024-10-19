import flet as ft
class Sheet(ft.UserControl):
    def __init__(self, page, controller, event):
        super().__init__()
        self.page = page
        self.controller = controller
        self.event = event
        
        #Properties
        self.columns = self.fetch_columns()
        self.rows = self.fetch_rows()
        
        #Layout
    def build(self):
        self.sheet = ft.DataTable(
            columns=self.columns,
            rows=self.rows,
            bgcolor=ft.colors.BLACK,
            )
        
        return self.sheet
    def fetch_columns(self):
        columns = []
        for column in self.controller.get_columns():
            columns.append(ft.DataColumn(ft.Text(column)))
        return columns

    def fetch_rows(self):
        rows = []
        for row in self.controller.get_registered_athletes():
            rows.append(ft.DataRow(cells=self.fetch_cells(row)))
        return rows
    def fetch_cells(self, row):
        cells = []
        for data in row:
            cells.append(ft.DataCell(ft.Text(data), data=str(data)))
        return cells