# Définition des constantes
GRID_SIZE = 50
CELL_SIZE = 10
NUM_FOOD = 10       # Nombre initial de nourriture
NUM_OBSTACLES = 100  # Nombre initial d'obstacles

NOMBRE_PROIE = 5
NOMBRE_CHASSEUR = 5
VITESSE_PROIE = 1
VITESSE_CHASSEUR = 1
DETECT_PROIE = 10
DETECT_CHASSEUR = 10
VITESSE_SIMU = 10  # Intervalle de mise à jour en millisecondes

# Constantes pour les Proies
ENERGIE_INITIALE_PROIE = 1000  # Energie initiale des proies
ENERGIE_DEPLACEMENT_PROIE = 2  # Energie consommée par un déplacement (proie)
ENERGIE_REPOS_PROIE = 0.5  # Energie consommée en restant immobile (proie)
ENERGIE_GAIN_PROIE = 10  # Energie regagnée par une proie près de la nourriture

# Constantes pour les Chasseurs
ENERGIE_INITIALE_CHASSEUR = 1000  # Energie initiale des chasseurs
ENERGIE_DEPLACEMENT_CHASSEUR = 3  # Energie consommée par un déplacement (chasseur)
ENERGIE_REPOS_CHASSEUR = 1  # Energie consommée en restant immobile (chasseur)
ENERGIE_GAIN_CHASSEUR = 15  # Energie regagnée par un chasseur près de la nourriture