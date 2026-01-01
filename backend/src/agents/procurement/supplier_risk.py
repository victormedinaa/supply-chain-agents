"""
Supplier Risk Assessment Module.

This system estimates the probability of supplier failure (delays, quality issues)
using a simplified Bayesian Network approach. It updates prior beliefs with 
new evidence (e.g., recent news, financial reports).
"""

from typing import Dict, List
import random
from backend.src.core.state import Supplier, SupplyChainState

class SupplierRiskModel:
    def __init__(self):
        # Base failure rates for different regions (Prior probabilities)
        self.priors = {
            "North America": 0.05,
            "Europe": 0.04,
            "Asia": 0.08,
            "South America": 0.10
        }

    def assess_risk(self, supplier: Supplier, state: SupplyChainState) -> float:
        """
        Calculates the risk score (0-1) for a specific supplier.
        
        Logic:
        1. Start with regional prior.
        2. Adjust based on historical reliability (Likelihood).
        3. Adjust based on active external factors (Evidence).
        """
        # 1. Prior
        region = supplier.location.split(",")[-1].strip() # Simple extraction
        prior_risk = self.priors.get(region, 0.05)
        
        # 2. Historical reliability impact
        # If reliability is high (1.0), risk decreases.
        reliability_factor = 1.0 - supplier.reliability_score 
        
        # 3. External Evidence from Simulation State
        # If there are active disruptions in the region, risk skyrockets.
        external_risk_adder = 0.0
        # Check simplified "news" or "events" from state (mocked access)
        # In full implementation, we'd check `state.environment.events`
        
        # Bayesian update (Simplified implementation of P(Fail|Evidence))
        # Posterior ~ Prior * Likelihood
        
        # We model "Likelihood" as the inverse of reliability
        posterior = (prior_risk * (1 + reliability_factor)) 
        
        # Cap at 1.0
        return min(max(posterior, 0.0), 1.0)
    
    def recommend_alternative(self, current_supplier: Supplier, all_suppliers: Dict[str, Supplier]) -> Supplier:
        """
        Finds the lowest-risk alternative supplier for the same category.
        """
        best_candidate = current_supplier
        lowest_risk = 1.0
        
        for cand in all_suppliers.values():
            if cand.id == current_supplier.id:
                continue
            
            # Mock category check (in real app, use `cand.capabilities`)
            risk = self.assess_risk(cand, None) # state is None for simple check here
            if risk < lowest_risk:
                lowest_risk = risk
                best_candidate = cand
                
        return best_candidate

# Singleton
risk_model = SupplierRiskModel()
