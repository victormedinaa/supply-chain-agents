"""
Procurement Negotiator Agent.

This agent simulates high-stakes negotiation with suppliers. 
It uses a Generative AI model to generate email drafts or API messages attempting to 
secure better prices or expedited shipping based on the `SupplierRiskModel` output.
"""

from typing import List
from langchain_core.prompts import ChatPromptTemplate
from backend.src.core.state import Supplier, SupplyChainState, AgentMessage
from backend.src.agents.procurement.supplier_risk import risk_model
from backend.src.core.llm_provider import get_llm

class Negotiator:
    def __init__(self, model_name: str = "gpt-4-turbo"):
        self.llm = get_llm(model_name=model_name, temperature=0.7)
    
    def draft_negotiation_email(self, supplier: Supplier, issue_type: str, state: SupplyChainState) -> str:
        """
        Drafts a negotiation message.
        
        Args:
            issue_type: 'price_reduction', 'expedite_shipping', 'quality_complaint'
        """
        current_risk = risk_model.assess_risk(supplier, state)
        
        # Strategy selection based on leverage (risk vs. reliability)
        if current_risk > 0.15:
            strategy = "Aggressive - Threaten to switch to alternative"
        elif supplier.reliability_score > 0.9:
            strategy = "Collaborative - Leveraging long-term partnership"
        else:
            strategy = "Neutral - Fact-based"
            
        prompt = ChatPromptTemplate.from_template(
            """
            You are a Senior Procurement Manager at a leading automotive company.
            Write a formal negotiation email to supplier '{supplier_name}'.
            
            Context:
            - Issue: {issue_type}
            - Current Risk Score: {risk_score} (High risk means we are worried)
            - Supplier Reliability: {reliability}
            
            Selected Strategy: {strategy}
            
            Draft the email body only. Be professional but firm.
            """
        )
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "supplier_name": supplier.name,
            "issue_type": issue_type,
            "risk_score": round(current_risk, 2),
            "reliability": supplier.reliability_score,
            "strategy": strategy
        })
        
        return response.content

    def run_routine(self, state: SupplyChainState) -> List[AgentMessage]:
        """
        Main entry point for the agent when called by the Orchestrator.
        """
        messages = []
        
        # Sca for high-risk suppliers or shortages
        # Mock logic: Assume we need to expedite shipping for SKU-001
        target_supplier_id = "SUP-001" # Mock
        if target_supplier_id in state.suppliers:
            supplier = state.suppliers[target_supplier_id]
            email = self.draft_negotiation_email(supplier, "expedite_shipping", state)
            
            messages.append(AgentMessage(
                sender="Procurement",
                receiver="Orchestrator",
                content=f"Negotiation initiated with {supplier.name}. Draft: {email[:50]}...",
                structured_data={"full_draft": email}
            ))
            
        return messages

# Singleton
negotiator = Negotiator()
