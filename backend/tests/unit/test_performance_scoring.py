"""
Unit Tests for Performance Scoring Engine.
"""

import unittest
from backend.src.services.performance_scoring import PerformanceScoringEngine, PerformanceMetrics
from backend.src.core.state import Supplier


class TestPerformanceScoringEngine(unittest.TestCase):
    
    def setUp(self):
        self.engine = PerformanceScoringEngine()
        self.sample_supplier = Supplier(
            id="SUP-TEST",
            name="Test Supplier",
            reliability_score=0.9,
            location="Test Zone",
            contract_terms={}
        )
    
    def test_record_delivery_updates_metric(self):
        initial = self.engine._get_or_create_metrics("SUP-001").on_time_delivery_rate
        
        self.engine.record_delivery("SUP-001", was_on_time=False)
        
        updated = self.engine._get_or_create_metrics("SUP-001").on_time_delivery_rate
        self.assertLess(updated, initial)
    
    def test_record_quality_updates_metric(self):
        self.engine.record_quality_result("SUP-002", passed=True)
        
        metrics = self.engine._get_or_create_metrics("SUP-002")
        self.assertGreater(metrics.quality_acceptance_rate, 0)
    
    def test_composite_score_in_range(self):
        score = self.engine.calculate_composite_score("SUP-003")
        
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_tier_gold(self):
        tier = self.engine.determine_tier(0.95)
        self.assertEqual(tier, "Gold")
    
    def test_tier_silver(self):
        tier = self.engine.determine_tier(0.80)
        self.assertEqual(tier, "Silver")
    
    def test_tier_bronze(self):
        tier = self.engine.determine_tier(0.65)
        self.assertEqual(tier, "Bronze")
    
    def test_tier_under_review(self):
        tier = self.engine.determine_tier(0.50)
        self.assertEqual(tier, "Under Review")
    
    def test_get_scorecard_returns_valid_object(self):
        scorecard = self.engine.get_scorecard(self.sample_supplier)
        
        self.assertEqual(scorecard.supplier_id, "SUP-TEST")
        self.assertIsNotNone(scorecard.composite_score)
        self.assertIn(scorecard.tier, ["Gold", "Silver", "Bronze", "Under Review"])
    
    def test_rank_suppliers_sorted_descending(self):
        suppliers = [
            Supplier(id="A", name="A", reliability_score=0.5, location="", contract_terms={}),
            Supplier(id="B", name="B", reliability_score=0.9, location="", contract_terms={}),
        ]
        
        # Modify scores to ensure different rankings
        self.engine.record_delivery("A", was_on_time=False)
        self.engine.record_delivery("A", was_on_time=False)
        self.engine.record_delivery("B", was_on_time=True)
        
        ranked = self.engine.rank_suppliers(suppliers)
        
        self.assertEqual(ranked[0].supplier_id, "B")


if __name__ == '__main__':
    unittest.main()
