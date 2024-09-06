# Définition des constantes
GRID_SIZE = 25
CELL_SIZE = 15
NUM_FOOD = 40       # Nombre initial de nourriture
NUM_OBSTACLES = 10  # Nombre initial d'obstacles

NOMBRE_PROIE = 15
NOMBRE_CHASSEUR = 15
VITESSE_PROIE = 0.3
VITESSE_CHASSEUR = 0.4
DETECT_PROIE = 7
DETECT_CHASSEUR = 5
VITESSE_SIMU = 10  # Intervalle de mise à jour en millisecondes

# Constantes pour les Proies
ENERGIE_INITIALE_PROIE = 100  # Energie initiale des proies
ENERGIE_DEPLACEMENT_PROIE = 2  # Energie consommée par un déplacement (proie)
ENERGIE_REPOS_PROIE = 0.5  # Energie consommée en restant immobile (proie)
ENERGIE_GAIN_PROIE = 10  # Energie regagnée par une proie près de la nourriture

# Constantes pour les Chasseurs
ENERGIE_INITIALE_CHASSEUR = 100  # Energie initiale des chasseurs
ENERGIE_DEPLACEMENT_CHASSEUR = 3  # Energie consommée par un déplacement (chasseur)
ENERGIE_REPOS_CHASSEUR = 1  # Energie consommée en restant immobile (chasseur)
ENERGIE_GAIN_CHASSEUR = 15  # Energie regagnée par un chasseur près de la nourriture