import flet as ft

def main(page : ft.Page) :
    page.title = "ants algo"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    titre = ft.Text("Visualisation de l'algorithme", size = 24, weight = "bold")
    bouton = ft.Button("Cliquez-moi", on_click = lambda e : print("test"))
    page.add(ft.Column([titre, bouton]))
    champ1 = ft.TextField(label = "Nombre de noeuds", value = "20", width = 150)
    champ2 = ft.TextField(label = "Nombre de fourmis", value = "15", width = 150)
    champ3 = ft.TextField(label = "Nombre d'itérations", value = "100", width = 150)
    zgraph = ft.Container(width = 600, height = 500, bgcolor = "lightblue", border = ft.border.all(2, "blue"))
    titre2 = ft.Text("Paramètres de l'algorithme", size = 24, weight = "bold")
    statut = ft.Text("Prêt à démarrer", size = 16, color = "green")
    page.add(ft.Column([titre2, ft.Row([champ1, champ2, champ3]), ft.Divider(), statut, zgraph]))

ft.run(main)
