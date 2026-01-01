"""
Simulation Environment.

Controls the passage of time and stochastic global events (Macro-economic shocks, Weather).
"""

import random
from datetime import datetime, timedelta
from backend.src.core.state import SupplyChainState

class SimulationEnvironment:
    def step(self, state: SupplyChainState):
        """
        Advances the simulation by one 'step' (e.g., 1 day).
        """
        state.simulation_step += 1
        state.current_time += timedelta(days=1)
        
        # Random Event Generation
        if random.random() < 0.05: # 5% chance of major event
            event_type = random.choice(["Strike", "Weather", "Tariff"])
            state.errors.append(f"GLOBAL EVENT: {event_type} disruption detected.")
            
        # Decay reliability slightly over time to force procurement to stay active
        for s in state.suppliers.values():
            if random.random() < 0.1:
                s.reliability_score = max(0.1, s.reliability_score - 0.01)

environment = SimulationEnvironment()
