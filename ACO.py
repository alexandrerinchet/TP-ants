import random
import time
import threading

class AntColony:
    def __init__(self, distances : list, n_fourmis : int, n_meilleurs : int, n_iterations : int, decroissance : float, alpha : float = 1, beta : float = 2):
        """
        Initialise la colonie de fourmis.
        
        Paramètres :
        - distances : matrice des distances entre les villes ex : distances[i][j] est la distance entre la ville i et la ville j
        - n_fourmis : nombre de fourmis par itération
        - n_meilleurs : nombre de meilleurs chemins qui déposent des phéromones
        - n_iterations : nombre d'itérations de l'algorithme
        - decay : taux d'évaporation des phéromones (entre 0 et 1)
        - alpha : importance des phéromones (α)
        - beta : importance de l'heuristique (β)
        """
        self.distances = distances
        self.pheromones = [[1.0 for _ in range(len(distances))] for _ in range(len(distances))]
        self.n_fourmis = n_fourmis
        self.n_meilleurs = n_meilleurs
        self.n_iterations = n_iterations
        self.decroissance = decroissance
        self.alpha = alpha
        self.beta = beta

        # Liste de tous les indices des villes ex : 0, 1, 2, ..., n-1
        self.tous_indices = range(len(distances))

        # Variables pour stocker le meilleur chemin et la meilleure distance
        self.meilleur_chemin = None
        self.meilleure_distance = float('inf')

    def run(self, callback_maj, evenement_arret):
        """
        Exécute l'algorithme complet.
        
        Paramètres :
        - callback_maj : fonction de callback appelée après chaque itération
        - evenement_arret : threading.Event pour arrêter l'algorithme
        """
        for iteration in range(self.n_iterations):
            # Vérifier si l'arrêt a été demandé
            if evenement_arret.is_set():
                break
            
            # Exécuter une itération
            chemin_courant, distance_courante = self.executer_iteration()
            
            # Appeler le callback de mise à jour
            callback_maj(iteration, chemin_courant, self.pheromones)
            
            # Petite pause pour permettre la mise à jour de l'interface
            time.sleep(0.1)

    def calculer_distance_chemin(self, chemin):
        """
        Calcule la distance totale d'un chemin.

        Paramètres
        ----------
        chemin : list
            Une liste d'indices représentant un chemin.

        Retourne
        -------
        int
            La distance totale du chemin.
        """
        tot = 0
        for i in range(len(chemin) - 1):
            tot += self.distances[chemin[i]][chemin[i+1]]
        return tot
    
    #reprendre ici

    def generer_tous_chemins(self):
        """
        Génère tous les chemins possibles en utilisant l'algorithme d'optimisation par colonie de fourmis.

        Retourne
        -------
        list
            Une liste de tuples, où chaque tuple contient un chemin et sa distance totale.
        """
        # Commencer par une ville aléatoire
        chemin = [random.randint(0, len(self.distances) - 1)]
        
        # Ajouter les autres villes
        while len(chemin) < len(self.distances):
            prochaines_probas = self.calculer_probabilites_mouvement(chemin)
            prochaine_ville = self.choisir_ville_suivante(prochaines_probas)
            chemin.append(prochaine_ville)
        
        return (chemin, self.calculer_distance_chemin(chemin))
        

    def calculer_probabilites_mouvement(self, chemin):
        """
        Calcule la probabilité de se déplacer vers chaque ville étant donné le chemin actuel.

        Paramètres
        ----------
        chemin : list
            Une liste d'indices représentant un chemin.

        Retourne
        -------
        list
            Une liste de probabilités, où chaque probabilité est la probabilité de se déplacer vers chaque ville étant donné le chemin actuel.
        """
        proba = []
        ville_act = chemin[-1]
        for ville in self.tous_indices :
            if ville in chemin :
                proba.append(0)
            else :
                proba.append(self.pheromones[ville_act][ville]**self.alpha*(1/self.distances[ville_act][ville])**self.beta)
        tot = sum(proba)
        if tot > 0 :
            return [p/tot for p in proba]
        else :
            return [0 for _ in range(len(proba))]


    def choisir_ville_suivante(self, probabilites):
        """
        Choisit la prochaine ville en fonction des probabilités données.

        Paramètres
        ----------
        probabilites : list
            Une liste de probabilités, où chaque probabilité est la probabilité de se déplacer vers chaque ville.

        Retourne
        -------
        int
            L'indice de la ville choisie comme prochaine ville.
        """
        barre = random.random()
        compt = 0
        i = 0
        while barre > compt :
            if i == len(probabilites) :
                return len(probabilites) - 1
            else :
                compt += probabilites[i]
                i += 1
        return i - 1
            

    def deposer_pheromones(self, tous_les_chemins):
        """
        Dépose des phéromones sur les meilleurs chemins.

        Paramètres
        ----------
        tous_chemins : list
            Une liste de tuples, où chaque tuple contient un chemin et sa distance totale.

        Retourne
        -------
        None
        """
        # Trier les chemins par distance (du meilleur au pire)
        chemins_tries = sorted(tous_les_chemins, key=lambda x: x[1])
        
        # Déposer des phéromones sur les n_best meilleurs chemins
        for chemin, distance in chemins_tries[:self.n_meilleurs]:
            for i in range(len(chemin) - 1):
                ville1, ville2 = chemin[i], chemin[i+1]
                # La quantité de phéromones est inversement proportionnelle à la distance
                self.pheromones[ville1][ville2] += 1.0 / distance
    

    def evaporer_pheromones(self) :
        phero = len(self.pheromones)
        for i in range(phero) :
            for j in range(phero) :
                self.pheromones[i][j] *= self.decroissance
    
    def executer_iteration(self) :
        # Générer les chemins pour toutes les fourmis
        tous_les_chemins = []
        for _ in range(self.n_fourmis):
            tous_les_chemins.append(self.generer_tous_chemins())
        
        # Trouver le meilleur chemin de cette itération
        meilleur_chemin_iteration = min(tous_les_chemins, key=lambda x: x[1])
        
        # Mettre à jour le meilleur chemin global
        if meilleur_chemin_iteration[1] < self.meilleure_distance:
            self.meilleur_chemin = meilleur_chemin_iteration[0]
            self.meilleure_distance = meilleur_chemin_iteration[1]
        
        # Déposer et évaporer les phéromones
        self.deposer_pheromones(tous_les_chemins)
        self.evaporer_pheromones()
        
        return meilleur_chemin_iteration




if __name__ == "__main__":
    distances = [
        [0, 2, 9, 10],
        [1, 0, 6, 4],
        [15, 7, 0, 8],
        [6, 3, 12, 0]
    ]
    # Créer une instance de la colonie de fourmis
    colonie_fourmis = AntColony(distances, n_fourmis=3, n_meilleurs=5, n_iterations=100, decroissance=0.95, alpha=1, beta=2)
    
    def callback_maj(iteration, meilleur_chemin, pheromones):
        """
        Fonction de callback appeler après chaque itération.

        Paramètres
        ----------
        iteration : int
            L'itération actuelle.
        meilleur_chemin : tuple
            Le meilleur chemin trouvé jusqu'à présent.
        pheromones : list
            La matrice des phéromones.

        Retourne
        -------
        None
        """
        if iteration % 10 == 0:
            print(f"Itération {iteration}: Meilleur chemin {meilleur_chemin} avec distance {colonie_fourmis.meilleure_distance}")
            print("Matrice des phéromones:")
            for ligne in pheromones:
                print(ligne)

    # Créer un événement d'arrêt
    evenement_arret = threading.Event()
    # Exécuter l'algorithme dans le thread principal pour cet exemple
    colonie_fourmis.run(callback_maj, evenement_arret)
    # Meillere chemin trouvé
    print(f"Meilleur chemin trouvé : {colonie_fourmis.meilleur_chemin} avec une distance de {colonie_fourmis.meilleure_distance}")