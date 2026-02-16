import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

# --- CONFIGURATION ---
GRID_SIZE = 10       # A 10x10 city (100 stops)
NUM_NODES = GRID_SIZE * GRID_SIZE
HOTSPOTS = [35, 545, 22, 90, 22100]  # Node IDs that will be "Downtown" (High traffic)
SEED = 42            # For reproducibility

random.seed(SEED)
np.random.seed(SEED)

def create_city_graph(n):
    """
    Creates a grid graph representing city streets.
    Returns:
        G: The NetworkX graph
        pos: A dictionary of coordinates for plotting {node_id: (x,y)}
    """
    # 1. Create a 2D Grid Graph
    # Nodes are tuples: (0,0), (0,1), etc.
    G_grid = nx.grid_2d_graph(n, n)
    
    # 2. Convert labels to Integers (0, 1, ..., 99) for easier matrix indexing
    # We keep the old labels as 'pos' attributes for plotting later
    G = nx.convert_node_labels_to_integers(G_grid, first_label=0, ordering='sorted')
    
    # 3. Create a position dictionary for Matplotlib
    # The original grid nodes were (x,y) tuples, but now nodes are ints.
    # We need to calculate (x,y) from the integer ID.
    pos = {}
    for node_id in G.nodes():
        x = node_id % n
        y = node_id // n
        pos[node_id] = (x, y)
        
    # 4. Assign Weights (Travel Time in Minutes) to Edges
    # Base time is 1 min. Randomly add "traffic" (1-4 mins) to edges.
    for u, v in G.edges():
        traffic_delay = random.choice([1, 2, 3, 5]) 
        G[u][v]['weight'] = traffic_delay
        
    return G, pos

def generate_demand_matrix(num_nodes, hotspots):
    """
    Creates a matrix D where D[i][j] is the number of passengers 
    wanting to go from Node i to Node j.
    """
    # 1. Start with low random background noise (0 to 2 people)
    D = np.random.randint(0, 3, size=(num_nodes, num_nodes))
    
    # 2. Zero out diagonal (People don't travel from Node A to Node A)
    np.fill_diagonal(D, 0)
    
    # 3. Add Hotspot Traffic (e.g., everyone going to Work/School)
    # We increase demand TO and FROM the hotspot nodes.
    for spot in hotspots:
        # High demand TO the hotspot
        row_indices = np.random.choice(num_nodes, size=20, replace=False)
        D[row_indices, spot] += np.random.randint(10, 50)
        
        # High demand FROM the hotspot
        col_indices = np.random.choice(num_nodes, size=20, replace=False)
        D[spot, col_indices] += np.random.randint(10, 50)
        
    return D

def visualize_city(G, pos, demand_matrix):
    """
    Visualizes the city grid.
    - Edges are colored by Travel Time (Red = Slow, Gray = Fast)
    - Nodes are sized by total Passenger Activity (Boarding + Alighting)
    """
    # Implementation kept for compatibility, but main visualization uses map_gdl
    pass
