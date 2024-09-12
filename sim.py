import tkinter as tk
import random
from config import *
from ia import IA
import math


class Radar:
    def __init__(self, agent, detection_range, known_obstacles):
        self.agent = agent
        self.detection_range = detection_range
        self.known_obstacles = known_obstacles  # Stocker les obstacles connus pour éviter de les redétecter


    def scan(self, env, num_sectors=4):
        """
        Scanne un carré autour de l'agent et retourne une représentation aplatie
        avec un one-hot encoding pour chaque secteur, modifié par la distance inversée.
        
        :param env: L'environnement de la simulation, contient la grille et les objets.
        :param num_sectors: Nombre de secteurs pour balayer l'espace (par défaut 8 secteurs).
        :return: Liste aplatie de one-hot encodings pondérés par l'inverse de la distance.
        """
        detection_range = self.detection_range
        agent_x, agent_y = self.agent.x, self.agent.y
        
        # Définir l'incrément angulaire pour diviser l'espace en secteurs
        angle_increment = 360 / num_sectors
        sectors = [None] * num_sectors  # Contient les informations par secteur (objet + distance)

        # Liste des catégories d'objets (Chasseur, Proie, Nourriture, Obstacle)
        categories = ['C', 'P', 'N', 'O']
        
        # Balayage dans un carré autour de l'agent
        for dx in range(-detection_range, detection_range + 1):
            for dy in range(-detection_range, detection_range + 1):
                x = agent_x + dx
                y = agent_y + dy
                
                # Vérifier que les coordonnées sont dans les limites de la grille
                if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
                    continue

                # Ne pas détecter l'agent lui-même
                if x == agent_x and y == agent_y:
                    continue

                # Calcul de la distance et de l'angle
                distance = math.sqrt(dx**2 + dy**2)
                if distance > detection_range:
                    continue  # L'objet est hors du rayon de détection

                # Calculer l'angle en radians et convertir en degrés
                angle = math.atan2(dy, dx)
                angle = math.degrees(angle)
                if angle < 0:
                    angle += 360  # Convertir les angles négatifs en positifs

                # Identifier le secteur correspondant
                sector = int(angle // angle_increment)

                # Détection de l'objet à cette position
                obj = env.grid[x][y]
                if obj == ' ':
                    continue  # Pas d'objet détecté

                # Assigner un type en fonction de l'objet détecté
                if isinstance(obj, Chasseur):
                    detected_type = 'C'
                elif isinstance(obj, Proie):
                    detected_type = 'P'
                elif obj == 'N':  # Nourriture
                    detected_type = 'N'
                elif obj == 'O':  # Obstacle
                    detected_type = 'O'
                else:
                    continue  # Si l'objet ne fait pas partie des types à détecter

                # Inverser la distance pour la normaliser entre 1 et 0.1
                normalized_distance = 1 - (distance / detection_range) * 0.9

                # Si aucun objet détecté dans ce secteur, ou si cet objet est plus proche
                if sectors[sector] is None or sectors[sector]['distance'] < normalized_distance:
                    sectors[sector] = {'type': detected_type, 'distance': normalized_distance}

        # Créer la sortie one-hot encodée avec la distance inversée
        one_hot_data = []
        for sector in sectors:
            # Initialiser un vecteur one-hot à 0
            one_hot_vector = [0] * len(categories)

            if sector is not None:
                # Trouver l'index de l'objet détecté
                index = categories.index(sector['type'])
                # Placer la distance normalisée dans le vecteur one-hot
                one_hot_vector[index] = sector['distance']

            # Ajouter ce vecteur au résultat
            one_hot_data.extend(one_hot_vector)

        return one_hot_data









class Agent:
    def __init__(self, x, y, agent_type, env, detection_range, vitesse, energie_init, energie_deplacement, energie_repos, energie_gain):
        self.x = x
        self.y = y
        self.agent_type = agent_type
        self.env = env
        self.radar = Radar(self, detection_range, env.obstacles)  # Chaque agent a son propre radar
        self.vitesse = vitesse  # Vitesse entre 0 et 1, utilisée comme probabilité de mouvement
        self.energie = energie_init  # Energie initiale de l'agent
        self.energie_deplacement = energie_deplacement
        self.energie_repos = energie_repos
        self.energie_gain = energie_gain
        self.energie_init = energie_init  # Stocker l'énergie initiale pour restaurer un chasseur
        self.tours_pres_nourriture = 0  # Compteur de tours près de la nourriture

        # Initialiser l'IA de l'agent
        input_size = 17  # Par exemple, 8 secteurs radar + 1 pour l'énergie
        layer_sizes = [5,-5, 5]  # Paramétrable : nombre de neurones dans chaque couche
        output_size = 2
        self.ia = IA(input_size, layer_sizes, output_size)  # Poids et seuils générés aléatoirement dans IA

    def decide(self, radar_data):
        """
        Utilise l'IA pour décider du mouvement de l'agent.
        :param radar_data: Données du radar (sous forme de liste)
        :return: Mouvement décidé par l'IA
        """
        energie_norm = 1 - self.energie / self.energie_init
        # Combiner les données du radar (flattées) et l'énergie dans une liste
        inputs = radar_data + [energie_norm]  # Ajouter l'énergie comme dernier élément
        
        # Obtenir la sortie du réseau de neurones
        output = self.ia.forward(inputs)
        
        # Interpréter la sortie comme un déplacement (par exemple, 2 neurones de sortie)
        dx = -1 if output[0] < -0.33 else (0 if output[0] < 0.33 else 1)
        dy = -1 if output[1] < -0.33 else (0 if output[1] < 0.33 else 1)
        
        return dx, dy

    def move(self, dx, dy):
        """
        Gère le déplacement de l'agent sur la grille.
        """
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Vérifier si le nouvel emplacement est dans les limites de la grille
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            target = self.env.grid[new_x][new_y]
            if isinstance(self, Chasseur) and isinstance(target, Proie):
                # Le chasseur attaque la proie
                target.energie = 0  # Proie perd toute son énergie
                self.env.remove_agent(target)  # La proie disparaît
                self.energie = self.energie_init  # Le chasseur récupère son énergie initiale
            elif target == ' ':
                # Se déplacer sur une case vide
                self.env.grid[self.x][self.y] = ' '  # Vide l'ancienne position
                self.x, self.y = new_x, new_y
                self.env.grid[self.x][self.y] = self  # Met l'agent dans la nouvelle position
                self.energie -= self.energie_deplacement  # Diminuer l'énergie plus rapidement lors du déplacement
                self.tours_pres_nourriture = 0  # Réinitialiser le compteur lorsqu'il se déplace
                if self.energie < 0:  # S'assurer que l'énergie ne descend pas en dessous de 0
                    self.energie = 0

    def check_nourriture(self):
        """
        Vérifie si l'agent est près de la nourriture et lui permet de regagner de l'énergie.
        """
        directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        for dx, dy in directions:
            x = self.x + dx
            y = self.y + dy
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                if self.env.grid[x][y] == 'N':  # Si de la nourriture est à proximité
                    self.tours_pres_nourriture += 1
                    if self.tours_pres_nourriture > 1:  # S'il reste plus d'un tour à côté de la nourriture
                        self.energie += self.energie_gain  # Augmenter l'énergie
                        if self.energie > self.env.max_energie(self.agent_type):  # Limiter l'énergie à la valeur initiale
                            self.energie = self.env.max_energie(self.agent_type)
                    return
        self.tours_pres_nourriture = 0  # Réinitialiser si pas de nourriture à proximité

    def update(self):
        """
        Met à jour l'état de l'agent à chaque tour. 
        L'agent peut se déplacer et son énergie diminue dans tous les cas.
        """
        if self.energie == 0:  # Si l'énergie atteint 0, l'agent disparaît
            self.env.remove_agent(self)
            return
        
        if self.energie > 0:  # Vérifier que l'agent a encore de l'énergie pour bouger
            if random.random() < self.vitesse:  # Tirage aléatoire pour décider si l'agent se déplace
                radar_data = self.radar.scan(self.env)
                dx, dy = self.decide(radar_data)
                self.move(dx, dy)
            else:
                # L'agent reste immobile, on diminue l'énergie plus lentement
                self.energie -= self.energie_repos  # Diminuer l'énergie plus lentement lorsqu'il reste immobile
                if self.energie < 0:  # S'assurer que l'énergie ne descend pas en dessous de 0
                    self.energie = 0
            self.check_nourriture()  # Vérifier si l'agent est près de la nourriture



class Chasseur(Agent):
    def __init__(self, x, y, env):
        super().__init__(x, y, 'C', env, detection_range=DETECT_CHASSEUR, vitesse=VITESSE_CHASSEUR,
                         energie_init=ENERGIE_INITIALE_CHASSEUR, energie_deplacement=ENERGIE_DEPLACEMENT_CHASSEUR,
                         energie_repos=ENERGIE_REPOS_CHASSEUR, energie_gain=ENERGIE_GAIN_CHASSEUR)


class Proie(Agent):
    def __init__(self, x, y, env):
        super().__init__(x, y, 'P', env, detection_range=DETECT_PROIE, vitesse=VITESSE_PROIE,
                         energie_init=ENERGIE_INITIALE_PROIE, energie_deplacement=ENERGIE_DEPLACEMENT_PROIE,
                         energie_repos=ENERGIE_REPOS_PROIE, energie_gain=ENERGIE_GAIN_PROIE)




class Environnement:
    def __init__(self):
        self.grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Initialisation de la grille
        self.agents = []  # Liste des agents (chasseurs et proies)
        self.obstacles = []  # Stocker les positions des obstacles
        self.reproduction_counter_proie = 0  # Compteur de reproduction pour les proies
        self.reproduction_counter_chasseur = 0  # Compteur de reproduction pour les chasseurs
        self.place_items('N', NUM_FOOD)  # Placement de la nourriture
        self.place_items('O', NUM_OBSTACLES)  # Placement des obstacles

    def place_items(self, item_type, count):
        """
        Place un certain nombre d'items (nourriture ou obstacles) sur la grille.
        
        :param item_type: 'N' pour nourriture, 'O' pour obstacle.
        :param count: Nombre d'items à placer.
        """
        for _ in range(count):
            while True:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                if self.grid[x][y] == ' ':  # Placer uniquement sur des cases vides
                    self.grid[x][y] = item_type
                    if item_type == 'O':  # Ajouter les obstacles à la liste
                        self.obstacles.append((x, y))
                    break

    def add_agent(self, agent):
        """
        Ajoute un agent dans l'environnement et met à jour la grille.
        
        :param agent: Instance de Chasseur ou Proie à ajouter.
        """
        self.agents.append(agent)
        self.grid[agent.x][agent.y] = agent  # Stocker l'agent dans la grille

    def remove_agent(self, agent):
        """
        Supprime un agent de l'environnement et met à jour la grille.
        
        :param agent: Instance de Chasseur ou Proie à supprimer.
        """
        if agent in self.agents:
            self.agents.remove(agent)
            self.grid[agent.x][agent.y] = ' '  # Marquer la case comme vide dans la grille

    def update(self):
        """
        Met à jour tous les agents dans l'environnement et vérifie les conditions de reproduction.
        """
        for agent in self.agents[:]:
            agent.update()  # Mise à jour de chaque agent (déplacement, consommation d'énergie, etc.)

        # Vérifier si la reproduction doit être déclenchée pour les proies
        if len([a for a in self.agents if isinstance(a, Proie)]) <= NOMBRE_PROIE // 2:
            self.reproduction('P')

        # Vérifier si la reproduction doit être déclenchée pour les chasseurs
        if len([a for a in self.agents if isinstance(a, Chasseur)]) <= NOMBRE_CHASSEUR // 2:
            self.reproduction('C')

    def reproduction(self, agent_type, mutation_rate=0.01):
        """
        Gère la reproduction des agents du même type (proies ou chasseurs).
        
        :param agent_type: 'P' pour Proie ou 'C' pour Chasseur.
        :param mutation_rate: Taux de mutation appliqué lors de la reproduction.
        """
        # Filtrer les agents du même type
        agents_of_type = [agent for agent in self.agents if agent.agent_type == agent_type]

        # Vérifier si la population est réduite à la moitié ou moins
        if len(agents_of_type) <= (NOMBRE_PROIE // 2 if agent_type == 'P' else NOMBRE_CHASSEUR // 2):
            print(f"Reproduction de {agent_type}s activée.")
            
            # Mélanger les agents pour former des paires
            random.shuffle(agents_of_type)
            num_pairs = len(agents_of_type) // 2  # Nombre de couples

            for i in range(num_pairs):
                parent1 = agents_of_type[i * 2]
                parent2 = agents_of_type[i * 2 + 1]

                # Mélanger les poids Fully-Connected seulement (on ignore les couches GRU)
                new_weights_1, new_weights_2 = self.mix_weights(parent1.ia.weights, parent2.ia.weights, mutation_rate)

                # Créer deux nouveaux agents avec les poids mélangés
                if agent_type == 'C':
                    new_agent1 = Chasseur(random.randint(0, GRID_SIZE // 4), random.randint(0, GRID_SIZE // 4), self)
                    new_agent2 = Chasseur(random.randint(0, GRID_SIZE // 4), random.randint(0, GRID_SIZE // 4), self)
                else:
                    new_agent1 = Proie(random.randint(3 * GRID_SIZE // 4, GRID_SIZE - 1), random.randint(3 * GRID_SIZE // 4, GRID_SIZE - 1), self)
                    new_agent2 = Proie(random.randint(3 * GRID_SIZE // 4, GRID_SIZE - 1), random.randint(3 * GRID_SIZE // 4, GRID_SIZE - 1), self)

                # Assigner les nouveaux poids aux agents créés
                new_agent1.ia.weights = new_weights_1
                new_agent2.ia.weights = new_weights_2

                # Ajouter les nouveaux agents à l'environnement
                self.add_agent(new_agent1)
                self.add_agent(new_agent2)

            # Incrémenter le compteur de reproduction
            if agent_type == 'C':
                self.reproduction_counter_chasseur += 1
            else:
                self.reproduction_counter_proie += 1


    def mix_weights(self, weights1, weights2, mutation_rate):
        """
        Mélange les poids de deux agents et applique des mutations aléatoires.
        Gère les poids qui peuvent être soit des floats individuels, soit des listes de floats.
        
        :param weights1: Poids du premier parent (une liste de couches ou des floats).
        :param weights2: Poids du deuxième parent.
        :param mutation_rate: Taux de mutation appliqué aux nouveaux poids.
        :return: Deux nouveaux ensembles de poids issus du mélange.
        """
        new_weights_1 = []
        new_weights_2 = []

        # Pour chaque couche ou ensemble de poids, on mélange les poids des deux parents
        for layer_weights1, layer_weights2 in zip(weights1, weights2):
            # Si les poids sont des floats, on les traite directement comme des poids individuels
            if isinstance(layer_weights1, float) and isinstance(layer_weights2, float):
                # Mélanger et appliquer la mutation directement sur les floats
                new_w1, new_w2 = layer_weights1, layer_weights2
                if random.random() < 0.5:
                    new_w1, new_w2 = layer_weights2, layer_weights1

                # Appliquer des mutations aléatoires sur le poids de new_w1 et new_w2
                if random.random() < mutation_rate:
                    new_w1 += random.uniform(-0.1, 0.1)
                if random.random() < mutation_rate:
                    new_w2 += random.uniform(-0.1, 0.1)

                new_weights_1.append(new_w1)
                new_weights_2.append(new_w2)

            # Si les poids sont des listes (couches), on appelle récursivement mix_weights
            elif isinstance(layer_weights1, list) and isinstance(layer_weights2, list):
                sub_weights_1, sub_weights_2 = self.mix_weights(layer_weights1, layer_weights2, mutation_rate)
                new_weights_1.append(sub_weights_1)
                new_weights_2.append(sub_weights_2)

            else:
                raise TypeError(f"Les types des poids ne correspondent pas : {type(layer_weights1)} et {type(layer_weights2)}")

        return new_weights_1, new_weights_2






    def max_energie(self, agent_type):
        """
        Retourne l'énergie maximale d'un agent en fonction de son type.
        
        :param agent_type: 'C' pour Chasseur, 'P' pour Proie.
        :return: Energie maximale pour le type d'agent.
        """
        if agent_type == 'C':
            return ENERGIE_INITIALE_CHASSEUR
        elif agent_type == 'P':
            return ENERGIE_INITIALE_PROIE
        return 0
