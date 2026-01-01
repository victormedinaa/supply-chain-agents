"""
Real-time Shipment Tracker.

This module monitors active shipments and updates their status based on 
stochastic events in the simulation environment (e.g., weather delays, customs holds).
"""

import random
from typing import List, Optional
from datetime import datetime, timedelta
from backend.src.core.state import Shipment, SupplyChainState, AgentMessage

class ShipmentTracker:
    def check_status(self, shipment: Shipment) -> str:
        """
        Simulates an API call to a carrier (e.g., Maersk, DHL) to get current status.
        """
        # Stochastic logic: random chance of delay based on risk factor
        roll = random.random()
        
        if shipment.status == "Delivered":
            return "Delivered"
            
        if roll < shipment.risk_factor:
            return "Delayed"
        elif roll < 0.05:
            return "Customs"
        else:
            return "In Transit"

    def update_eta(self, shipment: Shipment) -> datetime:
        """
        Recalculates estimated arrival based on current status.
        """
        if shipment.status == "Delayed":
            # Add random delay of 1-3 days
            delay = timedelta(days=random.randint(1, 3))
            return shipment.estimated_arrival + delay
        return shipment.estimated_arrival

    def monitor_active_shipments(self, state: SupplyChainState) -> List[AgentMessage]:
        """
        Batch process to check all active shipments. Returns alerts if delays found.
        """
        alerts = []
        
        for shipment in state.active_shipments:
            previous_status = shipment.status
            new_status = self.check_status(shipment)
            
            if new_status != previous_status:
                shipment.status = new_status
                if new_status == "Delayed":
                    shipment.estimated_arrival = self.update_eta(shipment)
                    alerts.append(AgentMessage(
                        sender="Logistics",
                        receiver="Production", # production needs to know about input delays!
                        content=f"Shipment {shipment.id} is DELAYED. New ETA: {shipment.estimated_arrival}",
                        priority="High"
                    ))
                elif new_status == "Delivered":
                    alerts.append(AgentMessage(
                        sender="Logistics",
                        receiver="Inventory",
                        content=f"Shipment {shipment.id} Arrived. Update stock.",
                        priority="Medium"
                    ))
                    
        return alerts

tracker = ShipmentTracker()
