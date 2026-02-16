# config.py
from dataclasses import dataclass

@dataclass
class Config:
    # --- City Parameters ---
    PLACE_NAME = "Guadalajara, Mexico"
    HOTSPOT_COORDS = [
        (20.6775, -103.3460),  # Centro Historico
        (20.6757, -103.3397),  # San Juan de Dios
        (20.6622, -103.3186),  # Medrano
        (20.7088, -103.4119),  # Puerta de Hierro
        (20.6746, -103.3547),  # Juarez
        (20.6395, -103.3119),  # Tlaquepaque
        (20.7311, -103.3880),  # Zapopan
        (20.6549, -103.3254)   # CUCEI
    ]
    
    # --- Simulation Constants ---
    BUS_SPEED_MULTIPLIER = 0.2
    OPERATOR_COST_PER_MIN = 1.0
    UNSERVED_PENALTY = 1000
    ALPHA_USER = 1.0
    BETA_OPERATOR = 10.0
    
    # --- GA Parameters ---
    NUM_ROUTES = 10
    MAX_ROUTE_LENGTH = 150 # Reduced slightly for performance
    POPULATION_SIZE = 20
    MAX_GENERATIONS = 50
    MUTATION_RATE = 0.4
    CROSSOVER_RATE = 0.7
    
    # --- System ---
    CACHE_FILE = "gdl_graph.pkl"
    FRAMES_DIR = "frames_gdl"