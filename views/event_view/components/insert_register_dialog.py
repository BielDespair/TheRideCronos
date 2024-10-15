import flet as ft

class InsertRegisterDialog(ft.AlertDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title = ft.Text("Adicionar Participante")
        
        #Texts
        #Athlete Personal
        self.name = ft.TextField(label="Nome")
        self.gender = ft.Dropdown(label="Sexo", options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Feminino")])
        self.birthdate = ft.TextField(label="Data de Nascimento", suffix=ft.IconButton(icon=ft.icons.CALENDAR_TODAY, on_click=lambda e: self.pickDate(e)))
        self.phone_number = ft.TextField(label="Celular")
        self.allow_contact = ft.Switch(label="Receber Mensagens")
        #Athlete Plating
        self.plate_name = ft.TextField(label="Placa")
        self.plate_number = ft.TextField(label="Número")
        
        trajectories = [ft.dropdown.Option(trajectory) for trajectory in self.controller.get_event_trajectories()]
        self.trajectory = ft.Dropdown(label="Trajeto", options=trajectories)
        
        categories = [ft.dropdown.Option(category) for category in self.controller.get_event_categories()]
        self.category = ft.Dropdown(label="Categoria", options=categories)
        
        #Rows and Columns
        self.content = ft.Column([self.name, self.gender, self.birthdate, self.phone_number, self.allow_contact, self.plate_name, self.plate_number, self.trajectory, self.category], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        self.actions = [ft.TextButton("Cancelar", on_click=lambda e: self.controller.dismiss_dialog()), ft.ElevatedButton("Adicionar", on_click=lambda e: self.add_participant())]
        
        
        