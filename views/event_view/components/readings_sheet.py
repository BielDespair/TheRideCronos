import flet as ft

class ReadingsSheet(ft.DataTable):
    def __init__(self, page, controller, event):
        self.page = page
        self.controller = controller
        self.event = event
        self.rows = self.fetch_rows()
        super().__init__(columns=self.fetch_columns(), rows=self.rows)



            
    def fetch_rows(self):
        new_rows = self.controller.get_readings_rows()
        rows = []
        for row in new_rows:
            rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(data)) for data in row]))
        self.rows = rows
        
    def fetch_columns(self):
        columns = []
        for column in self.controller.get_readings_columns():
            columns.append(ft.DataColumn(ft.Text(column)))
        return columns
    
    def update_rows(self):
        self.fetch_rows()
        self.update()
        