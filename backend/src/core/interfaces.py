"""
Abstract Base Classes for the Agent System.

Defines the contracts that all agents must implement, ensuring consistency
and enabling polymorphic behavior across the orchestration layer.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from backend.src.core.state import SupplyChainState, AgentMessage


class BaseAgent(ABC):
    """
    Interface for all domain agents.
    Ensures every agent implements a standard `run` method.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the unique identifier for this agent."""
        pass
    
    @abstractmethod
    def run(self, state: SupplyChainState) -> List[AgentMessage]:
        """
        Executes the agent's logic against the current system state.
        
        Args:
            state: The current global supply chain state.
            
        Returns:
            A list of messages to be logged and/or routed to other agents.
        """
        pass


class BaseAnalyzer(ABC):
    """
    Interface for analytical components that process data but do not directly
    modify the orchestration flow. Used for risk assessment, forecasting, etc.
    """
    
    @abstractmethod
    def analyze(self, data: Any) -> Dict[str, Any]:
        """
        Performs analysis on input data and returns structured results.
        """
        pass


class BaseRepository(ABC):
    """
    Interface for data access objects (DAOs).
    Implements the Repository Pattern to decouple business logic from persistence.
    """
    
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[Any]:
        """Retrieves a single entity by its unique identifier."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Any]:
        """Retrieves all entities of this type."""
        pass
    
    @abstractmethod
    def save(self, entity: Any) -> None:
        """Persists an entity to the data store."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Removes an entity from the data store."""
        pass


class BaseEventHandler(ABC):
    """
    Interface for event-driven components.
    Used by disruption handlers, notification services, etc.
    """
    
    @abstractmethod
    def handle(self, event: Dict[str, Any]) -> None:
        """Processes an incoming event."""
        pass
