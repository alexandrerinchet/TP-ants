import flet as ft
import random
import math

def main(page : ft.Page) :
    page.title = "algo ants"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    nodes = []
    titre = ft.Text("Visualisation de l'algorithme", size = 24, weight = "bold")
    champ_noeuds = ft.TextField(label = "Nombre de noeuds", value = "20", width = 150)
    champ_fourmis = ft.TextField(label = "Nombre de fourmis", value = "15", width = 150)
    champ_itérations = ft.TextField(label = "Nombre d'itérations", value = "100", width = 150)
    zgraph = ft.Container(width = 600, height = 500, bgcolor = "lightblue", border = ft.border.all(2, "blue"))
    titre2 = ft.Text("Paramètres de l'algorithme", size = 24, weight = "bold")
    statut = ft.Text("Prêt à démarrer", size = 16, color = "green")
    
    def calculer_distances():
    #Calcule la matrice des distances entre tous les nœuds
        distances = []
        for i in range(len(nodes)):
            row = []
            for j in range(len(nodes)):
                if i == j:
                    row.append(0)
                else:
                    # Distance euclidienne
                    dx = nodes[i][0] - nodes[j][0]
                    dy = nodes[i][1] - nodes[j][1]
                    distance = math.sqrt(dx * dx + dy * dy)
                    row.append(distance)
            distances.append(row)
        return distances
    
    def generer_nodes() :
        nonlocal nodes
        try :
            num_nodes = int(champ_noeuds.value)
        except :
            num_nodes = 20
        nodes = []
        for _ in range(num_nodes) :
            x = random.uniform(50, 550)
            y = random.uniform(50, 450)
            nodes.append((x,y))
        distances = calculer_distances()
        print(f"{len(nodes)} nœuds générés")
        print(f"Distance entre nœud 0 et 1 : {distances[0][1]:.2f}")
        dessiner_graphe()

        
    
    def dessiner_graphe() :
        shapes = []
        i = 1
        for noeud in nodes :
            x,y = noeud
            circle = ft.Container(
                width=20, height=20,
                bgcolor="green",
                border_radius=10,
                left=x-10, top=y-10,
                content=ft.Text(str(i), size=10, color="white"),
                alignment=ft.Alignment(0,0)
                )
            shapes.append(circle)
            i += 1
        zgraph.content = ft.Stack(controls = shapes, width = 600, height = 500)
        page.update()

    btn_generer = ft.ElevatedButton(
        "Générer le Graphe",
        on_click=lambda e: generer_nodes()
    )
    
    generer_nodes()

    page.add(
        ft.Column([
            titre2,
            ft.Row([champ_noeuds, champ_fourmis, champ_itérations]),
            btn_generer,
            ft.Divider(),
            statut,
            zgraph
        ])
    )
    


ft.run(main)
