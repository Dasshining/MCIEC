# ga_engine.py
import random
from copy import deepcopy
from config import Config

class GeneticAlgorithm:
    def __init__(self, graph_manager, fitness_evaluator):
        self.gm = graph_manager
        self.evaluator = fitness_evaluator
        self.population = []
        self.best_individual = None
        self.best_fitness = -1

    def create_initial_population(self):
        self.population = []
        nodes = list(self.gm.G.nodes())
        
        for _ in range(Config.POPULATION_SIZE):
            genome = []
            for _ in range(Config.NUM_ROUTES):
                # Random Walk Route Creation
                curr = random.choice(nodes)
                route = [curr]
                for _ in range(random.randint(5, Config.MAX_ROUTE_LENGTH)):
                    neighbors = list(self.gm.G.neighbors(curr))
                    if not neighbors: break
                    curr = random.choice(neighbors)
                    route.append(curr)
                genome.append(route)
            
            # Evaluate immediately
            fit, _ = self.evaluator.evaluate(genome, self.gm.G, self.gm.trips_data, self.gm.hotspots)
            self.population.append({'genome': genome, 'fitness': fit})

    def select_parents(self):
        # Tournament Selection
        selected = []
        for _ in range(Config.POPULATION_SIZE):
            candidates = random.sample(self.population, k=3)
            winner = max(candidates, key=lambda x: x['fitness'])
            selected.append(winner)
        return selected

    def crossover(self, p1, p2):
        if random.random() > Config.CROSSOVER_RATE:
            return deepcopy(p1['genome']), deepcopy(p2['genome'])
        
        # Swap Routes
        cut = random.randint(1, len(p1['genome']) - 1)
        c1 = deepcopy(p1['genome'][:cut] + p2['genome'][cut:])
        c2 = deepcopy(p2['genome'][:cut] + p1['genome'][cut:])
        return c1, c2

    def mutate(self, genome):
        for i in range(len(genome)):
            if random.random() < Config.MUTATION_RATE:
                action = random.choice(['grow', 'trim', 'replace'])
                route = genome[i]
                
                if action == 'grow' and len(route) < Config.MAX_ROUTE_LENGTH:
                    neighbors = list(self.gm.G.neighbors(route[-1]))
                    if neighbors: route.append(random.choice(neighbors))
                
                elif action == 'trim' and len(route) > 2:
                    route.pop()
                
                elif action == 'replace':
                    # Respawn short random route
                    start = random.choice(list(self.gm.G.nodes()))
                    new_r = [start]
                    curr = start
                    for _ in range(10):
                        nbs = list(self.gm.G.neighbors(curr))
                        if not nbs: break
                        curr = random.choice(nbs)
                        new_r.append(curr)
                    genome[i] = new_r
        return genome

    def evolve(self):
        parents = self.select_parents()
        next_gen = []
        
        for i in range(0, len(parents), 2):
            p1, p2 = parents[i], parents[(i+1)%len(parents)]
            c1_g, c2_g = self.crossover(p1, p2)
            
            c1_g = self.mutate(c1_g)
            c2_g = self.mutate(c2_g)
            
            next_gen.append({'genome': c1_g, 'fitness': 0})
            next_gen.append({'genome': c2_g, 'fitness': 0})
            
        # Bulk Evaluation
        for ind in next_gen:
            ind['fitness'], _ = self.evaluator.evaluate(ind['genome'], self.gm.G, self.gm.trips_data, self.gm.hotspots)
            
            if ind['fitness'] > self.best_fitness:
                self.best_fitness = ind['fitness']
                self.best_individual = ind

        self.population = next_gen[:Config.POPULATION_SIZE]