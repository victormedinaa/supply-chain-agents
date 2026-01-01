"""
Unit Tests for Utility Functions.
"""

import unittest
from datetime import datetime, timedelta
from backend.src.core.utils import (
    generate_hash, format_currency, calculate_lead_time,
    chunk_list, safe_divide, date_range, deep_merge,
    truncate_string, validate_sku_format, parse_location_string
)


class TestGenerateHash(unittest.TestCase):
    
    def test_same_input_same_hash(self):
        data = {"key": "value"}
        hash1 = generate_hash(data)
        hash2 = generate_hash(data)
        
        self.assertEqual(hash1, hash2)
    
    def test_different_input_different_hash(self):
        hash1 = generate_hash({"a": 1})
        hash2 = generate_hash({"a": 2})
        
        self.assertNotEqual(hash1, hash2)


class TestFormatCurrency(unittest.TestCase):
    
    def test_usd_format(self):
        result = format_currency(1234.56)
        self.assertEqual(result, "$1,234.56")
    
    def test_eur_format(self):
        result = format_currency(1000.00, "EUR")
        self.assertEqual(result, "€1,000.00")


class TestCalculateLeadTime(unittest.TestCase):
    
    def test_default_sea_route(self):
        result = calculate_lead_time("Shanghai", "Munich", "sea")
        self.assertGreater(result, 0)
    
    def test_air_faster_than_sea(self):
        air = calculate_lead_time("Asia", "Europe", "air")
        sea = calculate_lead_time("Asia", "Europe", "sea")
        self.assertLess(air, sea)


class TestChunkList(unittest.TestCase):
    
    def test_even_chunks(self):
        result = chunk_list([1, 2, 3, 4], 2)
        self.assertEqual(result, [[1, 2], [3, 4]])
    
    def test_uneven_chunks(self):
        result = chunk_list([1, 2, 3, 4, 5], 2)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[-1], [5])


class TestSafeDivide(unittest.TestCase):
    
    def test_normal_division(self):
        result = safe_divide(10, 2)
        self.assertEqual(result, 5.0)
    
    def test_zero_denominator_returns_default(self):
        result = safe_divide(10, 0)
        self.assertEqual(result, 0.0)
    
    def test_zero_denominator_custom_default(self):
        result = safe_divide(10, 0, default=-1.0)
        self.assertEqual(result, -1.0)


class TestDateRange(unittest.TestCase):
    
    def test_generates_correct_dates(self):
        start = datetime(2026, 1, 1)
        end = datetime(2026, 1, 3)
        
        result = date_range(start, end)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], start)
        self.assertEqual(result[-1], end)


class TestDeepMerge(unittest.TestCase):
    
    def test_shallow_merge(self):
        result = deep_merge({"a": 1}, {"b": 2})
        self.assertEqual(result, {"a": 1, "b": 2})
    
    def test_nested_merge(self):
        base = {"config": {"debug": False, "level": 1}}
        override = {"config": {"debug": True}}
        
        result = deep_merge(base, override)
        
        self.assertTrue(result["config"]["debug"])
        self.assertEqual(result["config"]["level"], 1)


class TestTruncateString(unittest.TestCase):
    
    def test_short_string_unchanged(self):
        result = truncate_string("Hello", 10)
        self.assertEqual(result, "Hello")
    
    def test_long_string_truncated(self):
        result = truncate_string("Hello World", 8)
        self.assertTrue(result.endswith("..."))
        self.assertEqual(len(result), 8)


class TestValidateSkuFormat(unittest.TestCase):
    
    def test_valid_sku(self):
        self.assertTrue(validate_sku_format("SKU-00001"))
    
    def test_invalid_prefix(self):
        self.assertFalse(validate_sku_format("PRD-00001"))
    
    def test_invalid_suffix(self):
        self.assertFalse(validate_sku_format("SKU-ABC"))


class TestParseLocationString(unittest.TestCase):
    
    def test_full_location(self):
        result = parse_location_string("Industrial Zone, Europe")
        self.assertEqual(result["area"], "Industrial Zone")
        self.assertEqual(result["region"], "Europe")
    
    def test_single_part(self):
        result = parse_location_string("Unknown")
        self.assertEqual(result["area"], "Unknown")


if __name__ == '__main__':
    unittest.main()
