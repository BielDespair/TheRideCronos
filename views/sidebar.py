import flet as ft

class SideBar(ft.NavigationRail):
    def __init__(self, page, controller):
        super().__init__()
        self.page = page
        self.controller = controller
        self.bgcolor = ft.colors.GREY_900
        self.selected_index = 0
        
        self.destinations = [
            ft.NavigationRailDestination(
                icon=ft.icons.HOME,
                selected_icon=ft.icons.HOME_OUTLINED,
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS,
                selected_icon=ft.icons.SETTINGS_OUTLINED,
                
            ),
        ]
        self.on_change = lambda e: self.controller.change_view(e)