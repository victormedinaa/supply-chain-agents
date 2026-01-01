"""
Alert Management Service.

Handles the creation, escalation, and lifecycle of operational alerts.
Implements a priority-based queue with escalation rules.
"""

from typing import List, Optional, Dict
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field
import uuid


class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"


class AlertStatus(str, Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"


class Alert(BaseModel):
    """Represents an operational alert in the system."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    severity: AlertSeverity
    status: AlertStatus = AlertStatus.OPEN
    source_agent: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    acknowledged_by: Optional[str] = None
    escalation_count: int = 0
    related_entity_id: Optional[str] = None
    metadata: Dict[str, str] = {}


class EscalationRule(BaseModel):
    """Defines when and how an alert should be escalated."""
    severity: AlertSeverity
    time_to_escalate_minutes: int
    escalate_to: str


class AlertManager:
    """
    Central service for managing alerts across the supply chain system.
    """
    
    def __init__(self):
        self._alerts: Dict[str, Alert] = {}
        self._escalation_rules: List[EscalationRule] = self._default_rules()
        
    def _default_rules(self) -> List[EscalationRule]:
        return [
            EscalationRule(severity=AlertSeverity.CRITICAL, time_to_escalate_minutes=15, escalate_to="Operations Manager"),
            EscalationRule(severity=AlertSeverity.EMERGENCY, time_to_escalate_minutes=5, escalate_to="VP Supply Chain"),
            EscalationRule(severity=AlertSeverity.WARNING, time_to_escalate_minutes=60, escalate_to="Shift Supervisor"),
        ]
    
    def create_alert(self, title: str, description: str, severity: AlertSeverity, source_agent: str, entity_id: Optional[str] = None) -> Alert:
        """Creates a new alert and adds it to the queue."""
        alert = Alert(
            title=title,
            description=description,
            severity=severity,
            source_agent=source_agent,
            related_entity_id=entity_id
        )
        self._alerts[alert.id] = alert
        return alert
    
    def acknowledge(self, alert_id: str, user: str) -> bool:
        """Marks an alert as acknowledged by a user."""
        if alert_id in self._alerts:
            alert = self._alerts[alert_id]
            alert.status = AlertStatus.ACKNOWLEDGED
            alert.acknowledged_by = user
            alert.updated_at = datetime.now()
            return True
        return False
    
    def resolve(self, alert_id: str) -> bool:
        """Marks an alert as resolved."""
        if alert_id in self._alerts:
            alert = self._alerts[alert_id]
            alert.status = AlertStatus.RESOLVED
            alert.updated_at = datetime.now()
            return True
        return False
    
    def get_open_alerts(self) -> List[Alert]:
        """Returns all alerts that are not yet resolved."""
        return [a for a in self._alerts.values() if a.status not in [AlertStatus.RESOLVED]]
    
    def get_by_severity(self, severity: AlertSeverity) -> List[Alert]:
        """Filters alerts by severity level."""
        return [a for a in self._alerts.values() if a.severity == severity]
    
    def check_escalations(self) -> List[Alert]:
        """
        Checks all open alerts against escalation rules and escalates if necessary.
        Returns a list of newly escalated alerts.
        """
        escalated = []
        now = datetime.now()
        
        for alert in self.get_open_alerts():
            for rule in self._escalation_rules:
                if alert.severity == rule.severity and alert.status == AlertStatus.OPEN:
                    age_minutes = (now - alert.created_at).total_seconds() / 60
                    if age_minutes >= rule.time_to_escalate_minutes:
                        alert.status = AlertStatus.ESCALATED
                        alert.escalation_count += 1
                        alert.metadata["escalated_to"] = rule.escalate_to
                        alert.updated_at = now
                        escalated.append(alert)
        
        return escalated
    
    def get_statistics(self) -> Dict[str, int]:
        """Returns a summary of alert counts by status."""
        stats = {status.value: 0 for status in AlertStatus}
        for alert in self._alerts.values():
            stats[alert.status.value] += 1
        return stats


# Singleton instance
alert_manager = AlertManager()
