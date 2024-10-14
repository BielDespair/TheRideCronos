import flet as ft

from views.event_view.info import InfoView
from views.event_view.register import RegisterView

from controllers.event import EventController

class EventView(ft.Container):
    def __init__(self, page, event):
        super().__init__()
        self.page = page
        self.controller = EventController(page, event, self)
        
        #Atributes
        self.event = event
        #Layout
        self.expand = True
        #Components

        #Tabs
        self.info = InfoView(self.page, self.controller, self.event)
        self.register = RegisterView(self.page, self.controller, self.event)
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Evento", content=self.info),
                ft.Tab(text="Cadastro", content=self.register),
                ft.Tab(text="Participantes", content=self.register),
                ],
        )
        
        self.content = self.tabs