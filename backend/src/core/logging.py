"""
Logging Configuration.

Sets up structured logging for the application.
Supports multiple output handlers (console, file).
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from backend.src.core.config import config


def setup_logger(name: str = "supply_chain") -> logging.Logger:
    """
    Configures and returns a logger instance.
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, config.logging.level, logging.INFO))
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(config.logging.format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File Handler
    log_dir = Path(config.logging.output_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(console_formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_agent_logger(agent_name: str) -> logging.Logger:
    """
    Returns a logger specifically namespaced for an agent.
    """
    return setup_logger(f"supply_chain.agents.{agent_name}")


def get_service_logger(service_name: str) -> logging.Logger:
    """
    Returns a logger specifically namespaced for a service.
    """
    return setup_logger(f"supply_chain.services.{service_name}")


# Default application logger
app_logger = setup_logger()
