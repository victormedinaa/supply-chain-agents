"""
Quality Inspector Agent.

Uses Statistical Process Control (SPC) concepts to monitor part quality.
Simulates sampling from incoming batches and flagging defects based on 'sigma' levels.
"""

from typing import List, Dict, Tuple
import random
import statistics
from backend.src.core.state import SupplyChainState, Part, AgentMessage

class QualityInspector:
    def inspect_delivery(self, shipment_id: str, parts: List[Part]) -> Tuple[float, List[str]]:
        """
        Simulates inspecting a shipment.
        Result: (Defect Rate, List of defective SKU IDs)
        """
        defective_skus = []
        sample_size = min(len(parts), 50) # Inspect random sample
        sample = random.sample(parts, sample_size)
        
        defects_found = 0
        for part in sample:
            # Simulate physical measurement
            # Nominal spec: 10.0mm. Tolerance +/- 0.1mm
            actual_measurement = random.gauss(10.0, 0.05) 
            
            if not (9.9 <= actual_measurement <= 10.1):
                defects_found += 1
                defective_skus.append(part.sku)
                
        defect_rate = defects_found / sample_size
        return defect_rate, defective_skus

    def monitor_quality(self, state: SupplyChainState) -> List[AgentMessage]:
        """
        Routine to scan recent deliveries for quality issues.
        """
        alerts = []
        # Mocking access to a 'recent_deliveries' list which would be part of state
        # For demo, we just simulate a random spot check
        
        if random.random() < 0.1: # 10% chance of a spot check finding something
            alerts.append(AgentMessage(
                sender="Quality", receiver="Procurement",
                content="High defect rate (3.2%) detected in batch batch-009 from Supplier-004. Initiate RCA.",
                priority="High"
            ))
            
        return alerts

inspector = QualityInspector()
