"""
Unit Tests for Custom Exceptions.
"""

import unittest
from backend.src.core.exceptions import (
    SupplyChainException, BudgetExceededException, InventoryShortageException,
    SupplierUnavailableException, RouteNotFoundException, QualityControlFailedException,
    GraphExecutionException
)


class TestBudgetExceededException(unittest.TestCase):
    
    def test_message_formatting(self):
        exc = BudgetExceededException(requested_amount=15000.0, available_budget=10000.0)
        
        self.assertIn("$15,000.00", str(exc))
        self.assertIn("$10,000.00", str(exc))
    
    def test_attributes_stored(self):
        exc = BudgetExceededException(5000.0, 3000.0)
        
        self.assertEqual(exc.requested_amount, 5000.0)
        self.assertEqual(exc.available_budget, 3000.0)


class TestInventoryShortageException(unittest.TestCase):
    
    def test_message_formatting(self):
        exc = InventoryShortageException(sku="SKU-001", required=100, available=25)
        
        self.assertIn("SKU-001", str(exc))
        self.assertIn("100", str(exc))
        self.assertIn("25", str(exc))


class TestSupplierUnavailableException(unittest.TestCase):
    
    def test_message_formatting(self):
        exc = SupplierUnavailableException(supplier_id="SUP-005", reason="Bankrupt")
        
        self.assertIn("SUP-005", str(exc))
        self.assertIn("Bankrupt", str(exc))


class TestRouteNotFoundException(unittest.TestCase):
    
    def test_message_formatting(self):
        exc = RouteNotFoundException(origin="Shanghai", destination="Mars")
        
        self.assertIn("Shanghai", str(exc))
        self.assertIn("Mars", str(exc))


class TestQualityControlFailedException(unittest.TestCase):
    
    def test_message_formatting(self):
        exc = QualityControlFailedException(batch_id="B-100", defect_rate=0.15, threshold=0.05)
        
        self.assertIn("B-100", str(exc))
        self.assertIn("15.00%", str(exc))
        self.assertIn("5.00%", str(exc))


class TestGraphExecutionException(unittest.TestCase):
    
    def test_message_formatting(self):
        exc = GraphExecutionException(agent_name="Procurement", details="Timeout")
        
        self.assertIn("Procurement", str(exc))
        self.assertIn("Timeout", str(exc))


class TestExceptionHierarchy(unittest.TestCase):
    
    def test_all_inherit_from_base(self):
        exceptions = [
            BudgetExceededException(1, 1),
            InventoryShortageException("sku", 1, 1),
            SupplierUnavailableException("id", "reason"),
            RouteNotFoundException("a", "b"),
            QualityControlFailedException("b", 0.1, 0.1),
            GraphExecutionException("agent", "detail")
        ]
        
        for exc in exceptions:
            self.assertIsInstance(exc, SupplyChainException)


if __name__ == '__main__':
    unittest.main()
