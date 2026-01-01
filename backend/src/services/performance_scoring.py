"""
Supplier Performance Scoring Engine.

Calculates a composite score for each supplier based on multiple Key Performance Indicators (KPIs).
Used by Procurement to make data-driven sourcing decisions.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from backend.src.core.state import Supplier


class PerformanceMetrics(BaseModel):
    """KPIs tracked for a single supplier."""
    supplier_id: str
    on_time_delivery_rate: float = Field(default=1.0, ge=0.0, le=1.0)
    quality_acceptance_rate: float = Field(default=1.0, ge=0.0, le=1.0)
    responsiveness_score: float = Field(default=1.0, ge=0.0, le=1.0)
    cost_competitiveness: float = Field(default=1.0, ge=0.0, le=1.0)
    sustainability_rating: float = Field(default=0.5, ge=0.0, le=1.0)
    last_updated: datetime = Field(default_factory=datetime.now)


class SupplierScorecard(BaseModel):
    """Aggregated scorecard for a supplier."""
    supplier_id: str
    supplier_name: str
    composite_score: float
    tier: str
    metrics: PerformanceMetrics


class PerformanceScoringEngine:
    """
    Calculates weighted composite scores and assigns supplier tiers.
    """
    
    def __init__(self):
        self._metrics_store: Dict[str, PerformanceMetrics] = {}
        self._weights = {
            "on_time_delivery_rate": 0.30,
            "quality_acceptance_rate": 0.25,
            "responsiveness_score": 0.15,
            "cost_competitiveness": 0.20,
            "sustainability_rating": 0.10
        }
    
    def record_delivery(self, supplier_id: str, was_on_time: bool):
        """Updates the on-time delivery metric for a supplier."""
        metrics = self._get_or_create_metrics(supplier_id)
        current_rate = metrics.on_time_delivery_rate
        # Exponential Moving Average (EMA) update
        alpha = 0.1
        new_value = 1.0 if was_on_time else 0.0
        metrics.on_time_delivery_rate = (alpha * new_value) + ((1 - alpha) * current_rate)
        metrics.last_updated = datetime.now()
    
    def record_quality_result(self, supplier_id: str, passed: bool):
        """Updates the quality acceptance metric."""
        metrics = self._get_or_create_metrics(supplier_id)
        current_rate = metrics.quality_acceptance_rate
        alpha = 0.1
        new_value = 1.0 if passed else 0.0
        metrics.quality_acceptance_rate = (alpha * new_value) + ((1 - alpha) * current_rate)
        metrics.last_updated = datetime.now()
    
    def update_responsiveness(self, supplier_id: str, response_hours: float):
        """Updates responsiveness based on average response time."""
        metrics = self._get_or_create_metrics(supplier_id)
        # Score is inversely proportional to response time (max 24h)
        score = max(0.0, 1.0 - (response_hours / 24.0))
        alpha = 0.15
        metrics.responsiveness_score = (alpha * score) + ((1 - alpha) * metrics.responsiveness_score)
        metrics.last_updated = datetime.now()
    
    def update_cost_competitiveness(self, supplier_id: str, quote_vs_market_ratio: float):
        """Updates cost competitiveness (lower ratio = more competitive)."""
        metrics = self._get_or_create_metrics(supplier_id)
        score = max(0.0, min(1.0, 2.0 - quote_vs_market_ratio))
        alpha = 0.2
        metrics.cost_competitiveness = (alpha * score) + ((1 - alpha) * metrics.cost_competitiveness)
        metrics.last_updated = datetime.now()
    
    def calculate_composite_score(self, supplier_id: str) -> float:
        """Calculates the weighted composite score for a supplier."""
        metrics = self._get_or_create_metrics(supplier_id)
        score = 0.0
        score += self._weights["on_time_delivery_rate"] * metrics.on_time_delivery_rate
        score += self._weights["quality_acceptance_rate"] * metrics.quality_acceptance_rate
        score += self._weights["responsiveness_score"] * metrics.responsiveness_score
        score += self._weights["cost_competitiveness"] * metrics.cost_competitiveness
        score += self._weights["sustainability_rating"] * metrics.sustainability_rating
        return round(score, 4)
    
    def determine_tier(self, score: float) -> str:
        """Assigns a tier based on composite score thresholds."""
        if score >= 0.90:
            return "Gold"
        elif score >= 0.75:
            return "Silver"
        elif score >= 0.60:
            return "Bronze"
        else:
            return "Under Review"
    
    def get_scorecard(self, supplier: Supplier) -> SupplierScorecard:
        """Generates a full scorecard for a supplier."""
        metrics = self._get_or_create_metrics(supplier.id)
        score = self.calculate_composite_score(supplier.id)
        tier = self.determine_tier(score)
        return SupplierScorecard(
            supplier_id=supplier.id,
            supplier_name=supplier.name,
            composite_score=score,
            tier=tier,
            metrics=metrics
        )
    
    def get_all_scorecards(self, suppliers: List[Supplier]) -> List[SupplierScorecard]:
        """Generates scorecards for all suppliers."""
        return [self.get_scorecard(s) for s in suppliers]
    
    def rank_suppliers(self, suppliers: List[Supplier]) -> List[SupplierScorecard]:
        """Returns scorecards sorted by composite score (descending)."""
        scorecards = self.get_all_scorecards(suppliers)
        return sorted(scorecards, key=lambda sc: sc.composite_score, reverse=True)
    
    def _get_or_create_metrics(self, supplier_id: str) -> PerformanceMetrics:
        if supplier_id not in self._metrics_store:
            self._metrics_store[supplier_id] = PerformanceMetrics(supplier_id=supplier_id)
        return self._metrics_store[supplier_id]


# Singleton instance
scoring_engine = PerformanceScoringEngine()
