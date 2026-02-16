# graph_loader.py
import os
import pickle
import random
import networkx as nx
import osmnx as ox
import numpy as np
from config import Config

class GraphManager:
    def __init__(self):
        self.G = None
        self.pos = {}
        self.hotspots = []
        self.demand_matrix = None
        self.trips_data = None

    def load_or_create_city(self):
        """Loads graph from cache if available, otherwise downloads from OSM."""
        if os.path.exists(Config.CACHE_FILE):
            print(f"Loading cached graph from {Config.CACHE_FILE}...")
            with open(Config.CACHE_FILE, "rb") as f:
                data = pickle.load(f)
                self.G, self.pos, self.hotspots = data['G'], data['pos'], data['hotspots']
        else:
            print(f"Downloading map data for {Config.PLACE_NAME}...")
            G_osm = ox.graph_from_place(Config.PLACE_NAME, network_type='drive')
            
            # Convert to standard integers for easier array indexing
            self.G = nx.convert_node_labels_to_integers(
                G_osm, first_label=0, ordering='default', label_attribute='original_id'
            )
            
            # Extract positions
            self.pos = {n: (d['x'], d['y']) for n, d in self.G.nodes(data=True)}
            
            # Add Weights (Time)
            for u, v, k, d in self.G.edges(keys=True, data=True):
                length = d.get('length', 100)
                # 400m/min approx 24km/h base speed
                base_time = length / 400.0
                # Add traffic noise directly here
                self.G[u][v][k]['weight'] = base_time * random.uniform(1.0, 1.5)

            # Map coordinates to nearest nodes for Hotspots
            if Config.HOTSPOT_COORDS:
                lats = [c[0] for c in Config.HOTSPOT_COORDS]
                lons = [c[1] for c in Config.HOTSPOT_COORDS]
                # Nearest nodes in the original graph
                orig_nodes = ox.nearest_nodes(G_osm, lons, lats)
                # Map to new integer IDs
                mapping = {d['original_id']: n for n, d in self.G.nodes(data=True)}
                self.hotspots = [mapping.get(oid, 0) for oid in orig_nodes]

            # Cache the result
            with open(Config.CACHE_FILE, "wb") as f:
                pickle.dump({'G': self.G, 'pos': self.pos, 'hotspots': self.hotspots}, f)
        
        # Generate Demand
        self._generate_demand()
        return self.G

    def _generate_demand(self):
        """Generates synthetic demand focused on hotspots."""
        num_nodes = self.G.number_of_nodes()
        # Sparse matrix approach is better for memory, but dense is fine for this scale
        self.demand_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        
        # Background noise (disabled for speed, or kept low)
        # self.demand_matrix += np.random.randint(0, 2, size=(num_nodes, num_nodes))
        
        for spot in self.hotspots:
            # Random traffic TO and FROM hotspots
            targets = np.random.choice(num_nodes, size=30, replace=False)
            self.demand_matrix[targets, spot] += np.random.randint(10, 50) # To Hotspot
            self.demand_matrix[spot, targets] += np.random.randint(10, 50) # From Hotspot
            
        np.fill_diagonal(self.demand_matrix, 0)
        self._precompute_trips()

    def _precompute_trips(self):
        """Optimizes fitness calculation by converting matrix to dict."""
        self.trips_data = {node: {} for node in self.hotspots}
        for origin in self.hotspots:
            destinations = np.where(self.demand_matrix[origin] > 0)[0]
            for dest in destinations:
                self.trips_data[origin][dest] = int(self.demand_matrix[origin][dest])