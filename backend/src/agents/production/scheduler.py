"""
Production Scheduler Module.

This component solves the Production Scheduling problem, treating it as a 
Constraint Satisfaction Problem (CSP).
Constraints:
1. Parts availability (from Inventory).
2. Production capacity (lines per day).
3. Delivery deadlines.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from backend.src.core.state import SupplyChainState, ProductionOrder, AgentMessage

class ProductionScheduler:
    def __init__(self, daily_capacity: int = 100):
        self.daily_capacity = daily_capacity
        
    def check_part_availability(self, order: ProductionOrder, state: SupplyChainState) -> Dict[str, bool]:
        """
        Verifies if sufficient stock exists for all BOM items.
        Returns a dict of status per SKU.
        """
        availability = {}
        for sku, required_qty in order.required_parts.items():
            current_stock = state.get_inventory(sku)
            availability[sku] = current_stock >= required_qty
        return availability

    def schedule_production(self, state: SupplyChainState) -> List[AgentMessage]:
        """
        Main routine to optimize the production queue.
        """
        messages = []
        
        # Sort orders by deadline (Earliest Due Date rule - EDD)
        
        pending_orders = [o for o in state.production_schedule if o.status == "Planned"]
        pending_orders.sort(key=lambda x: x.deadline)
        
        current_load = 0
        
        for order in pending_orders:
            # 1. Check Capacity
            if current_load >= self.daily_capacity:
                messages.append(AgentMessage(
                    sender="Production", receiver="Orchestrator",
                    content=f"Capacity Reached. Order {order.order_id} pushed to next slot."
                ))
                continue
                
            # 2. Check Materials
            availability = self.check_part_availability(order, state)
            missing_parts = [sku for sku, ok in availability.items() if not ok]
            
            if not missing_parts:
                # All good - Schedule it
                order.status = "Assembling"
                current_load += 1
                messages.append(AgentMessage(
                    sender="Production", receiver="Logistics",
                    content=f"Production started for {order.order_id}. Dispatch finished goods transport request."
                ))
            else:
                # Missing parts - Halt and Alert Procurement
                order.status = "Halted"
                messages.append(AgentMessage(
                    sender="Production", receiver="Procurement",
                    content=f"HALTED Order {order.order_id}. Missing parts: {missing_parts}",
                    priority="Critical"
                ))
                
        return messages

scheduler = ProductionScheduler()
