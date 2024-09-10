# Définition des constantes
GRID_SIZE = 70
CELL_SIZE = 10
NUM_FOOD = 10       # Nombre initial de nourriture
NUM_OBSTACLES = 30  # Nombre initial d'obstacles

NOMBRE_PROIE = 20
NOMBRE_CHASSEUR = 20
VITESSE_PROIE = 0.9
VITESSE_CHASSEUR = 0.8
DETECT_PROIE = 10
DETECT_CHASSEUR = 8
VITESSE_SIMU = 1  # Intervalle de mise à jour en millisecondes

# Constantes pour les Proies
ENERGIE_INITIALE_PROIE = 1000  # Energie initiale des proies
ENERGIE_DEPLACEMENT_PROIE = 2  # Energie consommée par un déplacement (proie)
ENERGIE_REPOS_PROIE = 0.5  # Energie consommée en restant immobile (proie)
ENERGIE_GAIN_PROIE = 10  # Energie regagnée par une proie près de la nourriture

# Constantes pour les Chasseurs
ENERGIE_INITIALE_CHASSEUR = 1000  # Energie initiale des chasseurs
ENERGIE_DEPLACEMENT_CHASSEUR = 3  # Energie consommée par un déplacement (chasseur)
ENERGIE_REPOS_CHASSEUR = 0.7  # Energie consommée en restant immobile (chasseur)
ENERGIE_GAIN_CHASSEUR = 15  # Energie regagnée par un chasseur près de la nourriture