"""
Demand Forecasting Module: Hybrid Statistical & Generative Model Approach.

This module implements a sophisticated forecasting engine that combines:
1.  **Quantitative Analysis**: Using ARIMA (AutoRegressive Integrated Moving Average) 
    concepts to project historical sales data.
2.  **Qualitative Adjustment**: Using LLMs to interpret unstructured market signals 
    (news, economic indicators) and adjust the statistical baseline.

The `ForecastAgent` is responsible for predicting the required quantity of parts 
based on the production schedule and external market factors.
"""

from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from backend.src.core.state import SupplyChainState, Part
from backend.src.core.llm_provider import get_llm

class DemandForecaster:
    def __init__(self, model_name: str = "gpt-4-turbo"):
        self.llm = get_llm(model_name=model_name, temperature=0.2)
        
    def _calculate_statistical_baseline(self, historical_data: pd.DataFrame, horizon_days: int = 30) -> Dict[str, float]:
        """
        Simulates a time-series forecast using a moving average with trend component.
        In a real production system, this would use `statsmodels.tsa.arima.model`.
        
        Args:
            historical_data: DataFrame with 'date' and 'quantity' columns.
            horizon_days: Number of days to forecast.
            
        Returns:
            Dictionary mapping SKU to predicted total demand over the horizon.
        """
        # Placeholder logic simulating a robust statistical projection
        # We assume a 5% monthly growth trend + random noise
        baseline_predictions = {}
        unique_skus = historical_data['sku'].unique()
        
        for sku in unique_skus:
            sku_data = historical_data[historical_data['sku'] == sku]
            avg_daily_demand = sku_data['quantity'].mean()
            # Apply growth factor
            projected_demand = avg_daily_demand * horizon_days * 1.05 
            baseline_predictions[sku] = round(projected_demand, 2)
            
        return baseline_predictions

    def _get_market_intelligence(self, state: SupplyChainState) -> str:
        """
        Synthesizes a text summary of the current market conditions from the simulation environment.
        """
        # In a real system, this would RAG against a news database.
        # Here we mock it based on simulation step to create scenarios.
        if state.simulation_step == 5:
            return "Reports indicate a strike at major semiconductor ports in Taiwan. Chip shortage expected."
        elif state.simulation_step == 10:
            return "Steel prices rely due to increased global infrastructure spending."
        else:
            return "Market conditions are stable with slight inflationary pressure."

    def generate_forecast(self, state: SupplyChainState, historical_data: pd.DataFrame) -> Dict[str, float]:
        """
        Generates the final forecast by enriching the statistical baseline with LLM insights.
        """
        baseline = self._calculate_statistical_baseline(historical_data)
        market_context = self._get_market_intelligence(state)
        
        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert Supply Chain Demand Planner.
            
            We have a statistical baseline forecast for automotive parts: 
            {baseline}
            
            However, we have received the following market intelligence:
            "{market_context}"
            
            Your task:
            1. Analyze how the market context impacts specific part categories (Electronics, Chassis, etc.).
            2. Adjust the baseline numbers accordingly (e.g., increase safety stock for threatened parts).
            3. Return the ADJUSTED forecast mapping (SKU -> Quantity).
            
            Output ONLY a valid JSON object.
            """
        )
        
        chain = prompt | self.llm | JsonOutputParser()
        
        try:
            # We wrap in a try-except to handle potential LLM parsing errors gracefully
            # In a research context, we might log this for analysis.
            adjusted_forecast = chain.invoke({
                "baseline": baseline,
                "market_context": market_context
            })
            return adjusted_forecast
        except Exception as e:
            # Fallback to statistical baseline if LLM fails
            print(f"Forecast Agent Error: {e}")
            return baseline

# Singleton for reuse
forecaster = DemandForecaster()
