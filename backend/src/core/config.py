"""
Application Configuration Module.

Centralizes all environment variables and system settings.
Follows the Principle of Single Responsibility by isolating config logic.
"""

import os
from pydantic import BaseModel, Field
from typing import Optional


class LLMConfig(BaseModel):
    """Settings for the Language Model provider."""
    model_name: str = Field(default="gpt-4-turbo")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048)
    api_key: Optional[str] = Field(default=None)
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.api_key is None:
            self.api_key = os.getenv("OPENAI_API_KEY")


class DatabaseConfig(BaseModel):
    """Settings for database connections."""
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    name: str = Field(default="supply_chain_db")
    user: str = Field(default="admin")
    password: Optional[str] = Field(default=None)
    
    def get_connection_string(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class LoggingConfig(BaseModel):
    """Settings for application logging."""
    level: str = Field(default="INFO")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    output_dir: str = Field(default="./logs")


class AppConfig(BaseModel):
    """Root configuration object aggregating all sub-configs."""
    llm: LLMConfig = Field(default_factory=LLMConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    # Operational Settings
    budget_limit: float = Field(default=10_000_000.0)
    safety_stock_target_service_level: float = Field(default=0.95)
    max_graph_recursion_limit: int = Field(default=50)


# Singleton instance for application-wide access
config = AppConfig()
