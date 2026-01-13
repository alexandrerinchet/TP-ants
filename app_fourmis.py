import flet as ft
import random
import math
import time
import threading
from ACO import AntColony

def main(page : ft.Page) :
    page.title = "algo ants"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    nodes = []
    #on définit les ces listes pour toute la boucle
    distances = []
    pheromones = []
    best_path = []
    iteration = 0
    running = False
    stop_event = threading.Event()
    #affiche les données de la simulation et permet à l'utilisateur de les visualiser/modifier
    best_field = ft.TextField(label="Meilleures fourmis", value="3", width=150)
    decay_field = ft.TextField(label="Décay", value="0.95", width=150)
    alpha_field = ft.TextField(label="Alpha", value="1", width=150)
    beta_field = ft.TextField(label="Beta", value="2", width=150)
    titre = ft.Text("Visualisation de l'algorithme", size = 24, weight = "bold")
    champ_noeuds = ft.TextField(label = "Nombre de noeuds", value = "20", width = 150)
    champ_fourmis = ft.TextField(label = "Nombre de fourmis", value = "15", width = 150)
    champ_itérations = ft.TextField(label = "Nombre d'itérations", value = "100", width = 150)
    zgraph = ft.Container(width = 600, height = 500, bgcolor = "lightblue", border = ft.border.all(2, "blue"))
    titre2 = ft.Text("Paramètres de l'algorithme", size = 24, weight = "bold")
    statut = ft.Text("Prêt à démarrer", size = 16, color = "green")
    #autres affichages pour l'utilisateur
    iteration_text = ft.Text("Itération: 0", size=16)
    pheromone_text = ft.Text("Phéromones moyennes: ", size=14)
    path_text = ft.Text("Meilleur chemin: ", size=14)
    
    def generer_nodes():
        '''Génère des positions aléatoires pour les nœuds'''
        nonlocal nodes, distances, pheromones

        try:
            num_nodes = int(champ_noeuds.value)
        except ValueError:
            num_nodes = 20

        nodes = []
        for _ in range(num_nodes):
            x = random.uniform(50, 550)
            y = random.uniform(50, 450)
            nodes.append((x, y))

        def calculer_distances():
            """Calcule la matrice des distances"""
            distances = []
            for i in range(len(nodes)):
                row = []
                for j in range(len(nodes)):
                    if i == j:
                        row.append(0)
                    else:
                        dx = nodes[i][0] - nodes[j][0]
                        dy = nodes[i][1] - nodes[j][1]
                        row.append(math.sqrt(dx*dx + dy*dy))
                distances.append(row)
            return distances

        distances = calculer_distances()
        pheromones = [[1.0 for _ in range(len(nodes))] for _ in range(len(nodes))]

        dessiner_graphe()

    def create_line(x1, y1, x2, y2, color, thickness):
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)

        return ft.Container(
            width=length,
            height=thickness,
            bgcolor=color,
            left=x1,
            top=y1 - thickness / 2,
            rotate=ft.Rotate(
                angle=angle,
                alignment=ft.alignment.Alignment(-1, 0)
            )
        )    
    
    def dessiner_graphe() :
        """
        Dessine le graphe des villes avec :
        - les arêtes pondérées par les phéromones
        - le meilleur chemin courant en rouge
        - les nœuds (villes) numérotés
        """

        # Liste de formes graphiques à afficher dans le Stack
        shapes = []
    
        # ==========================
        # Dessin des arêtes (phéromones)
        # ==========================
        if pheromones and len(pheromones) > 0:
            # Valeur maximale des phéromones (pour normalisation)
            max_pheromone = max(max(row) for row in pheromones) if pheromones else 1

            # Parcours de toutes les paires de nœuds
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    # Seuil minimal pour éviter l’encombrement visuel
                    if pheromones[i][j] > 0.1:
                        # Opacité proportionnelle à la quantité de phéromones
                        opacity = min(1, pheromones[i][j] / max_pheromone)

                        # Épaisseur proportionnelle aux phéromones
                        thickness = max(1, (pheromones[i][j] / max_pheromone) * 3)

                        # Création de la ligne entre les deux nœuds
                        line = create_line(
                            nodes[i][0], nodes[i][1],
                            nodes[j][0], nodes[j][1],
                            ft.Colors.with_opacity(opacity, ft.Colors.BLUE),
                            thickness
                        )
                        shapes.append(line)
    
        # ==========================
        # Dessin du meilleur chemin courant
        # ==========================
        if best_path:
            for i in range(len(best_path) - 1):
                start_idx = best_path[i]
                end_idx = best_path[i + 1]

                # Vérification de sécurité
                if start_idx < len(nodes) and end_idx < len(nodes):
                    line = create_line(
                        nodes[start_idx][0], nodes[start_idx][1],
                        nodes[end_idx][0], nodes[end_idx][1],
                        "red",   # Couleur du meilleur chemin
                        3        # Épaisseur renforcée
                    )
                    shapes.append(line)
    
        # ==========================
        # Dessin des nœuds (villes)
        # ==========================
        for i, (x, y) in enumerate(nodes):
            shapes.append(
                ft.Container(
                    width=20,
                    height=20,
                    bgcolor="green",
                    border_radius=10,   # Cercle
                    left=x - 10,
                    top=y - 10,
                    content=ft.Text(str(i), size=10, color="white"),
                    alignment=ft.alignment.Alignment(0, 0)
                )
            )
    
        # Mise à jour du conteneur graphique
        zgraph.content = ft.Stack(controls=shapes, width=600, height=500)
        page.update()
    
    def update_callback(iter_num, current_best_path, current_pheromones):
        """
        Callback appelé par l’algorithme à chaque itération
        pour mettre à jour l’interface graphique.
        """
        nonlocal iteration, best_path, pheromones

        # Mise à jour des variables globales
        iteration = iter_num
        best_path = current_best_path[0] if current_best_path else []
        pheromones = current_pheromones

        async def update_ui():
            # Affichage du numéro d’itération
            iteration_text.value = f"Itération: {iteration}"

            # Affichage du meilleur chemin et de sa longueur
            if current_best_path:
                path_text.value = (
                    f"Meilleur chemin: {best_path} "
                    f"(longueur: {current_best_path[1]:.2f})"
                )

            # Calcul de la moyenne des phéromones
            avg = sum(sum(row) for row in pheromones) / (len(nodes) ** 2)
            pheromone_text.value = f"Phéromones moyennes: {avg:.4f}"

            # Redessiner le graphe
            dessiner_graphe()

        # Lancement asynchrone pour ne pas bloquer l’UI
        page.run_task(update_ui)
    
    #reprendre ici
    
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
