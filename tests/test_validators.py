"""Unit tests for utils.validators using only the Python standard library.

These tests verify that the validator functions enforce the required data constraints
and raise :class:`utils.exceptions.ValidationError` when invalid input is supplied.
"""

import unittest
import math

from utils.validators import (
    validate_identifier,
    validate_full_name,
    validate_birth_year,
    validate_number,
    validate_non_negative,
    validate_hours_worked,
)
from utils.exceptions import ValidationError


class TestValidators(unittest.TestCase):
    # ---------------------------------------------------------------------
    # Identifier validation
    # ---------------------------------------------------------------------
    def test_validate_identifier_success(self):
        self.assertEqual(validate_identifier("abc"), "ABC")
        self.assertEqual(validate_identifier("Nv001"), "NV001")

    def test_validate_identifier_errors(self):
        # Too short (<3)
        with self.assertRaises(ValidationError):
            validate_identifier("ab")
        # Too long (>10)
        with self.assertRaises(ValidationError):
            validate_identifier("ABCDEFGHIJK")
        # Contains whitespace
        with self.assertRaises(ValidationError):
            validate_identifier("NV 001")
        # Contains hyphen
        with self.assertRaises(ValidationError):
            validate_identifier("NV-001")

    # ---------------------------------------------------------------------
    # Full name validation
    # ---------------------------------------------------------------------
    def test_validate_full_name_success(self):
        self.assertEqual(validate_full_name("  Nguyễn   Văn  An "), "Nguyễn Văn An")
        self.assertEqual(validate_full_name("Lê Thị B"), "Lê Thị B")

    def test_validate_full_name_errors(self):
        # Empty string
        with self.assertRaises(ValidationError):
            validate_full_name("")
        # Only whitespace
        with self.assertRaises(ValidationError):
            validate_full_name("   ")
        # Single character
        with self.assertRaises(ValidationError):
            validate_full_name("A")
        # Contains digits
        with self.assertRaises(ValidationError):
            validate_full_name("An123")

    # ---------------------------------------------------------------------
    # Birth year validation
    # ---------------------------------------------------------------------
    def test_validate_birth_year_success(self):
        current_year = 2026  # Fixed for test reproducibility
        self.assertEqual(validate_birth_year(current_year - 18), current_year - 18)
        self.assertEqual(validate_birth_year(current_year - 65), current_year - 65)

    def test_validate_birth_year_errors(self):
        current_year = 2026
        # Too young (<18)
        with self.assertRaises(ValidationError):
            validate_birth_year(current_year - 17)
        # Too old (>65)
        with self.assertRaises(ValidationError):
            validate_birth_year(current_year - 66)
        # Wrong type: string
        with self.assertRaises(ValidationError):
            validate_birth_year("1990")
        # Wrong type: bool
        with self.assertRaises(ValidationError):
            validate_birth_year(True)

    # ---------------------------------------------------------------------
    # Generic number validation
    # ---------------------------------------------------------------------
    def test_validate_number_success_and_limits(self):
        self.assertEqual(validate_number(10, "Test", 0, 20), 10.0)
        self.assertEqual(validate_number(0, "Test", 0), 0.0)
        self.assertEqual(validate_number(20, "Test", 0, 20), 20.0)

    def test_validate_number_errors(self):
        # Bool is not a valid number
        with self.assertRaises(ValidationError):
            validate_number(True, "Test")
        # Cannot be cast to float
        with self.assertRaises(ValidationError):
            validate_number("abc", "Test")
        # NaN / Inf are not finite
        with self.assertRaises(ValidationError):
            validate_number(float('nan'), "Test")
        with self.assertRaises(ValidationError):
            validate_number(float('inf'), "Test")
        # Below minimum
        with self.assertRaises(ValidationError):
            validate_number(-1, "Test", 0)
        # Above maximum
        with self.assertRaises(ValidationError):
            validate_number(101, "Test", 0, 100)

    # ---------------------------------------------------------------------
    # Non‑negative validation (used for salaries, allowances, etc.)
    # ---------------------------------------------------------------------
    def test_validate_non_negative(self):
        self.assertEqual(validate_non_negative(0, "Lương"), 0.0)
        self.assertEqual(validate_non_negative(123.45, "Lương"), 123.45)
        with self.assertRaises(ValidationError):
            validate_non_negative(-5, "Lương")

    # ---------------------------------------------------------------------
    # Hours worked validation (0‑300 inclusive)
    # ---------------------------------------------------------------------
    def test_validate_hours_worked(self):
        self.assertEqual(validate_hours_worked(0), 0.0)
        self.assertEqual(validate_hours_worked(300), 300.0)
        with self.assertRaises(ValidationError):
            validate_hours_worked(301)
        with self.assertRaises(ValidationError):
            validate_hours_worked(-1)


if __name__ == "__main__":
    unittest.main()
