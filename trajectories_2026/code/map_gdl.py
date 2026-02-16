import osmnx as ox
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
from city_environment import visualize_city, generate_demand_matrix
from optimized_route_evaluator import precompute_significant_trips, calculate_fitness

def create_real_city_graph(hotspot_coords=None):
    """
    Creates a real city graph from OSM data and identifies hotspot nodes from coordinates.
    """
    print("Downloading map data...")
    G_osm = ox.graph_from_place('Guadalajara, Mexico', network_type='drive')

    G = nx.convert_node_labels_to_integers(G_osm, first_label=0, ordering='default', label_attribute='original_osm_id')
    mapping = {data['original_osm_id']: node for node, data in G.nodes(data=True)}

    pos = {}
    for node, data in G.nodes(data=True):
        pos[node] = (data['x'], data['y'])
        
    for u, v, key, data in G.edges(keys=True, data=True):
        length = data.get('length', 100)
        travel_time = length / 400 
        G[u][v][key]['weight'] = travel_time * random.uniform(1.0, 1.5)

    hotspot_nodes = []
    if hotspot_coords:
        original_hotspot_nodes = ox.nearest_nodes(G_osm, [coord[1] for coord in hotspot_coords], [coord[0] for coord in hotspot_coords])
        hotspot_nodes = [mapping[osm_id] for osm_id in original_hotspot_nodes]
        print(f"Identified Hotspot OSM IDs: {original_hotspot_nodes}")
        print(f"Converted to Integer IDs: {hotspot_nodes}")

    return G, pos, hotspot_nodes

def visualize_city_gdl(G, pos, demand_matrix, hotspots=None):
    """
    Visualizes the city grid.
    """
    if hotspots is None:
        hotspots = []

    node_sizes = [50 if node in hotspots else 0 for node in G.nodes()]
    node_colors = ['red' if node in hotspots else 'w' for node in G.nodes()]

    if not any(node_sizes):
        print("Warning: No hotspots to display. Showing only the street network.")
    else:
        print(f"Highlighting {len(hotspots)} hotspots.")

    edge_weights = [d['weight'] for _, _, d in G.edges(data=True)]

    fig, ax = ox.plot_graph(
        G,
        node_size=node_sizes,
        node_color='w',
        node_edgecolor='r',
        node_zorder=2,
        edge_linewidth=0.5,
        edge_color='k',
        bgcolor='#DDDDDD',
        show=False,
        close=False
    )
    
    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=min(edge_weights), vmax=max(edge_weights)))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', shrink=0.7)
    cbar.set_label('Street Travel Time (Minutes)')

    fig.savefig('city_visualization.png', dpi=300, bbox_inches='tight', pad_inches=0)
    print("City visualization saved to city_visualization.png")
    plt.close(fig)

def plot_routes_on_gdl_map(G, all_time_best_routes, current_best_routes, hotspots, title, filepath):
    """
    Plots the base city map and overlays the bus routes.
    """
    node_sizes = [50 if node in hotspots else 0 for node in G.nodes()]

    fig, ax = ox.plot_graph(
        G,
        node_size=node_sizes,
        node_color='r',
        node_zorder=2,
        edge_linewidth=0.5,
        edge_color='k',
        bgcolor='#DDDDDD',
        show=False,
        close=True
    )

    if all_time_best_routes:
        ox.plot_graph_routes(G, all_time_best_routes, route_colors='lightgray', 
                             route_linewidths=4, route_alpha=0.5, ax=ax, orig_dest_size=0)

    if current_best_routes:
        colors = ['#FF3333', '#33FF33', '#3333FF', '#FFFF33', '#FF33FF', '#33FFFF',
                  '#FF8333', '#33FF83', '#8333FF', '#FF3383', '#3383FF', '#E67E22',
                  '#1ABC9C', '#9B59B6', '#F1C40F', '#E74C3C', '#3498DB', '#2ECC71']
        
        route_colors_list = [colors[idx % len(colors)] for idx in range(len(current_best_routes))]
        
        ox.plot_graph_routes(G, current_best_routes, route_colors=route_colors_list, 
                             route_linewidths=2, route_alpha=1, ax=ax, orig_dest_size=0)

    ax.set_title(title)
    fig.savefig(filepath, dpi=100, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
