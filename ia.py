import numpy as np
import math
import random

# Classe pour la couche Fully-Connected
class CoucheCachee:
    def __init__(self, nombre_neurones: int, nombre_entrees: int):
        """
        Initialise une couche fully-connected avec un certain nombre de neurones et de connexions en entrée.
        """
        self.neurones = [Neurone() for _ in range(nombre_neurones)]
        self.poids = [[random.uniform(-1, 1) for _ in range(nombre_entrees)] for _ in range(nombre_neurones)]
    
    def calculer_sorties(self, entrees: list[float]) -> list[float]:
        """
        Calcule les sorties de la couche Fully-Connected.
        """
        sorties = []
        for index_neurone, neurone in enumerate(self.neurones):
            somme_ponderee = sum(entree * poids for entree, poids in zip(entrees, self.poids[index_neurone]))
            sortie = neurone.activation_function(somme_ponderee)
            sorties.append(sortie)
        return sorties


# Classe pour les neurones classiques
class Neurone:
    def __init__(self, activation: str = "relu"):
        self.activation = activation
    
    def activation_function(self, x: float) -> float:
        if self.activation == "relu":
            return max(0, x)
        elif self.activation == "tanh":
            return math.tanh(x)
        else:
            raise ValueError("Fonction d'activation non reconnue.")


# Classe pour une couche GRU
class GRU:
    def __init__(self, nombre_neurones: int, nombre_entrees: int):
        """
        Initialisation du GRU avec le nombre de neurones et le nombre d'entrées.
        """
        self.nombre_neurones = nombre_neurones
        self.nombre_entrees = nombre_entrees
        
        # Initialisation des poids pour les différentes portes (reset, update, candidate)
        self.W_r = np.random.uniform(-1, 1, (nombre_neurones, nombre_entrees))  # Poids de la porte de réinitialisation
        self.U_r = np.random.uniform(-1, 1, (nombre_neurones, nombre_neurones)) # Poids de la porte de réinitialisation sur h_t-1
        
        self.W_z = np.random.uniform(-1, 1, (nombre_neurones, nombre_entrees))  # Poids de la porte de mise à jour
        self.U_z = np.random.uniform(-1, 1, (nombre_neurones, nombre_neurones)) # Poids de la porte de mise à jour sur h_t-1
        
        self.W_h = np.random.uniform(-1, 1, (nombre_neurones, nombre_entrees))  # Poids de la nouvelle entrée candidate
        self.U_h = np.random.uniform(-1, 1, (nombre_neurones, nombre_neurones)) # Poids de la nouvelle entrée candidate sur h_t-1
        
        self.h_t = np.zeros((nombre_neurones,))  # Initialisation de l'état caché à zéro

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def tanh(self, x):
        return np.tanh(x)

    def calculer_sorties(self, x_t):
        """
        Calcule les sorties de la couche GRU.
        """
        r_t = self.sigmoid(np.dot(self.W_r, x_t) + np.dot(self.U_r, self.h_t))  # Porte de réinitialisation
        z_t = self.sigmoid(np.dot(self.W_z, x_t) + np.dot(self.U_z, self.h_t))  # Porte de mise à jour
        h_candidat = self.tanh(np.dot(self.W_h, x_t) + np.dot(self.U_h, r_t * self.h_t))  # Candidat à l'état
        self.h_t = (1 - z_t) * self.h_t + z_t * h_candidat  # Mise à jour de l'état caché
        return self.h_t

# Classe pour la version GRU Neurone unique
class GRUNeurone(Neurone):
    def __init__(self, nombre_neurones: int, nombre_entrees: int):
        """
        Similaire à un neurone classique, mais avec le comportement d'un GRU.
        """
        self.gru = GRU(nombre_neurones, nombre_entrees)

    def activation_function(self, x: list[float]) -> list[float]:
        return self.gru.calculer_sorties(x)


# Classe du réseau neuronal général

class IA:
    def __init__(self, nombre_entrees: int, configuration_couches_cachees: list[int], nombre_sorties: int):
        """
        Initialise le réseau neuronal avec une entrée, des couches cachées et une sortie.
        """
        self.couches_cachees = []
        self.weights = []  # Ajout d'un attribut pour stocker les poids
        nombre_entrees_actuel = nombre_entrees

        # Création des couches cachées
        for nombre_neurones in configuration_couches_cachees:
            if nombre_neurones < 0:
                # Création d'une couche avec des neurones GRU
                couche = GRU(abs(nombre_neurones), nombre_entrees_actuel)
                # Aucune manipulation explicite des poids dans le cas des GRU
            else:
                # Création d'une couche Fully-Connected classique
                couche = CoucheCachee(nombre_neurones, nombre_entrees_actuel)
                self.weights.append(couche.poids)  # Ajoute les poids de la couche au tableau des poids
            
            self.couches_cachees.append(couche)
            nombre_entrees_actuel = abs(nombre_neurones)
        
        # Création de la couche de sortie
        self.couche_sortie = CoucheCachee(nombre_sorties, nombre_entrees_actuel)
        for neurone in self.couche_sortie.neurones:
            neurone.activation = "tanh"

        # Stocker également les poids de la couche de sortie
        self.weights.append(self.couche_sortie.poids)

    def forward(self, entrees: list[float]) -> list[float]:
        """
        Effectue la propagation avant à travers toutes les couches du réseau.
        :param entrees: Liste des valeurs d'entrée.
        :return: Liste des valeurs de sortie.
        """
        activations = entrees  # Les entrées deviennent les premières activations

        # Propagation à travers chaque couche cachée (Fully-Connected ou GRU)
        for couche in self.couches_cachees:
            if isinstance(couche, GRU):
                # Si c'est une couche GRU, on utilise son mécanisme de calcul de sortie
                activations = couche.calculer_sorties(activations)
            else:
                # Si c'est une couche Fully-Connected, on fait une propagation avant normale
                activations = couche.calculer_sorties(activations)

        # Propagation à travers la couche de sortie
        sorties = self.couche_sortie.calculer_sorties(activations)
        return sorties
