"""
Unit Tests for Location Optimizer Service.
"""

import unittest
from backend.src.services.location_optimizer import LocationOptimizer, GeographicPoint


class TestLocationOptimizer(unittest.TestCase):
    
    def setUp(self):
        self.optimizer = LocationOptimizer()
    
    def test_haversine_distance_same_point_is_zero(self):
        distance = self.optimizer.haversine_distance(48.8566, 2.3522, 48.8566, 2.3522)
        
        self.assertEqual(distance, 0.0)
    
    def test_haversine_distance_paris_to_london(self):
        # Paris to London is approximately 340km
        distance = self.optimizer.haversine_distance(48.8566, 2.3522, 51.5074, -0.1278)
        
        self.assertGreater(distance, 300)
        self.assertLess(distance, 400)
    
    def test_center_of_gravity_single_point(self):
        points = [GeographicPoint(name="A", latitude=50.0, longitude=10.0)]
        
        lat, lon = self.optimizer.calculate_center_of_gravity(points)
        
        self.assertEqual(lat, 50.0)
        self.assertEqual(lon, 10.0)
    
    def test_center_of_gravity_two_equal_points(self):
        points = [
            GeographicPoint(name="A", latitude=40.0, longitude=0.0),
            GeographicPoint(name="B", latitude=50.0, longitude=10.0)
        ]
        
        lat, lon = self.optimizer.calculate_center_of_gravity(points)
        
        self.assertAlmostEqual(lat, 45.0, places=4)
        self.assertAlmostEqual(lon, 5.0, places=4)
    
    def test_center_of_gravity_weighted(self):
        points = [
            GeographicPoint(name="A", latitude=40.0, longitude=0.0, weight=1.0),
            GeographicPoint(name="B", latitude=50.0, longitude=10.0, weight=3.0)
        ]
        
        lat, lon = self.optimizer.calculate_center_of_gravity(points)
        
        # Weighted average should be closer to B
        self.assertGreater(lat, 45.0)
        self.assertGreater(lon, 5.0)
    
    def test_optimize_returns_recommendation(self):
        points = [
            GeographicPoint(name="Munich", latitude=48.1351, longitude=11.5820),
            GeographicPoint(name="Stuttgart", latitude=48.7758, longitude=9.1829),
            GeographicPoint(name="Frankfurt", latitude=50.1109, longitude=8.6821)
        ]
        
        result = self.optimizer.optimize(points)
        
        self.assertIsNotNone(result.suggested_latitude)
        self.assertIsNotNone(result.suggested_longitude)
        self.assertGreater(len(result.served_locations), 0)
    
    def test_optimize_raises_on_empty_points(self):
        with self.assertRaises(ValueError):
            self.optimizer.calculate_center_of_gravity([])


if __name__ == '__main__':
    unittest.main()
