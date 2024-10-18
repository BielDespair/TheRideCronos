import flet as ft
class EventCard(ft.UserControl):
    
    def __init__(self, event, controller):
        super().__init__()
        self.controller = controller
        
        # Properties
        self.id = event.id
        self.name = event.name
        self.date = event.date
        self.icon = event.icon_path
        
        self.EventObj = event
        
        #Layout 
        self.bgcolor = ft.colors.RED
        
        #Components
        #Header
        self.header = ft.Row(controls=[ft.Container(ft.Text(self.name, size=18, text_align=ft.TextAlign.CENTER), expand=True, bgcolor=self.bgcolor, alignment=ft.alignment.center)], spacing=0)
        
        #Footer
        self.delete_button = ft.IconButton(icon=ft.icons.DELETE, tooltip="Deletar evento", on_click=lambda e: self.controller.delete_event_confirmation(self))
        self.footer = ft.Row(controls=[ft.Container(content=self.delete_button, expand=True, bgcolor=ft.colors.TRANSPARENT, alignment=ft.alignment.bottom_right)], spacing=0)
        #Body
        self.date_text = ft.Text(self.date, size=12)
        self.body = ft.Row(controls=[self.date_text], spacing=0, expand=True)
        
        self.delete_dialog = ft.AlertDialog(
            modal=False,
            title=ft.Text("Deletar evento"),
            content=ft.Text("Tem certeza que deseja deletar este evento?"),
            actions=[
                ft.TextButton("Cancelar", on_click= lambda e: self.controller.dismiss_dialog()),
                ft.TextButton("Deletar", on_click= lambda e: self.controller.delete_event(self)),
                ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        
    def build(self):        
        return ft.Container(
            content=ft.Column(
                # Column
                [self.header, self.body, self.footer],
                tight=True,
                expand=True,),
            
                #Container
                #Layout
                width=400,
                height=200,
                border_radius=ft.border_radius.all(5),
                image=ft.DecorationImage(src=self.icon, fit=ft.ImageFit.COVER),
                ink=True,
                margin=ft.margin.all(10),
                
                #Data
                on_click= lambda e: self.controller.enter_event(self.EventObj),
            )
    def hide(self):
        self.visible = False
    def show(self):
        self.visible = True