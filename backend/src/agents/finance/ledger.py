"""
Financial Ledger System.

Implements a double-entry bookkeeping system to track the financial health of the supply chain.
Every operational action (buying parts, shipping) triggers a financial transaction.
"""

from typing import List, Optional
from datetime import datetime
import uuid
from pydantic import BaseModel, Field

class TransactionEntry(BaseModel):
    account: str
    debit: float = 0.0
    credit: float = 0.0

class JournalEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime
    description: str
    entries: List[TransactionEntry]
    reference_id: Optional[str] = None # Link to PO or Shipment ID

    def is_balanced(self) -> bool:
        total_debit = sum(e.debit for e in self.entries)
        total_credit = sum(e.credit for e in self.entries)
        return abs(total_debit - total_credit) < 0.01

class GeneralLedger:
    def __init__(self):
        self.journal: List[JournalEntry] = []
        self.chart_of_accounts = {
            "Cash": 0.0,
            "Inventory": 0.0,
            "Accounts Payable": 0.0,
            "COGS": 0.0,
            "Logistics Expenses": 0.0,
            "Operating Expenses": 0.0
        }

    def post_entry(self, entry: JournalEntry):
        if not entry.is_balanced():
            raise ValueError(f"Transaction {entry.id} is not balanced.")
        
        self.journal.append(entry)
        
        # Update account balances
        # Asset/Expense accounts (Cash, Inventory, COGS, Expenses) -> Debit increases
        # Liability/Equity/Revenue (Accounts Payable) -> Credit increases
        
        for line in entry.entries:
            # Simplified logic for demo balance tracking
            if line.account in ["Cash"]:
                self.chart_of_accounts[line.account] += line.debit - line.credit
            elif line.account in ["Accounts Payable"]:
                self.chart_of_accounts[line.account] += line.credit - line.debit
            else:
                # Default "Dr is +ve" behavior for assets/expenses
                self.chart_of_accounts[line.account] += line.debit - line.credit

    def get_balance(self, account: str) -> float:
        return self.chart_of_accounts.get(account, 0.0)

# Singleton
ledger = GeneralLedger()
