"""
Event Bus.

Implements a publish/subscribe pattern for decoupled inter-agent communication.
Agents can emit events without knowing who will consume them.
"""

from typing import Dict, List, Callable, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class EventType(str, Enum):
    INVENTORY_LOW = "INVENTORY_LOW"
    SHIPMENT_DELAYED = "SHIPMENT_DELAYED"
    ORDER_PLACED = "ORDER_PLACED"
    ORDER_COMPLETED = "ORDER_COMPLETED"
    QUALITY_FAILED = "QUALITY_FAILED"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    SUPPLIER_RISK_HIGH = "SUPPLIER_RISK_HIGH"
    PRODUCTION_HALTED = "PRODUCTION_HALTED"


class Event(BaseModel):
    """Represents a domain event."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    payload: Dict[str, Any]
    source: str
    timestamp: datetime = Field(default_factory=datetime.now)


class EventBus:
    """
    Central event dispatcher.
    Handlers subscribe to event types and are invoked when events are published.
    """
    
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable[[Event], None]]] = {}
        self._event_log: List[Event] = []
    
    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        """Registers a handler for a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        """Removes a handler from an event type."""
        if event_type in self._subscribers:
            self._subscribers[event_type] = [h for h in self._subscribers[event_type] if h != handler]
    
    def publish(self, event: Event):
        """Dispatches an event to all registered handlers."""
        self._event_log.append(event)
        handlers = self._subscribers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"[EventBus] Handler error for {event.event_type}: {e}")
    
    def emit(self, event_type: EventType, payload: Dict[str, Any], source: str):
        """Convenience method to create and publish an event."""
        event = Event(event_type=event_type, payload=payload, source=source)
        self.publish(event)
    
    def get_history(self, event_type: EventType = None, limit: int = 100) -> List[Event]:
        """Retrieves recent events, optionally filtered by type."""
        events = self._event_log
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return events[-limit:]
    
    def clear_history(self):
        """Clears the event log (useful for testing)."""
        self._event_log = []


# Singleton instance
event_bus = EventBus()
