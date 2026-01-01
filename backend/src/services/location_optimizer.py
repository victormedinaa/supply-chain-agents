"""
Warehouse Location Optimizer.

Determines optimal placement of distribution centers based on demand patterns,
supplier locations, and transportation costs.
Uses a simplified Center of Gravity method enhanced with constraints.
"""

from typing import List, Dict, Tuple
from pydantic import BaseModel, Field
import math


class GeographicPoint(BaseModel):
    """Represents a point on the globe."""
    name: str
    latitude: float
    longitude: float
    weight: float = 1.0  # Demand volume or importance factor


class WarehouseRecommendation(BaseModel):
    """Output of the location optimization."""
    suggested_latitude: float
    suggested_longitude: float
    coverage_radius_km: float
    total_weighted_distance: float
    served_locations: List[str]


class LocationOptimizer:
    """
    Calculates optimal warehouse placement using weighted center of gravity.
    """
    
    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculates the great-circle distance between two points on Earth.
        Returns distance in kilometers.
        """
        R = 6371  # Earth's radius in km
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def calculate_center_of_gravity(self, points: List[GeographicPoint]) -> Tuple[float, float]:
        """
        Calculates the weighted center of gravity for a set of points.
        """
        if not points:
            raise ValueError("At least one point is required for optimization.")
        
        total_weight = sum(p.weight for p in points)
        weighted_lat = sum(p.latitude * p.weight for p in points) / total_weight
        weighted_lon = sum(p.longitude * p.weight for p in points) / total_weight
        
        return round(weighted_lat, 6), round(weighted_lon, 6)
    
    def optimize(self, demand_points: List[GeographicPoint], max_coverage_km: float = 500.0) -> WarehouseRecommendation:
        """
        Performs the location optimization and returns a recommendation.
        """
        cog_lat, cog_lon = self.calculate_center_of_gravity(demand_points)
        
        # Calculate total weighted distance from COG to all points
        total_distance = 0.0
        served = []
        
        for point in demand_points:
            dist = self.haversine_distance(cog_lat, cog_lon, point.latitude, point.longitude)
            total_distance += dist * point.weight
            if dist <= max_coverage_km:
                served.append(point.name)
        
        return WarehouseRecommendation(
            suggested_latitude=cog_lat,
            suggested_longitude=cog_lon,
            coverage_radius_km=max_coverage_km,
            total_weighted_distance=round(total_distance, 2),
            served_locations=served
        )
    
    def multi_warehouse_optimization(self, demand_points: List[GeographicPoint], num_warehouses: int = 2) -> List[WarehouseRecommendation]:
        """
        Simplified k-means approach for multiple warehouse placement.
        For production, use proper k-means or p-median algorithms.
        """
        if num_warehouses >= len(demand_points):
            # Edge case: More warehouses than demand points
            return [
                WarehouseRecommendation(
                    suggested_latitude=p.latitude,
                    suggested_longitude=p.longitude,
                    coverage_radius_km=100.0,
                    total_weighted_distance=0.0,
                    served_locations=[p.name]
                ) for p in demand_points
            ]
        
        # Simplified: Split points into clusters based on longitude (east/west split)
        sorted_points = sorted(demand_points, key=lambda p: p.longitude)
        cluster_size = len(sorted_points) // num_warehouses
        
        recommendations = []
        for i in range(num_warehouses):
            start_idx = i * cluster_size
            end_idx = start_idx + cluster_size if i < num_warehouses - 1 else len(sorted_points)
            cluster = sorted_points[start_idx:end_idx]
            
            if cluster:
                rec = self.optimize(cluster)
                recommendations.append(rec)
        
        return recommendations


# Singleton instance
location_optimizer = LocationOptimizer()
