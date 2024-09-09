import math
import random

class CoucheCachee:
    def __init__(self, nombre_neurones: int, nombre_entrees: int):
        """
        Initialise une couche cachée avec un certain nombre de neurones.
        Chaque neurone est associé à un ensemble de poids pour chaque entrée.
        """
        self.neurones = [Neurone(activation="relu") for _ in range(nombre_neurones)]
        # Chaque neurone a un poids par entrée
        self.poids = [[random.uniform(-1, 1) for _ in range(nombre_entrees)] for _ in range(nombre_neurones)]
    
    def calculer_sorties(self, entrees: list[float]) -> list[float]:
        """
        Calcule les sorties de la couche en appliquant les poids et la fonction d'activation
        pour chaque neurone.
        
        :param entrees: Liste des valeurs en entrée venant de la couche précédente.
        :return: Liste des sorties de la couche.
        """
        sorties = []
        for index_neurone, neurone in enumerate(self.neurones):
            somme_ponderee = sum(entree * poids for entree, poids in zip(entrees, self.poids[index_neurone]))
            sortie = neurone.activation_function(somme_ponderee)
            sorties.append(sortie)
        return sorties

class Neurone:
    def __init__(self, activation: str = "relu"):
        """
        Initialise le neurone avec une fonction d'activation.
        Par défaut, la fonction d'activation est ReLU.
        """
        self.activation = activation
    
    def activation_function(self, x: float) -> float:
        """
        Applique la fonction d'activation choisie.
        - ReLU : max(0, x)
        - Tanh : math.tanh(x)
        """
        if self.activation == "relu":
            return max(0, x)
        elif self.activation == "tanh":
            return math.tanh(x)
        else:
            raise ValueError("Fonction d'activation non reconnue.")
    
    def calcul_sortie(self, input_value: float, poids: float) -> float:
        """
        Calcule la somme pondérée et applique la fonction d'activation.
        """
        somme_ponderee = input_value * poids
        return self.activation_function(somme_ponderee)


class IA:
    def __init__(self, nombre_entrees: int, configuration_couches_cachees: list[int], nombre_sorties: int):
        """
        Initialise le réseau neuronal avec une entrée, des couches cachées et une sortie.
        :param nombre_entrees: Le nombre de neurones dans la couche d'entrée.
        :param configuration_couches_cachees: Liste où chaque élément est le nombre de neurones dans une couche cachée.
        :param nombre_sorties: Nombre de neurones dans la couche de sortie.
        """
        # Initialiser les couches cachées
        self.couches_cachees = []
        nombre_entrees_actuel = nombre_entrees

        # Création des couches cachées
        for nombre_neurones in configuration_couches_cachees:
            couche = CoucheCachee(nombre_neurones, nombre_entrees_actuel)
            self.couches_cachees.append(couche)
            nombre_entrees_actuel = nombre_neurones  # Le nombre de sorties d'une couche devient le nombre d'entrées de la suivante
        
        # Création des poids pour la couche de sortie
        self.couche_sortie = CoucheCachee(nombre_sorties, nombre_entrees_actuel)
        # Modifier la fonction d'activation des neurones de la sortie à "tanh"
        for neurone in self.couche_sortie.neurones:
            neurone.activation = "tanh"
    
    def normaliser_entrees(self, entrees: list[float]) -> list[float]:
        """
        Normalise les entrées entre -1 et 1 pour éviter des valeurs trop faibles après normalisation.
        """
        min_val = min(entrees)
        max_val = max(entrees)
        if max_val == min_val:
            return entrees  # Evite la division par zéro si toutes les valeurs sont identiques
        
        # Normalisation entre -1 et 1
        return [2 * (entree - min_val) / (max_val - min_val) - 1 for entree in entrees]


    def forward(self, entrees: list[float]) -> list[float]:
        """
        Réalise la propagation avant à travers tout le réseau.
        :param entrees: Les valeurs d'entrée à transmettre dans le réseau.
        :return: Les valeurs de sortie du réseau.
        """
        entrees_normalisees = self.normaliser_entrees(entrees)

        # Passage à travers chaque couche cachée
        for couche in self.couches_cachees:
            entrees = couche.calculer_sorties(entrees_normalisees)
        
        # Passage à travers la couche de sortie
        sorties = self.couche_sortie.calculer_sorties(entrees)
        return sorties


    def debug_forward(self, entrees: list[float]) -> list[float]:
        """
        Réalise la propagation avant à travers tout le réseau avec des logs pour le débogage.
        :param entrees: Les valeurs d'entrée à transmettre dans le réseau.
        :return: Les valeurs de sortie du réseau.
        """
        print("=== Début de la propagation avant ===")
        print("Entrées initiales :", entrees)
        
        # Passage à travers chaque couche cachée
        for idx, couche in enumerate(self.couches_cachees):
            print(f"\n--- Couche cachée {idx + 1} ---")
            print(f"Entrées de la couche {idx + 1} : {entrees}")
            sorties = []
            for neurone_index, neurone in enumerate(couche.neurones):
                somme_ponderee = sum(entree * poids for entree, poids in zip(entrees, couche.poids[neurone_index]))
                print(f"Neurone {neurone_index + 1} - Somme pondérée : {somme_ponderee}")
                sortie = neurone.activation_function(somme_ponderee)
                print(f"Neurone {neurone_index + 1} - Sortie après activation : {sortie}")
                sorties.append(sortie)
            entrees = sorties
            print(f"Sorties après couche {idx + 1} :", sorties)
        
        # Passage à travers la couche de sortie
        print("\n--- Couche de sortie ---")
        print(f"Entrées de la couche de sortie : {entrees}")
        sorties = []
        for neurone_index, neurone in enumerate(self.couche_sortie.neurones):
            somme_ponderee = sum(entree * poids for entree, poids in zip(entrees, self.couche_sortie.poids[neurone_index]))
            print(f"Neurone de sortie {neurone_index + 1} - Somme pondérée : {somme_ponderee}")
            sortie = neurone.activation_function(somme_ponderee)
            print(f"Neurone de sortie {neurone_index + 1} - Sortie après activation (Tanh) : {sortie}")
            sorties.append(sortie)
        
        print("Sorties finales :", sorties)
        print("=== Fin de la propagation avant ===\n")
        return sorties