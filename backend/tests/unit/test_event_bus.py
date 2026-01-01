"""
Unit Tests for Event Bus.
"""

import unittest
from backend.src.core.event_bus import EventBus, Event, EventType


class TestEventBus(unittest.TestCase):
    
    def setUp(self):
        self.bus = EventBus()
        self.received_events = []
    
    def _handler(self, event: Event):
        self.received_events.append(event)
    
    def test_subscribe_and_publish(self):
        self.bus.subscribe(EventType.INVENTORY_LOW, self._handler)
        
        self.bus.emit(
            event_type=EventType.INVENTORY_LOW,
            payload={"sku": "SKU-001"},
            source="TestAgent"
        )
        
        self.assertEqual(len(self.received_events), 1)
        self.assertEqual(self.received_events[0].event_type, EventType.INVENTORY_LOW)
    
    def test_unsubscribe_stops_events(self):
        self.bus.subscribe(EventType.SHIPMENT_DELAYED, self._handler)
        self.bus.unsubscribe(EventType.SHIPMENT_DELAYED, self._handler)
        
        self.bus.emit(
            event_type=EventType.SHIPMENT_DELAYED,
            payload={},
            source="Test"
        )
        
        self.assertEqual(len(self.received_events), 0)
    
    def test_get_history_returns_events(self):
        self.bus.emit(EventType.ORDER_PLACED, {"order_id": "1"}, "Test")
        self.bus.emit(EventType.ORDER_COMPLETED, {"order_id": "1"}, "Test")
        
        history = self.bus.get_history()
        
        self.assertEqual(len(history), 2)
    
    def test_get_history_filters_by_type(self):
        self.bus.emit(EventType.ORDER_PLACED, {}, "Test")
        self.bus.emit(EventType.QUALITY_FAILED, {}, "Test")
        
        filtered = self.bus.get_history(event_type=EventType.ORDER_PLACED)
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].event_type, EventType.ORDER_PLACED)
    
    def test_clear_history(self):
        self.bus.emit(EventType.BUDGET_EXCEEDED, {}, "Test")
        self.bus.clear_history()
        
        self.assertEqual(len(self.bus.get_history()), 0)


if __name__ == '__main__':
    unittest.main()
