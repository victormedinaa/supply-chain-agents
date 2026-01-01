"""
Unit Tests for Supplier Repository.
"""

import unittest
from backend.src.repositories.supplier_repository import SupplierRepository
from backend.src.core.state import Supplier


class TestSupplierRepository(unittest.TestCase):
    
    def setUp(self):
        self.repo = SupplierRepository()
        self.sample_supplier = Supplier(
            id="SUP-001",
            name="Test Supplier",
            reliability_score=0.85,
            location="Industrial Zone, Europe",
            contract_terms={"payment": "Net30"}
        )
    
    def test_save_and_get_by_id(self):
        self.repo.save(self.sample_supplier)
        
        result = self.repo.get_by_id("SUP-001")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Test Supplier")
    
    def test_get_by_id_returns_none_for_missing(self):
        result = self.repo.get_by_id("NONEXISTENT")
        
        self.assertIsNone(result)
    
    def test_get_all_returns_list(self):
        self.repo.save(self.sample_supplier)
        
        result = self.repo.get_all()
        
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 1)
    
    def test_delete_removes_supplier(self):
        self.repo.save(self.sample_supplier)
        
        result = self.repo.delete("SUP-001")
        
        self.assertTrue(result)
        self.assertIsNone(self.repo.get_by_id("SUP-001"))
    
    def test_delete_returns_false_for_missing(self):
        result = self.repo.delete("NONEXISTENT")
        
        self.assertFalse(result)
    
    def test_find_by_reliability_filters_correctly(self):
        low_rel = Supplier(
            id="SUP-LOW", name="Low Rel", reliability_score=0.5,
            location="Somewhere", contract_terms={}
        )
        high_rel = Supplier(
            id="SUP-HIGH", name="High Rel", reliability_score=0.95,
            location="Somewhere", contract_terms={}
        )
        self.repo.save(low_rel)
        self.repo.save(high_rel)
        
        result = self.repo.find_by_reliability(min_score=0.8)
        
        self.assertIn(high_rel, result)
        self.assertNotIn(low_rel, result)
    
    def test_bulk_insert_adds_multiple(self):
        suppliers = {
            "SUP-A": Supplier(id="SUP-A", name="A", reliability_score=0.9, location="A", contract_terms={}),
            "SUP-B": Supplier(id="SUP-B", name="B", reliability_score=0.8, location="B", contract_terms={})
        }
        
        count = self.repo.bulk_insert(suppliers)
        
        self.assertEqual(count, 2)
        self.assertIsNotNone(self.repo.get_by_id("SUP-A"))
        self.assertIsNotNone(self.repo.get_by_id("SUP-B"))


if __name__ == '__main__':
    unittest.main()
