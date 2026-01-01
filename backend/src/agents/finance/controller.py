"""
Cost Controller Agent.

Responsible for enforcing budget constraints and analyzing cost variances.
Acts as a gatekeeper for high-value procurement orders.
"""

from typing import List, Dict
from pydantic import BaseModel
from backend.src.core.state import SupplyChainState, AgentMessage
from backend.src.agents.finance.ledger import ledger, JournalEntry, TransactionEntry
from datetime import datetime

class CostController:
    def __init__(self, budget_limit: float = 1_000_000.0):
        self.monthly_budget = budget_limit
        
    def check_budget_availability(self, amount: float) -> bool:
        """
        Verifies if current spending is within limits.
        """
        current_spend = ledger.get_balance("Operating Expenses") + ledger.get_balance("Logistics Expenses")
        if current_spend + amount > self.monthly_budget:
            return False
        return True

    def log_procurement_cost(self, po_id: str, amount: float):
        """
        Records a purchase of inventory.
        """
        entry = JournalEntry(
            date=datetime.now(),
            description=f"Procurement for PO {po_id}",
            entries=[
                TransactionEntry(account="Inventory", debit=amount),
                TransactionEntry(account="Accounts Payable", credit=amount)
            ],
            reference_id=po_id
        )
        ledger.post_entry(entry)

    def log_logistics_cost(self, shipment_id: str, amount: float):
        """
        Records a shipping expense.
        """
        entry = JournalEntry(
            date=datetime.now(),
            description=f"Shipping for {shipment_id}",
            entries=[
                TransactionEntry(account="Logistics Expenses", debit=amount),
                TransactionEntry(account="Cash", credit=amount) # Assuming immediate payment for simplicty
            ],
            reference_id=shipment_id
        )
        ledger.post_entry(entry)

    def analyze_variance(self, state: SupplyChainState) -> List[AgentMessage]:
        """
        Routine to check financial health and alert if costs are spiraling.
        """
        alerts = []
        
        cogs = ledger.get_balance("COGS")
        logistics = ledger.get_balance("Logistics Expenses")
        
        # Heuristic: If logistics cost > 20% of inventory value, flag it.
        inventory_value = ledger.get_balance("Inventory")
        
        if inventory_value > 0 and (logistics / inventory_value) > 0.20:
             alerts.append(AgentMessage(
                sender="Finance",
                receiver="Logistics",
                content=f"Route optimization required. Logistics ratio {logistics/inventory_value:.1%} exceeds target.",
                priority="High"
            ))
            
        return alerts

controller = CostController()
