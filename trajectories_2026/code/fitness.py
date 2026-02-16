# fitness.py
import networkx as nx
from config import Config

class FitnessEvaluator:
    @staticmethod
    def evaluate(genome, G, trips_data, hotspots):
        """
        Calculates the fitness of a genome (list of routes).
        Returns: Tuple (Fitness Score, Details Dictionary)
        """
        # 1. Operator Cost: Based on total length of bus routes
        operator_cost = 0
        bus_edges = set()
        
        for route in genome:
            if len(route) < 2: continue
            for i in range(len(route) - 1):
                u, v = route[i], route[i+1]
                edge_key = tuple(sorted((u, v)))
                
                # Count cost only if new segment (or count every time if paying per bus)
                # Here we assume cost per unique segment coverage
                if edge_key not in bus_edges:
                    if G.has_edge(u, v):
                        # Handle MultiDiGraph data access safely
                        data = G.get_edge_data(u, v)
                        w = data[0].get('weight', 1.0) if 0 in data else 1.0
                        operator_cost += (w * Config.BUS_SPEED_MULTIPLIER) * Config.OPERATOR_COST_PER_MIN
                    else:
                        operator_cost += 50 # Penalty for invalid jump
                    bus_edges.add(edge_key)

        # 2. Build Transit Sub-Graph (Virtual Graph)
        # Faster than copying the whole graph: use G_transit as a view or lightweight copy
        # For simplicity/correctness in Dijkstra, we create a subgraph view or graph
        G_transit = nx.Graph() 
        # Add only the bus edges with improved speed
        for u, v in bus_edges:
            w = None
            if G.has_edge(u, v):
                data = G.get_edge_data(u, v)
                w = data[0].get('weight', 1.0) if 0 in data else 1.0
            elif G.has_edge(v, u):
                data = G.get_edge_data(v, u)
                w = data[0].get('weight', 1.0) if 0 in data else 1.0
            
            if w is not None:
                G_transit.add_edge(u, v, weight=w * Config.BUS_SPEED_MULTIPLIER)

        # 3. User Cost: Dijkstra from hotspots
        user_cost = 0
        for source in hotspots:
            if source not in trips_data: continue
            targets = trips_data[source]
            if not targets: continue

            # If source not in transit network, all its trips fail
            if source not in G_transit:
                user_cost += sum(targets.values()) * Config.UNSERVED_PENALTY
                continue
            
            try:
                # Calculate paths from source to all reachable nodes
                paths = nx.single_source_dijkstra_path_length(G_transit, source, weight='weight')
                
                for dest, count in targets.items():
                    if dest in paths:
                        user_cost += count * paths[dest]
                    else:
                        user_cost += count * Config.UNSERVED_PENALTY
            except:
                user_cost += sum(targets.values()) * Config.UNSERVED_PENALTY

        # 4. Total Cost Calculation
        total_cost = (operator_cost * Config.BETA_OPERATOR) + (user_cost * Config.ALPHA_USER)
        
        # Invert for Fitness (Higher is better)
        fitness = 1e9 / total_cost if total_cost > 0 else 0
        
        return fitness, {"op": operator_cost, "user": user_cost}