"""
Root Cause Analyzer.

Uses a probabilistic causal graph to determine the likely source of a defect.
Factors considered: Supplier Reliability, Transport/Handling Shock, Storage Conditions.
"""

from typing import Dict
import networkx as nx
from backend.src.core.state import SupplyChainState

class RootCauseAnalyzer:
    def __init__(self):
        self.causal_graph = nx.DiGraph()
        self._build_graph()
        
    def _build_graph(self):
        """
        Nodes: Potential Causes
        Edges: Causal influence probability
        """
        self.causal_graph.add_edge("Supplier Quality", "Part Defect", weight=0.6)
        self.causal_graph.add_edge("Transport Shock", "Part Defect", weight=0.3)
        self.causal_graph.add_edge("Warehouse Temp", "Part Defect", weight=0.1)

    def diagnose_defect(self, supplier_id: str, transport_route: str) -> str:
        """
        Returns the most likely root cause for a defect.
        """
        # Simplistic inference engine
        # In a real PhD project, this would use Do-Calculus or a Bayesian Network library (pgmpy)
        
        scores = {
            "Supplier Quality": 0.5, # Base probability
            "Transport Shock": 0.2,
            "Warehouse Temp": 0.1
        }
        
        # Adjust based on context
        if "Overseas" in transport_route:
            scores["Transport Shock"] += 0.3
            
        # Return max
        return max(scores, key=scores.get)

rca = RootCauseAnalyzer()
