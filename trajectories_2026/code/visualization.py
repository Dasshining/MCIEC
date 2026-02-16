# visualization.py
import matplotlib.pyplot as plt
import osmnx as ox
import imageio
import os

class Visualizer:
    @staticmethod
    def save_frame(G, routes, hotspots, gen, fitness, filepath):
        # Create the plot but DO NOT show it (show=False)
        # close=True ensures the figure is cleared from memory after saving
        node_sizes = [30 if n in hotspots else 0 for n in G.nodes()]
        node_colors = ['red' if n in hotspots else 'none' for n in G.nodes()]
        
        # Plot graph (blocking disabled)
        fig, ax = ox.plot_graph(
            G, 
            node_size=node_sizes, 
            node_color=node_colors, 
            edge_linewidth=0.3, 
            edge_color='#999999', 
            show=False,   # Critical: prevents blocking
            close=False,  # Keep open just long enough to save
            bgcolor='white'
        )
        
        # Plot routes on top
        if routes:
            colors = ['blue', 'green', 'orange', 'purple', 'cyan', 'magenta']
            rc = [colors[i % len(colors)] for i in range(len(routes))]
            ox.plot_graph_routes(G, routes, route_colors=rc, route_linewidths=2, ax=ax)
            
        ax.set_title(f"Generation {gen}\nFitness: {fitness:.4f}", fontsize=12)
        
        # Save and strictly close
        fig.savefig(filepath, dpi=80)
        plt.close(fig)  # Force close to prevent memory leaks or pop-ups

    @staticmethod
    def show_final_plot(G, routes, hotspots):
        """Displays only the final result to the screen."""
        node_sizes = [50 if n in hotspots else 0 for n in G.nodes()]
        node_colors = ['red' if n in hotspots else 'none' for n in G.nodes()]
        
        fig, ax = ox.plot_graph(
            G, node_size=node_sizes, node_color=node_colors, 
            show=False, close=False, bgcolor='white'
        )
        
        if routes:
            colors = ['blue', 'green', 'orange', 'purple', 'cyan', 'magenta']
            rc = [colors[i % len(colors)] for i in range(len(routes))]
            ox.plot_graph_routes(G, routes, route_colors=rc, route_linewidths=2, ax=ax)
        
        plt.show() # This is the ONLY blocking call you want