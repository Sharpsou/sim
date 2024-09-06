import tkinter as tk
import random
from config import *


class Radar:
    def __init__(self, agent, detection_range, known_obstacles):
        self.agent = agent
        self.detection_range = detection_range
        self.known_obstacles = known_obstacles  # Stocker les obstacles connus pour éviter de les redétecter

    def scan(self, env):
        directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        detections = [{'C': 0, 'P': 0, 'N': 0, 'O': 0} for _ in range(8)]
        
        for idx, (dx, dy) in enumerate(directions):
            for dist in range(1, self.detection_range + 1):
                x = self.agent.x + dx * dist
                y = self.agent.y + dy * dist
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:  # Vérifier que les coordonnées sont dans la grille
                    if (x, y) in self.known_obstacles:  # Utiliser la liste d'obstacles connus
                        detections[idx]['O'] = dist / self.detection_range
                        break
                    
                    obj = env.grid[x][y]
                    if obj != ' ':  # Si un objet est détecté
                        normalized_distance = dist / self.detection_range
                        if isinstance(obj, Chasseur):
                            key = 'C'
                        elif isinstance(obj, Proie):
                            key = 'P'
                        else:
                            key = obj  # Pour 'N', 'O', ou autre

                        if detections[idx][key] == 0 or normalized_distance < detections[idx][key]:
                            detections[idx][key] = normalized_distance
                        if key == 'O':  # Si un obstacle est détecté, enregistrer la distance et arrêter la détection
                            break
        return detections


class Communication:
    def __init__(self):
        self.message = [False, False, False, False]

    def exchange(self, other_agent):
        # Implémentation simplifiée de l'échange de communication
        for i in range(len(self.message)):
            self.message[i] = self.message[i] or other_agent.comm.message[i]


class Logic:
    def __init__(self):
        self.ponderation = 10

    def decide(self, radar_data, energie, communication):
        
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])

        return dx, dy, communication



class Agent:
    def __init__(self, x, y, agent_type, env, detection_range, vitesse, energie_init, energie_deplacement, energie_repos, energie_gain):
        self.x = x
        self.y = y
        self.agent_type = agent_type
        self.env = env
        self.radar = Radar(self, detection_range, env.obstacles)  # Chaque agent a son propre radar
        self.comm = Communication()
        self.logic = Logic()  # Chaque agent a sa propre logique
        self.vitesse = vitesse  # Vitesse entre 0 et 1, utilisée comme probabilité de mouvement
        self.energie = energie_init  # Energie initiale de l'agent
        self.energie_deplacement = energie_deplacement
        self.energie_repos = energie_repos
        self.energie_gain = energie_gain
        self.energie_init = energie_init  # Stocker l'énergie initiale pour restaurer un chasseur
        self.tours_pres_nourriture = 0  # Compteur de tours près de la nourriture

    def move(self, dx, dy):
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
        # Vérifier s'il y a de la nourriture autour de l'agent
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
        if self.energie == 0:  # Si l'énergie atteint 0, l'agent disparaît
            self.env.remove_agent(self)
            return
        
        if self.energie > 0:  # Vérifier que l'agent a encore de l'énergie pour bouger
            if random.random() < self.vitesse:  # Tirage aléatoire pour décider si l'agent se déplace
                radar_data = self.radar.scan(self.env)
                dx, dy, new_comm = self.logic.decide(radar_data,self.energie, self.comm)
                self.comm = new_comm
                self.move(dx, dy)
            else:
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
        self.grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.agents = []
        self.obstacles = []  # Stocker les positions des obstacles
        self.place_items('N', NUM_FOOD)
        self.place_items('O', NUM_OBSTACLES)

    def place_items(self, item_type, count):
        for _ in range(count):
            while True:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                if self.grid[x][y] == ' ':
                    self.grid[x][y] = item_type
                    if item_type == 'O':  # Ajouter les obstacles dans la liste
                        self.obstacles.append((x, y))
                    break

    def add_agent(self, agent):
        self.agents.append(agent)
        self.grid[agent.x][agent.y] = agent  # Stocker l'agent dans la grille

    def update(self):
        for agent in self.agents[:]:
            agent.update()

    def remove_agent(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)
            self.grid[agent.x][agent.y] = ' '  # Effacer l'agent de la grille

    def max_energie(self, agent_type):
        if agent_type == 'C':
            return ENERGIE_INITIALE_CHASSEUR
        elif agent_type == 'P':
            return ENERGIE_INITIALE_PROIE
        return 0


class SimulationApp:
    def __init__(self, root):
        self.env = Environnement()
        self.canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
        self.canvas.pack()
        self.create_agents()
        self.draw_obstacles()  # Dessiner les obstacles une seule fois
        self.update_canvas()

    def create_agents(self):
        # Spawner les chasseurs dans le quart supérieur gauche
        for _ in range(NOMBRE_CHASSEUR):
            while True:
                chasseur_x = random.randint(0, GRID_SIZE // 4)
                chasseur_y = random.randint(0, GRID_SIZE // 4)
                if self.env.grid[chasseur_x][chasseur_y] == ' ':
                    chasseur = Chasseur(chasseur_x, chasseur_y, self.env)
                    self.env.add_agent(chasseur)
                    break

        # Spawner les proies dans le quart inférieur droit
        for _ in range(NOMBRE_PROIE):
            while True:
                proie_x = random.randint(3 * GRID_SIZE // 4, GRID_SIZE - 1)
                proie_y = random.randint(3 * GRID_SIZE // 4, GRID_SIZE - 1)
                if self.env.grid[proie_x][proie_y] == ' ':
                    proie = Proie(proie_x, proie_y, self.env)
                    self.env.add_agent(proie)
                    break

    def draw_obstacles(self):
        # Dessiner tous les obstacles une seule fois
        for x, y in self.env.obstacles:
            x1 = x * CELL_SIZE
            y1 = y * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

    def update_canvas(self):
        self.env.update()
        self.canvas.delete("agents")  # Supprimer uniquement les agents, pas les obstacles
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x1 = i * CELL_SIZE
                y1 = j * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                if isinstance(self.env.grid[i][j], Agent):
                    agent = self.env.grid[i][j]
                    agent_color = "red" if agent.agent_type == 'C' else "blue"
                    # Dessiner l'agent
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=agent_color, tags="agents")
                    # Dessiner la barre d'énergie
                    energie_ratio = agent.energie / self.env.max_energie(agent.agent_type)
                    energie_x1 = x1 + 2
                    energie_y1 = y1 + 2
                    energie_x2 = x1 + (CELL_SIZE - 4) * energie_ratio
                    energie_y2 = y1 + 5
                    self.canvas.create_rectangle(energie_x1, energie_y1, energie_x2, energie_y2, fill="green", tags="agents")
                elif self.env.grid[i][j] == 'N':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", tags="agents")
        root.after(VITESSE_SIMU, self.update_canvas)


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()
