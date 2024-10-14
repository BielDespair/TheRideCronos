import flet as ft

from controllers.main import MainController

#Components
from views.home_view.components.add_event_dialog import AddEventDialog
from views.home_view.components.event_card import EventCard
class HomeView(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controller = MainController(page, self)

        #Layout
        self.color = ft.colors.RED
        self.expand = True
        self.alignment = ft.alignment.top_left

        #Initialize event cards
        self.fetch_events()
        #Components
        self.add_event_dialog = AddEventDialog
        
        #Controls
        add_event_button = ft.Row([ft.IconButton(icon=ft.icons.ADD, tooltip="Criar novo evento", on_click=lambda e: self.controller.add_event_dialog())])
        searchbar = ft.TextField(label="Pesquisar", on_change=lambda e: self.controller.search(e.control.value))
        filter_events = ft.Dropdown(options=[ft.dropdown.Option("Todos"), ft.dropdown.Option("Ativos"), ft.dropdown.Option("Inativos")], value="Todos")
        header = ft.Container(ft.Row([add_event_button, searchbar, filter_events], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), margin=10)
        self.controls = [header, self.events]
        
    def fetch_events(self):
        #Create a EventCard for each event in path
        self.events = ft.Row(
            [
                EventCard(event, self.controller) for event in self.controller.get_events()
            ],
            wrap=True,
        )
        self.update()
    def append_event(self, event):
        self.events.controls.append(EventCard(event, self.controller))
        self.update()