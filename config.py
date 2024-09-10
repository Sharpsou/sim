# Définition des constantes
GRID_SIZE =15
CELL_SIZE = 15
NUM_FOOD = 10       # Nombre initial de nourriture
NUM_OBSTACLES = 0  # Nombre initial d'obstacles

NOMBRE_PROIE = 10
NOMBRE_CHASSEUR = 10
VITESSE_PROIE = 0.9
VITESSE_CHASSEUR = 0.7
DETECT_PROIE = 10
DETECT_CHASSEUR = 10
VITESSE_SIMU = 1  # Intervalle de mise à jour en millisecondes

# Constantes pour les Proies
ENERGIE_INITIALE_PROIE = 50  # Energie initiale des proies
ENERGIE_DEPLACEMENT_PROIE = 2  # Energie consommée par un déplacement (proie)
ENERGIE_REPOS_PROIE = 0.5  # Energie consommée en restant immobile (proie)
ENERGIE_GAIN_PROIE = 10  # Energie regagnée par une proie près de la nourriture

# Constantes pour les Chasseurs
ENERGIE_INITIALE_CHASSEUR = 150  # Energie initiale des chasseurs
ENERGIE_DEPLACEMENT_CHASSEUR = 1  # Energie consommée par un déplacement (chasseur)
ENERGIE_REPOS_CHASSEUR = 3  # Energie consommée en restant immobile (chasseur)
ENERGIE_GAIN_CHASSEUR = 0  # Energie regagnée par un chasseur près de la nourriture
MUTATION_RATE = 0.1