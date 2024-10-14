import flet as ft
from views.app_layout import AppLayout


def main(page: ft.Page):
    #Page properties
    page.title = "The Ride Cronos"
    
    page.add(AppLayout(page))
    
ft.app(target=main)