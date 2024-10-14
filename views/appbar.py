import flet as ft

class AppBar(ft.AppBar):
    def __init__(self):
        super().__init__()
        self.leading = ft.Icon(ft.icons.HOURGLASS_EMPTY_SHARP, color="white")
        self.title = ft.Text("The Ride Cronos")
        self.toolbar_height = 75
        self.bgcolor = ft.colors.BLACK