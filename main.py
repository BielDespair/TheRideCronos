import flet as ft
from views.app_layout import AppLayout


def main(page: ft.Page):
    #Page properties
    page.title = "The Ride Cronos"
    page.window_min_width = 1366
    page.window_min_height = 768
    
    page.add(AppLayout(page))
    
ft.app(target=main)