"""
Logistics Router Module.

This component calculates optimal shipping routes based on cost, time, and carbon footprint.
It simulates a graph-based routing algorithm (like Dijkstra's) across a global network 
of ports and distribution centers.
"""

from typing import List, Dict, Tuple
import networkx as nx
from backend.src.core.state import Shipment, SupplyChainState

class LogisticsRouter:
    def __init__(self):
        # Create a graph representing the global logistics network
        self.network = nx.Graph()
        self._initialize_network()
        
    def _initialize_network(self):
        """
        Builds a synthetic global supply chain network graph.
        Nodes = Ports/Airports/Warehouses
        Edges = Routes with attributes (cost, time_days, co2_emission)
        """
        # Major hubs
        hubs = ["Shanghai", "Singapore", "Los Angeles", "New York", "Rotterdam", "Hamburg", "Munich (HQ)"]
        self.network.add_nodes_from(hubs)
        
        # Add edges (simplified)
        routes = [
            ("Shanghai", "Singapore", {"cost": 500, "time": 3}),
            ("Singapore", "Rotterdam", {"cost": 1200, "time": 20}), # Suez Canal route
            ("Rotterdam", "Hamburg", {"cost": 200, "time": 2}),
            ("Hamburg", "Munich (HQ)", {"cost": 300, "time": 1}),
            ("Shanghai", "Los Angeles", {"cost": 1000, "time": 14}),
            ("Los Angeles", "New York", {"cost": 800, "time": 5}), # Rail
            ("New York", "Hamburg", {"cost": 900, "time": 10}),
        ]
        self.network.add_edges_from(routes)

    def find_optimal_route(self, origin: str, destination: str, criterion: str = "time") -> Dict[str, any]:
        """
        Finds the best path using Dijkstra's algorithm.
        
        Args:
            criterion: 'time', 'cost', or 'balanced'
        """
        if origin not in self.network.nodes or destination not in self.network.nodes:
            raise ValueError(f"Unknown location in route: {origin} -> {destination}")
            
        try:
            path = nx.shortest_path(self.network, source=origin, target=destination, weight=criterion)
            
            # Calculate total metrics for the path
            total_cost = 0
            total_time = 0
            
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                edge_data = self.network[u][v]
                total_cost += edge_data.get("cost", 0)
                total_time += edge_data.get("time", 0)
                
            return {
                "path": path,
                "estimated_transit_time": total_time,
                "estimated_cost": total_cost
            }
        except nx.NetworkXNoPath:
            return None

# Singleton
router = LogisticsRouter()
