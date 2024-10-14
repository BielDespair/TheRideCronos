import flet as ft

from views.appbar import AppBar
from views.sidebar import SideBar

from controllers.navrail import NavController
class AppLayout(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        #Theme
        self.page.theme_mode = ft.ThemeMode.DARK
        
        #Layout properties
        self.expand = True
        self.page.padding = 0
        
        #Components
        self.page.appbar = AppBar()
        self.page.sidebar = SideBar(self.page, NavController(self.page, self))
        
        self.controls = [self.page.sidebar, self.page.sidebar.controller.active_view]