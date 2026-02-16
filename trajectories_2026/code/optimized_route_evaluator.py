import networkx as nx
import numpy as np

# --- CONFIGURATION ---
BUS_SPEED_MULTIPLIER = 0.2
OPERATOR_COST_PER_MIN = 1.0 
UNSERVED_PENALTY = 1000   

def precompute_significant_trips(demand_matrix, hotspots):
    """
    OPTIMIZATION HELPER:
    Converts the matrix into a Dictionary of trips organized by Origin.
    Structure: { origin_id: { dest_id: count, dest_id2: count }, ... }
    """
    significant_trips = {node: {} for node in hotspots}
    
    for origin in hotspots:
        if origin >= demand_matrix.shape[0]: continue
        
        destinations = demand_matrix[origin]
        valid_dest_indices = np.where(destinations > 0)[0]
        
        for dest in valid_dest_indices:
            if origin == dest: continue
            count = int(destinations[dest])
            significant_trips[origin][dest] = count
            
    return significant_trips

def calculate_fitness(solution_routes, city_graph, trips_data, hotspots):
    """
    Optimized Fitness Function.
    """
    
    # --- 1. OPERATOR COST ---
    operator_cost = 0
    bus_edges = set()
    
    for route in solution_routes:
        if len(route) < 2: continue
        
        for i in range(len(route) - 1):
            u, v = route[i], route[i+1]
            edge_key = tuple(sorted((u, v)))
            bus_edges.add(edge_key)
            
            if city_graph.has_edge(u, v):
                data = city_graph.get_edge_data(u, v)
                if isinstance(data, dict) and 0 in data: 
                    data = data[0]
                
                w = data.get('weight', data.get('length', 1.0))
                operator_cost += (w * BUS_SPEED_MULTIPLIER) * OPERATOR_COST_PER_MIN
            else:
                operator_cost += 100 # Penalty for teleporting

    # --- 2. BUILD TRANSIT GRAPH ---
    G_transit = city_graph.copy()
    
    for u, v in bus_edges:
        if G_transit.has_edge(u, v):
            try:
                data = G_transit[u][v]
                if isinstance(G_transit, nx.MultiGraph) or isinstance(G_transit, nx.MultiDiGraph):
                    base_weight = data[0].get('weight', 1.0)
                    data[0]['weight'] = base_weight * BUS_SPEED_MULTIPLIER
                else:
                    base_weight = data.get('weight', 1.0)
                    G_transit[u][v]['weight'] = base_weight * BUS_SPEED_MULTIPLIER
            except Exception:
                pass

    # --- 3. USER COST ---
    user_cost = 0
    
    for source in hotspots:
        if source not in trips_data: continue
        source_trips = trips_data[source]
        if not source_trips: continue

        try:
            lengths = nx.single_source_dijkstra_path_length(G_transit, source, weight='weight')
            for dest, count in source_trips.items():
                if dest in lengths:
                    user_cost += count * lengths[dest]
                else:
                    user_cost += count * UNSERVED_PENALTY

        except Exception as e:
            user_cost += sum(source_trips.values()) * UNSERVED_PENALTY

    alpha_user = 1.0
    beta_operator = 10.0
    
    total_fitness = (operator_cost * beta_operator) + (user_cost * alpha_user)
    
    return total_fitness, {
        "op_cost": operator_cost,
        "user_cost": user_cost
    }
