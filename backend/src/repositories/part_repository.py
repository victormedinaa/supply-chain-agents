"""
Part Repository.

Implements the Repository Pattern to manage Part data access.
"""

from typing import List, Optional, Dict
from backend.src.core.interfaces import BaseRepository
from backend.src.core.state import Part


class PartRepository(BaseRepository):
    """
    In-memory repository for Part entities.
    """
    
    def __init__(self):
        self._store: Dict[str, Part] = {}
    
    def get_by_id(self, entity_id: str) -> Optional[Part]:
        return self._store.get(entity_id)
    
    def get_all(self) -> List[Part]:
        return list(self._store.values())
    
    def save(self, entity: Part) -> None:
        self._store[entity.sku] = entity
    
    def delete(self, entity_id: str) -> bool:
        if entity_id in self._store:
            del self._store[entity_id]
            return True
        return False
    
    def find_by_category(self, category: str) -> List[Part]:
        """
        Retrieves all parts belonging to a specific category.
        """
        return [p for p in self._store.values() if p.category == category]
    
    def find_by_supplier(self, supplier_id: str) -> List[Part]:
        """
        Retrieves all parts sourced from a specific supplier.
        """
        return [p for p in self._store.values() if p.supplier_id == supplier_id]
    
    def get_total_value(self) -> float:
        """
        Calculates the total catalog value (sum of all part costs).
        """
        return sum(p.cost for p in self._store.values())
    
    def bulk_insert(self, parts: Dict[str, Part]) -> int:
        """
        Efficiently inserts multiple parts at once.
        """
        initial_count = len(self._store)
        self._store.update(parts)
        return len(self._store) - initial_count


# Singleton instance
part_repository = PartRepository()
