"""
Unit Tests for Alert Management Service.
"""

import unittest
from datetime import datetime, timedelta
from backend.src.services.alert_manager import (
    AlertManager, Alert, AlertSeverity, AlertStatus
)


class TestAlertManager(unittest.TestCase):
    
    def setUp(self):
        self.manager = AlertManager()
    
    def test_create_alert_returns_alert_object(self):
        alert = self.manager.create_alert(
            title="Test Alert",
            description="This is a test",
            severity=AlertSeverity.WARNING,
            source_agent="UnitTest"
        )
        
        self.assertIsInstance(alert, Alert)
        self.assertEqual(alert.title, "Test Alert")
        self.assertEqual(alert.severity, AlertSeverity.WARNING)
        self.assertEqual(alert.status, AlertStatus.OPEN)
    
    def test_acknowledge_updates_status(self):
        alert = self.manager.create_alert(
            title="Ack Test",
            description="Testing acknowledgement",
            severity=AlertSeverity.INFO,
            source_agent="UnitTest"
        )
        
        result = self.manager.acknowledge(alert.id, "TestUser")
        
        self.assertTrue(result)
        self.assertEqual(alert.status, AlertStatus.ACKNOWLEDGED)
        self.assertEqual(alert.acknowledged_by, "TestUser")
    
    def test_resolve_updates_status(self):
        alert = self.manager.create_alert(
            title="Resolve Test",
            description="Testing resolution",
            severity=AlertSeverity.CRITICAL,
            source_agent="UnitTest"
        )
        
        result = self.manager.resolve(alert.id)
        
        self.assertTrue(result)
        self.assertEqual(alert.status, AlertStatus.RESOLVED)
    
    def test_get_open_alerts_excludes_resolved(self):
        alert1 = self.manager.create_alert(
            title="Open", description="", severity=AlertSeverity.INFO, source_agent="Test"
        )
        alert2 = self.manager.create_alert(
            title="Resolved", description="", severity=AlertSeverity.INFO, source_agent="Test"
        )
        self.manager.resolve(alert2.id)
        
        open_alerts = self.manager.get_open_alerts()
        
        self.assertIn(alert1, open_alerts)
        self.assertNotIn(alert2, open_alerts)
    
    def test_get_statistics_returns_counts(self):
        self.manager.create_alert(
            title="A1", description="", severity=AlertSeverity.INFO, source_agent="Test"
        )
        self.manager.create_alert(
            title="A2", description="", severity=AlertSeverity.WARNING, source_agent="Test"
        )
        
        stats = self.manager.get_statistics()
        
        self.assertEqual(stats["OPEN"], 2)
        self.assertEqual(stats["RESOLVED"], 0)


class TestAlertSeverity(unittest.TestCase):
    
    def test_severity_values_exist(self):
        self.assertEqual(AlertSeverity.INFO.value, "INFO")
        self.assertEqual(AlertSeverity.CRITICAL.value, "CRITICAL")
        self.assertEqual(AlertSeverity.EMERGENCY.value, "EMERGENCY")


if __name__ == '__main__':
    unittest.main()
