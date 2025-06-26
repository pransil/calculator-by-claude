"""
Test Calculator Engine
Comprehensive tests for calculator engine functionality.
"""

import pytest
from src.calculator_engine import CalculatorEngine


class TestCalculatorEngine:
    """Test cases for CalculatorEngine class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.engine = CalculatorEngine()
    
    def test_basic_arithmetic(self):
        """Test basic arithmetic operations."""
        assert self.engine.evaluate_expression("2 + 3") == "5"
        assert self.engine.evaluate_expression("10 - 4") == "6"
        assert self.engine.evaluate_expression("6 * 7") == "42"
        assert self.engine.evaluate_expression("15 / 3") == "5"
    
    def test_decimal_operations(self):
        """Test operations with decimal numbers."""
        assert self.engine.evaluate_expression("2.5 + 1.5") == "4"
        assert self.engine.evaluate_expression("3.14 * 2") == "6.28"
        assert self.engine.evaluate_expression("10.5 / 2") == "5.25"
    
    def test_parentheses(self):
        """Test parentheses grouping."""
        assert self.engine.evaluate_expression("(2 + 3) * 4") == "20"
        assert self.engine.evaluate_expression("2 * (3 + 4)") == "14"
        assert self.engine.evaluate_expression("((2 + 3) * 4) / 2") == "10"
    
    def test_operator_precedence(self):
        """Test mathematical operator precedence."""
        assert self.engine.evaluate_expression("2 + 3 * 4") == "14"
        assert self.engine.evaluate_expression("20 - 6 / 2") == "17"
        assert self.engine.evaluate_expression("2 * 3 + 4 * 5") == "26"
    
    def test_negative_numbers(self):
        """Test negative number handling."""
        assert self.engine.evaluate_expression("-5") == "-5"
        assert self.engine.evaluate_expression("-2 + 3") == "1"
        assert self.engine.evaluate_expression("-(2 + 3)") == "-5"
    
    def test_division_by_zero(self):
        """Test division by zero handling."""
        assert self.engine.evaluate_expression("5 / 0") == "?"
        assert self.engine.evaluate_expression("10 / (2 - 2)") == "?"
    
    def test_invalid_expressions(self):
        """Test invalid expression handling."""
        assert self.engine.evaluate_expression("") == "?"
        assert self.engine.evaluate_expression("   ") == "?"
        assert self.engine.evaluate_expression("2 +") == "?"
        assert self.engine.evaluate_expression("* 3") == "?"
        assert self.engine.evaluate_expression("2 + + 3") == "?"
        assert self.engine.evaluate_expression("(2 + 3") == "?"
        assert self.engine.evaluate_expression("2 + 3)") == "?"
    
    def test_decimal_precision(self):
        """Test decimal precision limits."""
        result = self.engine.evaluate_expression("1 / 3")
        assert result == "0.33333333"  # 8 decimal places max
        
        result = self.engine.evaluate_expression("2 / 3")
        assert result == "0.66666667"  # 8 decimal places max, rounded
    
    def test_too_small_numbers(self):
        """Test very small number handling."""
        # Test number too small to represent (using division to create small number)
        result = self.engine.evaluate_expression("1 / 100000000000")  # 1e-11
        assert result == "Too Small"
    
    def test_valid_input_characters(self):
        """Test input character validation."""
        assert self.engine.is_valid_input_character('1') == True
        assert self.engine.is_valid_input_character('+') == True
        assert self.engine.is_valid_input_character('.') == True
        assert self.engine.is_valid_input_character('(') == True
        assert self.engine.is_valid_input_character(' ') == True
        
        assert self.engine.is_valid_input_character('a') == False
        assert self.engine.is_valid_input_character('=') == False
        assert self.engine.is_valid_input_character('$') == False
    
    def test_expression_validation(self):
        """Test expression validation."""
        assert self.engine.validate_expression("2 + 3") == True
        assert self.engine.validate_expression("(2 + 3) * 4") == True
        assert self.engine.validate_expression("") == False
        assert self.engine.validate_expression("   ") == False
        assert self.engine.validate_expression("2 + 3)") == False
        assert self.engine.validate_expression("(2 + 3") == False
    
    def test_number_formatting(self):
        """Test number input formatting."""
        # Test decimal point handling
        result = self.engine.format_number_input("2", ".")
        assert result == "2."
        
        result = self.engine.format_number_input("", ".")
        assert result == "0."
        
        result = self.engine.format_number_input("2.5", ".")
        assert result == "2.5"  # No change, already has decimal
        
        result = self.engine.format_number_input("2+", ".")
        assert result == "2+0."  # Add leading zero after operator
    
    def test_complex_expressions(self):
        """Test complex mathematical expressions."""
        assert self.engine.evaluate_expression("(2.5 + 1.5) * (3 - 1)") == "8"
        assert self.engine.evaluate_expression("100 / (2 * 5) + 3") == "13"
        assert self.engine.evaluate_expression("((10 - 5) * 2) / (1 + 1)") == "5"
    
    def test_whitespace_handling(self):
        """Test whitespace in expressions."""
        assert self.engine.evaluate_expression("2+3") == "5"
        assert self.engine.evaluate_expression("  2  +  3  ") == "5"
        assert self.engine.evaluate_expression("2 + 3") == "5"
    
    def test_implicit_multiplication(self):
        """Test implicit multiplication handling."""
        assert self.engine.evaluate_expression("2(3)") == "6"
        assert self.engine.evaluate_expression("(2)(3)") == "6"
        assert self.engine.evaluate_expression("2(3+4)") == "14"