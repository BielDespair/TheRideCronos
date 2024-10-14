import flet as ft
from views.app_layout import AppLayout


class TheRideConnectApp():
    def __init__(self, page):
        self.page = page
        self.app = AppLayout(self.page)


    def build(self):
        return self.app
        
    