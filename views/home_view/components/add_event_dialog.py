import flet as ft
class AddEventDialog(ft.AlertDialog):
    def __init__(self, view, controller):
        super().__init__()
        self.view = view
        self.controller = controller
        
        #Layout
        self.modal = True
        
        #Components
        self.title = ft.Text("Adicionar evento")
        self.content = ft.TextField(label="Nome do evento")
        self.actions = [ft.TextButton("Cancelar", on_click=lambda e: self.controller.dismiss_dialog()), ft.ElevatedButton("Adicionar", on_click=lambda e: self.add_event())]
        
        self.name = ft.TextField(label="Nome do Evento", autofocus=True, on_change=lambda e: self.update())
        self.date = ft.TextField(label="Data", read_only=True, suffix=ft.IconButton(icon=ft.icons.CALENDAR_TODAY, on_click=lambda e: self.pickDate(e)))
        self.local = ft.TextField(label="Local")
        self.sheet = ft.TextField(label="Planilha(s)", suffix=ft.IconButton(icon=ft.icons.UPLOAD_FILE, on_click=lambda e: print(e)))
        self.net_mode = ft.Switch(label="Offline", value=False, on_change=self.toggle_switch)
        self.progress = ft.ProgressRing(visible=False)
        
        self.error = ft.Text(value="Parece que algo deu errado ao adicionar o evento:")
        self.error_code = ft.Text(color="red")
        self.error_column = ft.Column([self.error, self.error_code], visible=False)
        #Controls
        self.content = ft.Column([self.name, self.date, self.local, self.sheet, self.net_mode, self.progress, self.error_column], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
    def add_event(self):
        self.controller.add_event(self.name.value, self.net_mode.value, self.local.value)
        
    def pickDate(self, e):
        self.open = False
        self.EventsView.page.open(ft.DatePicker(on_change=lambda e: self.confirmPicker(e), on_dismiss=lambda e: self.cancelPicker(e)))
        
    def confirmPicker(self, e):
        self.open = True
        self.date.value = e.control.value.strftime('%d/%m/%Y')
        self.EventsView.page.update()
        self.date.focus()
        
    def cancelPicker(self, e):
        self.open = True
        self.EventsView.page.update()
        self.date.focus()
        
    def show_error(self, error):
        self.error_column.visible = True
        self.error_code.value = "Error: " + error
        self.update()
    def toggle_waiting(self):
        self.progress.visible = not self.progress.visible
        self.modal = not self.modal
        self.update()
        
    def toggle_switch(self, e):
        if e.control.value:
            e.control.label="Online"
        else:
            e.control.label = "Offline"
        self.update()

