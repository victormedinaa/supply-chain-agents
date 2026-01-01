"""
Multi-Echelon Inventory Optimization (MEIO) Module.

This module determines the optimal stock levels across the supply chain network.
It uses standard operations research formulas to calculate Safety Stock (SS) 
and Reorder Points (ROP) based on service level targets and demand variability.
"""

from typing import Dict, List, Optional
import math
from scipy.stats import norm
from backend.src.core.state import SupplyChainState, InventoryRecord, Part

class InventoryOptimizer:
    def __init__(self, service_level: float = 0.95):
        """
        Args:
            service_level: Target probability of not stocking out during lead time.
        """
        self.service_level = service_level
        # Z-score for the given service level (e.g., 0.95 -> 1.645)
        self.z_score = norm.ppf(service_level)

    def calculate_safety_stock(self, std_dev_demand: float, avg_lead_time: float, std_dev_lead_time: float, avg_demand: float) -> int:
        """
        Calculates Safety Stock using the standard formula considering uncertainties 
        in both demand and lead time.
        
        Formula: SS = Z * sqrt((L * sigma_D^2) + (D^2 * sigma_L^2))
        """
        term1 = avg_lead_time * (std_dev_demand ** 2)
        term2 = (avg_demand ** 2) * (std_dev_lead_time ** 2)
        combined_uncertainty = math.sqrt(term1 + term2)
        
        return int(math.ceil(self.z_score * combined_uncertainty))

    def calculate_reorder_point(self, avg_demand: float, avg_lead_time: float, safety_stock: int) -> int:
        """
        ROP = (Average Daily Demand * Average Lead Time) + Safety Stock
        """
        lead_time_demand = avg_demand * avg_lead_time
        return int(math.ceil(lead_time_demand + safety_stock))
    
    def optimize_warehouse(self, state: SupplyChainState, sku: str, demand_forecast: float, lead_time_days: int) -> InventoryRecord:
        """
        Updates the inventory parameters for a specific SKU based on the latest forecast.
        
        In a full MEIO system, this would optimize across multiple tiers (Central Warehouse -> Regional DC).
        Here we simplify to a single echelon for the demonstration but keep the mathematical rigor.
        """
        # Derived parameters (mocked from history for this step)
        # In reality, these come from `state.history`
        std_dev_demand = demand_forecast * 0.2  # Assume 20% volatility
        std_dev_lead_time = lead_time_days * 0.1 # Assume 10% volatility in delivery
        avg_demand = demand_forecast / 30 # Daily demand
        
        ss = self.calculate_safety_stock(std_dev_demand, lead_time_days, std_dev_lead_time, avg_demand)
        rop = self.calculate_reorder_point(avg_demand, lead_time_days, ss)
        
        # Get existing record or create new
        existing_record = None
        for key, record in state.inventory.items():
            if record.sku == sku:
                existing_record = record
                break
                
        if existing_record:
            existing_record.reorder_point = rop
            existing_record.safety_stock = ss
            return existing_record
        else:
            # Create new record
            return InventoryRecord(
                sku=sku,
                warehouse_id="MAIN_DC",
                quantity_on_hand=0,
                quantity_reserved=0,
                reorder_point=rop,
                safety_stock=ss
            )

# Singleton
optimizer = InventoryOptimizer()
