import flet as ft

def main(page : ft.Page) :
    page.title = "ants algo"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    titre = ft.Text("Visualisation de l'algorithme", size = 24, weight = "bold")
    bouton = ft.Button("Cliquez-moi", on_click = lambda e : print("test"))
    page.add(ft.Column([titre, bouton]))

ft.run(main)
