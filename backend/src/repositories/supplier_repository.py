"""
Supplier Repository.

Implements the Repository Pattern to manage Supplier data access.
Decouples business logic from persistence concerns.
"""

from typing import List, Optional, Dict
from backend.src.core.interfaces import BaseRepository
from backend.src.core.state import Supplier


class SupplierRepository(BaseRepository):
    """
    In-memory repository for Supplier entities.
    In a production system, this would be backed by PostgreSQL or a similar RDBMS.
    """
    
    def __init__(self):
        self._store: Dict[str, Supplier] = {}
    
    def get_by_id(self, entity_id: str) -> Optional[Supplier]:
        return self._store.get(entity_id)
    
    def get_all(self) -> List[Supplier]:
        return list(self._store.values())
    
    def save(self, entity: Supplier) -> None:
        self._store[entity.id] = entity
    
    def delete(self, entity_id: str) -> bool:
        if entity_id in self._store:
            del self._store[entity_id]
            return True
        return False
    
    def find_by_reliability(self, min_score: float = 0.8) -> List[Supplier]:
        """
        Custom query to find suppliers above a reliability threshold.
        """
        return [s for s in self._store.values() if s.reliability_score >= min_score]
    
    def find_by_region(self, region: str) -> List[Supplier]:
        """
        Custom query to find suppliers in a specific region.
        """
        return [s for s in self._store.values() if region.lower() in s.location.lower()]
    
    def bulk_insert(self, suppliers: Dict[str, Supplier]) -> int:
        """
        Efficiently inserts multiple suppliers at once.
        Returns the count of inserted records.
        """
        initial_count = len(self._store)
        self._store.update(suppliers)
        return len(self._store) - initial_count


# Singleton instance
supplier_repository = SupplierRepository()
