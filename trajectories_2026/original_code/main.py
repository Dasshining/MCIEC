import random
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox

# Store graphics
import os
import imageio

# Import graph modules
from city_environment import visualize_city, generate_demand_matrix
from map_gdl import create_real_city_graph, visualize_city_gdl, plot_routes_on_gdl_map
from optimized_route_evaluator import precompute_significant_trips, calculate_fitness
# Import genetic algorithm
from genetic_algoritm import genetic_algorithm, ProblemConfig

# --- GLOBAL CONFIGURATION ---
NUM_ROUTES = 10          # How many bus lines to create (Rutas troncales 21)
MAX_ROUTE_LENGTH = 300   # Max stops per line (El grafo esta compuesto de 
                         # 22,282 nodos,  lo que indica un tamno de aprox 
                         # 150 x 150, 300 deberia ser suficiente para una vuelta completa a la ciudad)
PAUSE_TIME = 0.1         # Visualization speed

# Initialize City Data Globally (so functions can access them)
print("Initializing City...")
hotspot_locations = [
    (20.6775, -103.3460),  # Centro historico
    (20.6757, -103.3397),  # San Juan de Dios
    (20.6622, -103.3186),  # Zona de Medrano
    (20.7088, -103.4119),  # Puerta de hierro
    (20.6746, -103.3547),  # Estacion Juarez
    (20.6395, -103.3119),  # Tlaquepaque Centro
    (20.7311, -103.3880),  # Zapopan Centro
    (20.6549, -103.3254)   # CUCEI
]
G, POS, HOTSPOTS = create_real_city_graph(hotspot_coords=hotspot_locations)
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
print(f"City created with {num_nodes} stops and {num_edges} streets.")
DEMAND = generate_demand_matrix(num_nodes, HOTSPOTS)
print(f"Demand Matrix Generated. Total trips in simulation: {np.sum(DEMAND)}")
SIGNIFICANT_TRIPS = precompute_significant_trips(DEMAND, HOTSPOTS)

# --- 1. DOMAIN SPECIFIC GENOME CREATION ---

def create_transit_genome(range_val, len_val):
    """
    Creates a random valid set of bus routes.
    len_val = number of routes.
    """
    genome = []
    for _ in range(len_val):
        # 1. Start at a random node
        current_node = random.choice(list(G.nodes()))
        route = [current_node]
        
        # 2. Random walk to build the route
        route_len = random.randint(5, MAX_ROUTE_LENGTH)
        for _ in range(route_len):
            neighbors = list(G.neighbors(current_node))
            if not neighbors: break
            next_node = random.choice(neighbors)
            route.append(next_node)
            current_node = next_node
        
        genome.append(route)
    return genome

# --- 2. CUSTOM OPERATORS (CROSSOVER & MUTATION) ---

def crossover_transit(genome1, genome2, config):
    """
    Swaps whole routes between two solutions.
    """
    if random.random() < config.crossover_probability:
        # Swap point based on number of routes
        pt = random.randint(1, len(genome1) - 1)
        # Child 1 gets first half of Parent A, second half of Parent B
        child1 = genome1[:pt] + genome2[pt:]
        child2 = genome2[:pt] + genome1[pt:]
        return child1, child2
    return genome1, genome2

def mutation_transit(genome, config):
    """
    Modifies routes to explore new paths.
    """
    mutated = [list(route) for route in genome] # Deep copy
    
    for i in range(len(mutated)):
        if random.random() < config.mutation_probability:
            mutation_type = random.choice(['extend', 'trim', 'regenerate'])
            route = mutated[i]
            
            if mutation_type == 'extend' and len(route) < MAX_ROUTE_LENGTH:
                # Add a neighbor to the end
                last_node = route[-1]
                neighbors = list(G.neighbors(last_node))
                if neighbors:
                    route.append(random.choice(neighbors))
            
            elif mutation_type == 'trim' and len(route) > 2:
                # Remove the last stop
                route.pop()
                
            elif mutation_type == 'regenerate':
                # Create a brand new random route from a random spot
                start = random.choice(list(G.nodes()))
                new_route = [start]
                curr = start
                for _ in range(random.randint(5, MAX_ROUTE_LENGTH)):
                    nbs = list(G.neighbors(curr))
                    if not nbs: break
                    nxt = random.choice(nbs)
                    new_route.append(nxt)
                    curr = nxt
                mutated[i] = new_route
                
    return mutated

# --- 3. FITNESS FUNCTION WRAPPER ---

def fitness_wrapper(genome):
    """
    Wraps the complex evaluator into the simple format expected by your GA class.
    """
    # The evaluator returns (cost, details_dict). We only need cost.
    cost, _ = calculate_fitness(genome, G, SIGNIFICANT_TRIPS, HOTSPOTS)
    
    # Your GA maximizes fitness if tendency='max'.
    # But evaluator returns Cost (Lower is better).
    # We invert it so Higher Fitness = Lower Cost.
    if cost == 0: return float('inf')
    return 1000000000 / cost 

# --- 4. VISUALIZATION & STOP CONDITION ---

def create_visual_stop_func(config, tendency='max'):
    """
    A 'Trojan Horse' stop function that updates the plot every generation.
    """
    def stop_condition(generation, population):
        # Standard limit check
        if generation >= config.max_generations:
            print("Max generations reached.")
            return False
        
        # --- VISUALIZATION LOGIC ---
        # 1. Get current generation's best individual
        best_ind = max(population.individuals, key=lambda ind: ind.fitness)

        # 2. Update the all-time best individual if the current one is better
        if config.best_individual is None or best_ind.fitness > config.best_individual.fitness:
            config.best_individual  = best_ind
        
        # 2. Only redraw every N generations to save speed (optional)
        if generation % 1 == 0: 
            title = (f"Gen {generation} | Current Fitness: {best_ind.fitness:.2f}\n"
                     f"Best Overall Fitness: {config.best_individual.fitness:.2f}")
            
            # Save frame for GIF (Optional)
            filepath = f"frames_gdl/gen_{generation:03d}.png"
            
            # Use the new dedicated plotting function
            plot_routes_on_gdl_map(
                G,
                all_time_best_routes=config.best_individual.genome if config.best_individual else None,
                current_best_routes=best_ind.genome,
                hotspots=HOTSPOTS,
                title=title,
                filepath=filepath
            )
        
        # Print progress to console
        print(f"Gen {generation}: Current Best={best_ind.fitness:.4f}, Overall Best={config.best_individual.fitness:.4f}")
        
        return True # Continue evolving
    
    return stop_condition

# --- 5. MAIN EXECUTION ---

def run_transit_ga():
    # Create a directory to save frames for the GIF
    frames_dir = "frames_gdl"
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)

    config = ProblemConfig(
        function_name="Transit_Network_Optimization",
        gene_range=(0, num_nodes-1),     # Node IDs
        gene_length=NUM_ROUTES, # Number of routes
        population_size=20,     # Keep small for speed in Python
        max_generations=50,
        mutation_probability=0.4,
        crossover_probability=0.7,
        generation_improvement_count=0,
        pass_method='list'
    )

    print("Starting Optimization...")
    
    best_genome = genetic_algorithm(
        config=config,
        create_genome=create_transit_genome,
        fitness_func=fitness_wrapper,
        stop_condition_func=create_visual_stop_func(config),
        crossover_func=crossover_transit,
        mutation_func=mutation_transit,
        selection_method='tournament', # Tournament is usually better for this than roulette
        tendency='max'
    )
    
    print("Optimization Complete.")
    print("Best Genome: {best_genome}")

    # --- GIF CREATION ---
    print("Creating GIF from saved frames...")
    images = []
    sorted_files = sorted(os.listdir(frames_dir), key=lambda x: int(x.split('_')[1].split('.')[0]))
    for filename in sorted_files:
        if filename.endswith('.png'):
            images.append(imageio.imread(os.path.join(frames_dir, filename)))
    imageio.mimsave('transit_optimization.gif', images, fps=5)
    print("GIF saved as transit_optimization.gif")

if __name__ == "__main__":
    run_transit_ga()