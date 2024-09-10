import tkinter as tk
import random
from sim import *
from config import *

# Ajoutez ici vos imports nécessaires comme `Chasseur`, `Proie`, `Environnement`, etc.

class ConfigurationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuration Simulation")

        
        # Paramètres globaux
        self.grid_size_label = tk.Label(root, text="Taille de la grille (GRID_SIZE):")
        self.grid_size_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.grid_size_entry = tk.Entry(root)
        self.grid_size_entry.insert(0, GRID_SIZE)
        self.grid_size_entry.grid(row=0, column=1, padx=10, pady=5)

        self.cell_size_label = tk.Label(root, text="Taille des cellules (CELL_SIZE):")
        self.cell_size_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.cell_size_entry = tk.Entry(root)
        self.cell_size_entry.insert(0, CELL_SIZE)
        self.cell_size_entry.grid(row=1, column=1, padx=10, pady=5)

        self.num_food_label = tk.Label(root, text="Nombre de nourriture (NUM_FOOD):")
        self.num_food_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.num_food_entry = tk.Entry(root)
        self.num_food_entry.insert(0, NUM_FOOD)
        self.num_food_entry.grid(row=2, column=1, padx=10, pady=5)

        self.num_obstacles_label = tk.Label(root, text="Nombre d'obstacles (NUM_OBSTACLES):")
        self.num_obstacles_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.num_obstacles_entry = tk.Entry(root)
        self.num_obstacles_entry.insert(0, NUM_OBSTACLES)
        self.num_obstacles_entry.grid(row=3, column=1, padx=10, pady=5)

        # Paramètres des proies
        self.num_proie_label = tk.Label(root, text="Nombre de proies (NOMBRE_PROIE):")
        self.num_proie_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.num_proie_entry = tk.Entry(root)
        self.num_proie_entry.insert(0, NOMBRE_PROIE)
        self.num_proie_entry.grid(row=4, column=1, padx=10, pady=5)

        self.vitesse_proie_label = tk.Label(root, text="Vitesse des proies (VITESSE_PROIE):")
        self.vitesse_proie_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.vitesse_proie_entry = tk.Entry(root)
        self.vitesse_proie_entry.insert(0, VITESSE_PROIE)
        self.vitesse_proie_entry.grid(row=5, column=1, padx=10, pady=5)

        self.detect_proie_label = tk.Label(root, text="Portée de détection des proies (DETECT_PROIE):")
        self.detect_proie_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.detect_proie_entry = tk.Entry(root)
        self.detect_proie_entry.insert(0, DETECT_PROIE)
        self.detect_proie_entry.grid(row=6, column=1, padx=10, pady=5)

        self.energie_proie_label = tk.Label(root, text="Énergie initiale des proies (ENERGIE_INITIALE_PROIE):")
        self.energie_proie_label.grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.energie_proie_entry = tk.Entry(root)
        self.energie_proie_entry.insert(0, ENERGIE_INITIALE_PROIE)
        self.energie_proie_entry.grid(row=7, column=1, padx=10, pady=5)

        self.energie_deplacement_proie_label = tk.Label(root, text="Énergie déplacement proie (ENERGIE_DEPLACEMENT_PROIE):")
        self.energie_deplacement_proie_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
        self.energie_deplacement_proie_entry = tk.Entry(root)
        self.energie_deplacement_proie_entry.insert(0, ENERGIE_DEPLACEMENT_PROIE)
        self.energie_deplacement_proie_entry.grid(row=8, column=1, padx=10, pady=5)

        self.energie_repos_proie_label = tk.Label(root, text="Énergie repos proie (ENERGIE_REPOS_PROIE):")
        self.energie_repos_proie_label.grid(row=9, column=0, padx=10, pady=5, sticky="e")
        self.energie_repos_proie_entry = tk.Entry(root)
        self.energie_repos_proie_entry.insert(0, ENERGIE_REPOS_PROIE)
        self.energie_repos_proie_entry.grid(row=9, column=1, padx=10, pady=5)

        self.energie_gain_proie_label = tk.Label(root, text="Énergie gain proie (ENERGIE_GAIN_PROIE):")
        self.energie_gain_proie_label.grid(row=10, column=0, padx=10, pady=5, sticky="e")
        self.energie_gain_proie_entry = tk.Entry(root)
        self.energie_gain_proie_entry.insert(0, ENERGIE_GAIN_PROIE)
        self.energie_gain_proie_entry.grid(row=10, column=1, padx=10, pady=5)

        # Paramètres des chasseurs
        self.num_chasseur_label = tk.Label(root, text="Nombre de chasseurs (NOMBRE_CHASSEUR):")
        self.num_chasseur_label.grid(row=11, column=0, padx=10, pady=5, sticky="e")
        self.num_chasseur_entry = tk.Entry(root)
        self.num_chasseur_entry.insert(0, NOMBRE_CHASSEUR)
        self.num_chasseur_entry.grid(row=11, column=1, padx=10, pady=5)

        self.vitesse_chasseur_label = tk.Label(root, text="Vitesse des chasseurs (VITESSE_CHASSEUR):")
        self.vitesse_chasseur_label.grid(row=12, column=0, padx=10, pady=5, sticky="e")
        self.vitesse_chasseur_entry = tk.Entry(root)
        self.vitesse_chasseur_entry.insert(0, VITESSE_CHASSEUR)
        self.vitesse_chasseur_entry.grid(row=12, column=1, padx=10, pady=5)

        self.detect_chasseur_label = tk.Label(root, text="Portée de détection des chasseurs (DETECT_CHASSEUR):")
        self.detect_chasseur_label.grid(row=13, column=0, padx=10, pady=5, sticky="e")
        self.detect_chasseur_entry = tk.Entry(root)
        self.detect_chasseur_entry.insert(0, DETECT_CHASSEUR)
        self.detect_chasseur_entry.grid(row=13, column=1, padx=10, pady=5)

        self.energie_initiale_chasseur_label = tk.Label(root, text="Énergie initiale des chasseurs (ENERGIE_INITIALE_CHASSEUR):")
        self.energie_initiale_chasseur_label.grid(row=14, column=0, padx=10, pady=5, sticky="e")
        self.energie_initiale_chasseur_entry = tk.Entry(root)
        self.energie_initiale_chasseur_entry.insert(0, ENERGIE_INITIALE_CHASSEUR)
        self.energie_initiale_chasseur_entry.grid(row=14, column=1, padx=10, pady=5)

        self.energie_deplacement_chasseur_label = tk.Label(root, text="Énergie déplacement chasseur (ENERGIE_DEPLACEMENT_CHASSEUR):")
        self.energie_deplacement_chasseur_label.grid(row=15, column=0, padx=10, pady=5, sticky="e")
        self.energie_deplacement_chasseur_entry = tk.Entry(root)
        self.energie_deplacement_chasseur_entry.insert(0, ENERGIE_DEPLACEMENT_CHASSEUR)
        self.energie_deplacement_chasseur_entry.grid(row=15, column=1, padx=10, pady=5)

        self.energie_repos_chasseur_label = tk.Label(root, text="Énergie repos chasseur (ENERGIE_REPOS_CHASSEUR):")
        self.energie_repos_chasseur_label.grid(row=16, column=0, padx=10, pady=5, sticky="e")
        self.energie_repos_chasseur_entry = tk.Entry(root)
        self.energie_repos_chasseur_entry.insert(0, ENERGIE_REPOS_CHASSEUR)
        self.energie_repos_chasseur_entry.grid(row=16, column=1, padx=10, pady=5)

        self.energie_gain_chasseur_label = tk.Label(root, text="Énergie gain chasseur (ENERGIE_GAIN_CHASSEUR):")
        self.energie_gain_chasseur_label.grid(row=17, column=0, padx=10, pady=5, sticky="e")
        self.energie_gain_chasseur_entry = tk.Entry(root)
        self.energie_gain_chasseur_entry.insert(0, ENERGIE_GAIN_CHASSEUR)
        self.energie_gain_chasseur_entry.grid(row=17, column=1, padx=10, pady=5)

        # Paramètre du taux de mutation
        self.mutation_rate_label = tk.Label(root, text="Taux de mutation (MUTATION_RATE):")
        self.mutation_rate_label.grid(row=18, column=0, padx=10, pady=5, sticky="e")
        self.mutation_rate_entry = tk.Entry(root)
        self.mutation_rate_entry.insert(0, MUTATION_RATE)
        self.mutation_rate_entry.grid(row=18, column=1, padx=10, pady=5)

        # Vitesse de simulation
        self.vitesse_simu_label = tk.Label(root, text="Vitesse de simulation (VITESSE_SIMU):")
        self.vitesse_simu_label.grid(row=19, column=0, padx=10, pady=5, sticky="e")
        self.vitesse_simu_entry = tk.Entry(root)
        self.vitesse_simu_entry.insert(0, VITESSE_SIMU)
        self.vitesse_simu_entry.grid(row=19, column=1, padx=10, pady=5)

        # Bouton pour lancer la simulation
        self.start_button = tk.Button(root, text="Lancer Simulation", command=self.start_simulation)
        self.start_button.grid(row=20, column=0, columnspan=2, padx=10, pady=20)

    def start_simulation(self):
        global GRID_SIZE, CELL_SIZE, NUM_FOOD, NUM_OBSTACLES, NOMBRE_PROIE, NOMBRE_CHASSEUR
        global VITESSE_PROIE, VITESSE_CHASSEUR, DETECT_PROIE, DETECT_CHASSEUR, VITESSE_SIMU
        global ENERGIE_INITIALE_PROIE, ENERGIE_DEPLACEMENT_PROIE, ENERGIE_GAIN_PROIE
        global ENERGIE_INITIALE_CHASSEUR, ENERGIE_DEPLACEMENT_CHASSEUR, ENERGIE_GAIN_CHASSEUR
        global ENERGIE_REPOS_PROIE, ENERGIE_REPOS_CHASSEUR
        global MUTATION_RATE

        # Récupérer les valeurs des champs
        GRID_SIZE = int(self.grid_size_entry.get())
        CELL_SIZE = int(self.cell_size_entry.get())
        NUM_FOOD = int(self.num_food_entry.get())
        NUM_OBSTACLES = int(self.num_obstacles_entry.get())
        NOMBRE_PROIE = int(self.num_proie_entry.get())
        NOMBRE_CHASSEUR = int(self.num_chasseur_entry.get())
        VITESSE_PROIE = float(self.vitesse_proie_entry.get())
        VITESSE_CHASSEUR = float(self.vitesse_chasseur_entry.get())
        DETECT_PROIE = int(self.detect_proie_entry.get())
        DETECT_CHASSEUR = int(self.detect_chasseur_entry.get())
        VITESSE_SIMU = int(self.vitesse_simu_entry.get())
        ENERGIE_INITIALE_PROIE = int(self.energie_proie_entry.get())
        ENERGIE_DEPLACEMENT_PROIE = int(self.energie_deplacement_proie_entry.get())
        ENERGIE_GAIN_PROIE = int(self.energie_gain_proie_entry.get())
        ENERGIE_INITIALE_CHASSEUR = int(self.energie_initiale_chasseur_entry.get())
        ENERGIE_DEPLACEMENT_CHASSEUR = int(self.energie_deplacement_chasseur_entry.get())
        ENERGIE_GAIN_CHASSEUR = int(self.energie_gain_chasseur_entry.get())
        ENERGIE_REPOS_PROIE = float(self.energie_repos_proie_entry.get())
        ENERGIE_REPOS_CHASSEUR = float(self.energie_repos_chasseur_entry.get())
        # Récupérer la valeur de mutation_rate
        MUTATION_RATE = float(self.mutation_rate_entry.get())

        # Fermer la fenêtre de configuration
        self.root.destroy()

        # Lancer la simulation
        simulation_root = tk.Tk()
        app = SimulationApp(simulation_root)
        simulation_root.mainloop()


class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.env = Environnement()
        self.canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
        self.canvas.pack()

        self.create_agents()
        self.draw_obstacles()  # Dessiner les obstacles une seule fois

        # Compteur de tours
        self.tour_count = 0
        self.tour_label = tk.Label(root, text=f"Nombre de tours: {self.tour_count}")
        self.tour_label.pack()

        # Compteur de reproduction
        self.reproduction_proie_label = tk.Label(root, text=f"Reproduction Proie: {self.env.reproduction_counter_proie}")
        self.reproduction_proie_label.pack()

        self.reproduction_chasseur_label = tk.Label(root, text=f"Reproduction Chasseur: {self.env.reproduction_counter_chasseur}")
        self.reproduction_chasseur_label.pack()

        # Bouton pause/reprendre
        self.is_paused = False
        self.pause_button = tk.Button(root, text="Pause", command=self.toggle_pause)
        self.pause_button.pack()

        self.update_canvas()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Reprendre" if self.is_paused else "Pause")

    def create_agents(self):
        # Spawner les chasseurs et proies en fonction des paramètres globaux
        for _ in range(NOMBRE_CHASSEUR):
            while True:
                chasseur_x = random.randint(0, GRID_SIZE // 4)
                chasseur_y = random.randint(0, GRID_SIZE // 4)
                if self.env.grid[chasseur_x][chasseur_y] == ' ':
                    chasseur = Chasseur(chasseur_x, chasseur_y, self.env)
                    self.env.add_agent(chasseur)
                    break

        for _ in range(NOMBRE_PROIE):
            while True:
                proie_x = random.randint(3 * GRID_SIZE // 4, GRID_SIZE - 1)
                proie_y = random.randint(3 * GRID_SIZE // 4, GRID_SIZE - 1)
                if self.env.grid[proie_x][proie_y] == ' ':
                    proie = Proie(proie_x, proie_y, self.env)
                    self.env.add_agent(proie)
                    break

    def draw_obstacles(self):
        for x, y in self.env.obstacles:
            x1 = x * CELL_SIZE
            y1 = y * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

    def update_canvas(self):
        if not self.is_paused:
            self.env.update()  # Mettre à jour l'environnement
            self.tour_count += 1
            self.tour_label.config(text=f"Nombre de tours: {self.tour_count}")

            # Mettre à jour les compteurs de reproduction
            self.reproduction_proie_label.config(text=f"Reproduction Proie: {self.env.reproduction_counter_proie}")
            self.reproduction_chasseur_label.config(text=f"Reproduction Chasseur: {self.env.reproduction_counter_chasseur}")

            # Effacer les agents
            self.canvas.delete("agents")

            # Redessiner les agents
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    x1 = i * CELL_SIZE
                    y1 = j * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    if isinstance(self.env.grid[i][j], Agent):
                        agent = self.env.grid[i][j]
                        agent_color = "red" if agent.agent_type == 'C' else "blue"
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=agent_color, tags="agents")
                        energie_ratio = agent.energie / self.env.max_energie(agent.agent_type)
                        energie_x1 = x1 + 2
                        energie_y1 = y1 + 2
                        energie_x2 = x1 + (CELL_SIZE - 4) * energie_ratio
                        energie_y2 = y1 + 5
                        self.canvas.create_rectangle(energie_x1, energie_y1, energie_x2, energie_y2, fill="green", tags="agents")
                    elif self.env.grid[i][j] == 'N':
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", tags="agents")

        # Planifier la prochaine mise à jour après un délai
        self.root.after(VITESSE_SIMU, self.update_canvas)



if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigurationApp(root)
    root.mainloop()
