"""
Simulation Data Generator.

This module populates the SupplyChainState with a massive amount of realistic synthetic data
to ensure the enterprise-grade system has sufficient complexity.
"""

import random
import uuid
from typing import Dict, List
from datetime import datetime
from backend.src.core.state import SupplyChainState, Supplier, Part, InventoryRecord, Shipment, ProductionOrder

class DataGenerator:
    def __init__(self):
        self.regions = ["North America", "Europe", "Asia", "South America"]
        self.categories = ["Electronics", "Chassis", "Powertrain", "Interior"]
        self.suppliers = []
        self.parts = []
        
    def generate_suppliers(self, count: int = 50) -> Dict[str, Supplier]:
        generated = {}
        for i in range(count):
            sid = f"SUP-{i:03d}"
            region = random.choice(self.regions)
            s = Supplier(
                id=sid,
                name=f"Global {random.choice(['Tech', 'Steel', 'Parts', 'Logistics'])} {i}",
                reliability_score=random.uniform(0.7, 0.99),
                location=f"Industrial Zone, {region}",
                contract_terms={"payment": "Net30", "shipping": "FOB"}
            )
            generated[sid] = s
            self.suppliers.append(s)
        return generated

    def generate_parts(self, count: int = 200) -> Dict[str, Part]:
        generated = {}
        if not self.suppliers:
            self.generate_suppliers()
            
        for i in range(count):
            sku = f"SKU-{i:05d}"
            cat = random.choice(self.categories)
            p = Part(
                sku=sku,
                name=f"{cat} Component v{i}",
                category=cat,
                cost=random.uniform(10.0, 5000.0),
                weight_kg=random.uniform(0.1, 50.0),
                supplier_id=random.choice(self.suppliers).id
            )
            generated[sku] = p
            self.parts.append(p)
        return generated

    def generate_initial_state(self) -> SupplyChainState:
        """
        Creates a full populated state object.
        """
        suppliers = self.generate_suppliers(20)
        parts = self.generate_parts(100)
        
        inventory = {}
        for part in parts.values():
            # Initial stock random
            qty = random.randint(0, 500)
            inv = InventoryRecord(
                sku=part.sku,
                warehouse_id="MAIN_DC",
                quantity_on_hand=qty,
                quantity_reserved=0,
                reorder_point=50,
                safety_stock=20
            )
            inventory[f"MAIN_DC_{part.sku}"] = inv
            
        # Create some mock production orders
        schedule = []
        for i in range(5):
            order = ProductionOrder(
                order_id=f"PROD-{i:04d}",
                car_model="BMW X5 M-Competition",
                required_parts={p.sku: 1 for p in random.sample(list(parts.values()), 5)},
                deadline=datetime.now(), # mock
                status="Planned"
            )
            schedule.append(order)
            
        return SupplyChainState(
            current_time=datetime.now(),
            total_budget=10_000_000.0,
            suppliers=suppliers,
            parts_catalog=parts,
            inventory=inventory,
            active_shipments=[],
            production_schedule=schedule
        )

generator = DataGenerator()
