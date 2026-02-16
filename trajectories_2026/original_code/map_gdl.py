import osmnx as ox
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
from city_environment import visualize_city, generate_demand_matrix
# from route_evaluator import calculate_fitness
from optimized_route_evaluator import precompute_significant_trips, calculate_fitness

def create_real_city_graph(hotspot_coords=None):
    """
    Creates a real city graph from OSM data and identifies hotspot nodes from coordinates.

    Args:
        hotspot_coords (list of tuples): A list of (latitude, longitude) tuples for hotspots.

    Returns:
        tuple: A tuple containing (G, pos, hotspot_nodes)
               - G: The networkx graph with integer node labels.
               - pos: A dictionary of node positions.
               - hotspot_nodes: A list of integer node IDs corresponding to the nearest nodes to hotspot_coords.
    """
    # 1. Download the map (Example: A neighborhood in Guadalajara)
    # You can use a bounding box or a name
    print("Downloading map data...")
    G_osm = ox.graph_from_place('Guadalajara, Mexico', network_type='drive')

    # 2. Relabel nodes to Integers (0, 1, 2...) and create a mapping
    # from original OSM IDs to new integer IDs.
    # We store the old label in a node attribute and then build the mapping.
    G = nx.convert_node_labels_to_integers(G_osm, first_label=0, ordering='default', label_attribute='original_osm_id')
    
    # Build the mapping from original OSM ID to new integer ID
    mapping = {data['original_osm_id']: node for node, data in G.nodes(data=True)}

    
    # 4. Extract Positions (OSMnx stores them as 'x' and 'y' attributes)
    pos = {}
    for node, data in G.nodes(data=True):
        pos[node] = (data['x'], data['y'])
        
    # 5. Process Edges to set Weights
    # OSM data often includes 'length' (meters). We want 'time'.
    for u, v, key, data in G.edges(keys=True, data=True):
        length = data.get('length', 100) # Default 100m if missing
        
        # Heuristic: Assume "primary" roads are faster but have more traffic?
        # Or just use length as the base cost.
        # Speed estimate: 30 km/h = 500 m/min. Let's use 400 to simulate some traffic.
        travel_time = length / 400 
        
        # Add traffic noise
        G[u][v][key]['weight'] = travel_time * random.uniform(1.0, 1.5)

    # 6. Find integer node IDs for hotspots
    hotspot_nodes = []
    if hotspot_coords:
        # Use the original graph (G_osm) to find the nearest nodes by lat/lon
        original_hotspot_nodes = ox.nearest_nodes(G_osm, [coord[1] for coord in hotspot_coords], [coord[0] for coord in hotspot_coords])
        # Use the mapping to convert OSM IDs to integer IDs
        hotspot_nodes = [mapping[osm_id] for osm_id in original_hotspot_nodes]
        print(f"Identified Hotspot OSM IDs: {original_hotspot_nodes}")
        print(f"Converted to Integer IDs: {hotspot_nodes}")

    return G, pos, hotspot_nodes

def visualize_city_gdl(G, pos, demand_matrix, hotspots=None):
    """
    Visualizes the city grid.
    - Edges are colored by Travel Time (Red = Slow, Gray = Fast)
    - Only hotspot nodes are shown.
    This version is optimized for large graphs from osmnx.
    """
    if hotspots is None:
        hotspots = []

    # Set node sizes: 50 for hotspots, 0 for all other nodes to hide them.
    node_sizes = [50 if node in hotspots else 0 for node in G.nodes()]
    # Set node colors: red for hotspots, white for others (though they won't be visible).
    node_colors = ['red' if node in hotspots else 'w' for node in G.nodes()]

    if not any(node_sizes):
        print("Warning: No hotspots to display. Showing only the street network.")
    else:
        print(f"Highlighting {len(hotspots)} hotspots.")

    edge_weights = [d['weight'] for _, _, d in G.edges(data=True)]

    # Use osmnx to plot the graph which handles large geo-data better
    fig, ax = ox.plot_graph(
        G,
        node_size=node_sizes,
        node_color='w',
        node_edgecolor='r',
        node_zorder=2,
        edge_linewidth=0.5,
        edge_color='k',
        bgcolor='#DDDDDD',
        show=False,  # Do not show or close the plot until we are done modifying it
        close=False
    )
    
    # Add a colorbar for the edge weights (travel time)
    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=min(edge_weights), vmax=max(edge_weights)))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', shrink=0.7)
    cbar.set_label('Street Travel Time (Minutes)')

    # Save the figure
    fig.savefig('city_visualization.png', dpi=300, bbox_inches='tight', pad_inches=0)
    print("City visualization saved to city_visualization.png")

def plot_routes_on_gdl_map(G, all_time_best_routes, current_best_routes, hotspots, title, filepath):
    """
    Plots the base city map and overlays the bus routes.

    Args:
        G (nx.MultiDiGraph): The city graph from osmnx.
        all_time_best_routes (list): List of routes for the best-ever individual.
        current_best_routes (list): List of routes for the current generation's best.
        hotspots (list): List of hotspot node IDs.
        title (str): The title for the plot.
        filepath (str): The path to save the resulting image.
    """
    # Make non-hotspot nodes invisible
    node_sizes = [50 if node in hotspots else 0 for node in G.nodes()]

    # Use osmnx to plot the base graph
    fig, ax = ox.plot_graph(
        G,
        node_size=node_sizes,
        node_color='r',
        node_zorder=2,
        edge_linewidth=0.5,
        edge_color='k',
        bgcolor='#DDDDDD',
        show=False,
        close=True  # Close the plot to free memory
    )

    # Draw All-Time Best Routes (in gray)
    if all_time_best_routes:
        ox.plot_graph_routes(G, all_time_best_routes, route_colors='lightgray', 
                             route_linewidths=4, route_alpha=0.5, ax=ax, orig_dest_size=0)

    # Draw Current Best Bus Routes (in color) on top
    if current_best_routes:
        # Use a more vibrant and larger color palette
        colors = ['#FF3333', '#33FF33', '#3333FF', '#FFFF33', '#FF33FF', '#33FFFF',
                  '#FF8333', '#33FF83', '#8333FF', '#FF3383', '#3383FF', '#E67E22',
                  '#1ABC9C', '#9B59B6', '#F1C40F', '#E74C3C', '#3498DB', '#2ECC71']
        
        # Use ox.plot_graph_routes for efficiency
        route_colors_list = [colors[idx % len(colors)] for idx in range(len(current_best_routes))]
        
        ox.plot_graph_routes(G, current_best_routes, route_colors=route_colors_list, 
                             route_linewidths=2, route_alpha=1, ax=ax, orig_dest_size=0)

    ax.set_title(title)
    
    # Save the figure
    fig.savefig(filepath, dpi=100, bbox_inches='tight', pad_inches=0)
    plt.close(fig) # Ensure the figure is closed


if __name__ == "__main__":
    # 1. Setup City
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
    G, pos, hotspots = create_real_city_graph(hotspot_coords=hotspot_locations)
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    print(f"City created with {num_nodes} stops and {num_edges} streets.")
    
    # 2. Generate Demand
    demand = generate_demand_matrix(num_nodes, hotspots)
    print(f"Demand Matrix Generated. Total trips in simulation: {np.sum(demand)}")
    
    # 3. Inspect a specific connection (e.g., Node 0 to Node 1)
    if num_edges > 0:
        # Instead of hardcoding an edge, pick a random one that exists.
        u, v, key = random.choice(list(G.edges(keys=True)))
        print(f"Street connecting {u}->{v} takes {G[u][v][key]['weight']:.2f} minutes.")
        # Make sure the hotspot index is valid
        if hotspots and hotspots[0] < num_nodes:
            print(f"Passengers waiting at {u} to go to {hotspots[0]}: {demand[u][hotspots[0]]}")

    # 4. Show the Map
    visualize_city_gdl(G, pos, demand, hotspots=hotspots)

    # 2. Create a Dummy Solution (Two horizontal lines, one vertical)
    #    Route 1: Nodes 0 to 9 (Bottom row)
    #    Route 2: Nodes 0, 10, 20... 90 (Left column)
    test_solution = [
        list(range(0, 10)),           # [0, 1, 2, ... 9]
        list(range(0, 100, 10))       # [0, 10, 20, ... 90]
    ]
    
    print("Evaluating Test Solution...")
    precopute_trips = precompute_significant_trips(demand, hotspots)
    score, details = calculate_fitness(test_solution, G, precopute_trips, hotspots)

    with open(f"GA_output/test_gdl_map.txt", "w") as text_file:
        text = str(G)
        text_file.write(text)
        text_file.write("\n")
        
        text = str(precopute_trips)
        text_file.write(text)
        text_file.write("\n")
        
        text = str(details)
        text_file.write(text)
        text_file.write("\n")

    
    print(f"\n--- RESULTS ---")
    print(f"Fitness Score: {score:.2f} (Lower is better)")
    print(f"Operator Cost: {details['op_cost']:.2f} (Bus driving minutes)")
    print(f"User Cost:     {details['user_cost']:.2f} (Total passenger waiting minutes)")