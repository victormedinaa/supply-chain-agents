"""
Dependency Injection Container.

Provides a centralized container for managing dependencies across the application.
Follows the Inversion of Control (IoC) principle for better testability.
"""

from typing import Dict, Any, TypeVar, Type, Optional
from functools import lru_cache

T = TypeVar('T')


class Container:
    """
    Simple dependency injection container.
    Supports singleton and factory registrations.
    """
    
    def __init__(self):
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, callable] = {}
    
    def register_singleton(self, key: str, instance: Any) -> None:
        """Registers a pre-instantiated singleton."""
        self._singletons[key] = instance
    
    def register_factory(self, key: str, factory: callable) -> None:
        """Registers a factory function that creates new instances."""
        self._factories[key] = factory
    
    def resolve(self, key: str) -> Any:
        """Resolves a dependency by key."""
        if key in self._singletons:
            return self._singletons[key]
        
        if key in self._factories:
            instance = self._factories[key]()
            self._singletons[key] = instance  # Cache the instance
            return instance
        
        raise KeyError(f"Dependency '{key}' not registered.")
    
    def resolve_or_none(self, key: str) -> Optional[Any]:
        """Resolves a dependency or returns None if not found."""
        try:
            return self.resolve(key)
        except KeyError:
            return None
    
    def has(self, key: str) -> bool:
        """Checks if a dependency is registered."""
        return key in self._singletons or key in self._factories
    
    def clear(self) -> None:
        """Clears all registrations (useful for testing)."""
        self._singletons.clear()
        self._factories.clear()


# Global container instance
container = Container()


def inject(key: str) -> Any:
    """Convenience function to resolve dependencies."""
    return container.resolve(key)


def register_defaults():
    """Registers default implementations for all services."""
    from backend.src.core.llm_provider import get_llm
    from backend.src.services.alert_manager import AlertManager
    from backend.src.services.performance_scoring import PerformanceScoringEngine
    from backend.src.services.location_optimizer import LocationOptimizer
    from backend.src.services.notification_service import NotificationService
    from backend.src.repositories.supplier_repository import SupplierRepository
    from backend.src.repositories.part_repository import PartRepository
    from backend.src.repositories.inventory_repository import InventoryRepository
    
    container.register_factory("llm", get_llm)
    container.register_factory("alert_manager", AlertManager)
    container.register_factory("scoring_engine", PerformanceScoringEngine)
    container.register_factory("location_optimizer", LocationOptimizer)
    container.register_factory("notification_service", NotificationService)
    container.register_factory("supplier_repo", SupplierRepository)
    container.register_factory("part_repo", PartRepository)
    container.register_factory("inventory_repo", InventoryRepository)
