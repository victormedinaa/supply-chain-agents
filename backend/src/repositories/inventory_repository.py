"""
Inventory Repository.

Manages InventoryRecord data access.
"""

from typing import List, Optional, Dict
from backend.src.core.interfaces import BaseRepository
from backend.src.core.state import InventoryRecord


class InventoryRepository(BaseRepository):
    """
    In-memory repository for InventoryRecord entities.
    """
    
    def __init__(self):
        self._store: Dict[str, InventoryRecord] = {}
    
    def get_by_id(self, entity_id: str) -> Optional[InventoryRecord]:
        """entity_id format: 'WAREHOUSE_SKU'"""
        return self._store.get(entity_id)
    
    def get_all(self) -> List[InventoryRecord]:
        return list(self._store.values())
    
    def save(self, entity: InventoryRecord) -> None:
        key = f"{entity.warehouse_id}_{entity.sku}"
        self._store[key] = entity
    
    def delete(self, entity_id: str) -> bool:
        if entity_id in self._store:
            del self._store[entity_id]
            return True
        return False
    
    def find_by_sku(self, sku: str) -> List[InventoryRecord]:
        """
        Retrieves all inventory records for a specific SKU across all warehouses.
        """
        return [r for r in self._store.values() if r.sku == sku]
    
    def find_by_warehouse(self, warehouse_id: str) -> List[InventoryRecord]:
        """
        Retrieves all inventory records for a specific warehouse.
        """
        return [r for r in self._store.values() if r.warehouse_id == warehouse_id]
    
    def find_below_reorder_point(self) -> List[InventoryRecord]:
        """
        Identifies all SKUs that need replenishment.
        """
        return [r for r in self._store.values() if r.quantity_on_hand <= r.reorder_point]
    
    def get_total_on_hand(self, sku: str) -> int:
        """
        Calculates total quantity on hand for a SKU across all warehouses.
        """
        return sum(r.quantity_on_hand for r in self.find_by_sku(sku))
    
    def bulk_insert(self, records: Dict[str, InventoryRecord]) -> int:
        initial_count = len(self._store)
        self._store.update(records)
        return len(self._store) - initial_count


# Singleton instance
inventory_repository = InventoryRepository()
