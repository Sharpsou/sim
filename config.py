# Définition des constantes
GRID_SIZE =45
CELL_SIZE = 15
NUM_FOOD = 20       # Nombre initial de nourriture
NUM_OBSTACLES = 0  # Nombre initial d'obstacles

NOMBRE_PROIE = 10
NOMBRE_CHASSEUR = 10
VITESSE_PROIE = 0.7
VITESSE_CHASSEUR = 0.5
DETECT_PROIE = 20
DETECT_CHASSEUR = 40
VITESSE_SIMU = 1  # Intervalle de mise à jour en millisecondes

# Constantes pour les Proies
ENERGIE_INITIALE_PROIE = 150  # Energie initiale des proies
ENERGIE_DEPLACEMENT_PROIE = 4  # Energie consommée par un déplacement (proie)
ENERGIE_REPOS_PROIE = 2  # Energie consommée en restant immobile (proie)
ENERGIE_GAIN_PROIE = 5  # Energie regagnée par une proie près de la nourriture

# Constantes pour les Chasseurs
ENERGIE_INITIALE_CHASSEUR = 250  # Energie initiale des chasseurs
ENERGIE_DEPLACEMENT_CHASSEUR = 0  # Energie consommée par un déplacement (chasseur)
ENERGIE_REPOS_CHASSEUR = 2  # Energie consommée en restant immobile (chasseur)
ENERGIE_GAIN_CHASSEUR = 0  # Energie regagnée par un chasseur près de la nourriture
MUTATION_RATE = 0.01