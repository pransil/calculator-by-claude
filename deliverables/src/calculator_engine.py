"""
Calculator Engine
Core calculation logic and expression parsing with safety and error handling.
"""

import ast
import operator
import re
from typing import Union, Optional


class CalculatorEngine:
    """Safe calculator engine with expression parsing and evaluation."""
    
    # Supported operators
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    def __init__(self):
        """Initialize calculator engine."""
        self.max_decimal_places = 8
        self.min_representable = 1e-8
    
    def is_valid_input_character(self, char: str) -> bool:
        """Check if character is allowed in calculator input."""
        allowed_chars = set('0123456789+-*/.() ')
        return char in allowed_chars
    
    def validate_expression(self, expression: str) -> bool:
        """
        Validate if expression contains only allowed characters and basic structure.
        Returns True if expression could potentially be valid.
        """
        if not expression or not expression.strip():
            return False
            
        # Check for allowed characters only
        for char in expression:
            if not self.is_valid_input_character(char):
                return False
        
        # Basic structure validation
        clean_expr = expression.strip()
        if not clean_expr:
            return False
            
        # Check for balanced parentheses
        paren_count = 0
        for char in clean_expr:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count < 0:
                    return False
        
        return paren_count == 0
    
    def evaluate_expression(self, expression: str) -> Union[float, str]:
        """
        Safely evaluate mathematical expression.
        Returns calculated result or error indicator.
        """
        if not expression or not expression.strip():
            return "?"
        
        # Clean and validate expression
        clean_expr = expression.strip()
        
        if not self.validate_expression(clean_expr):
            return "?"
        
        try:
            # Replace common issues
            clean_expr = self._preprocess_expression(clean_expr)
            # Parse expression into AST
            node = ast.parse(clean_expr, mode='eval')
            
            # Evaluate the AST safely
            result = self._evaluate_node(node.body)
            
            # Handle special cases
            if isinstance(result, (int, float)):
                if abs(result) < self.min_representable and result != 0:
                    return "Too Small"
                
                # Format result with max decimal places
                if isinstance(result, float):
                    # Remove trailing zeros, limit decimal places
                    formatted = f"{result:.{self.max_decimal_places}f}".rstrip('0').rstrip('.')
                    if '.' not in formatted and abs(result) < 1e15:
                        return str(int(result))
                    return formatted
                else:
                    return str(result)
            
            return str(result)
            
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError):
            return "?"
        except Exception:
            return "?"
    
    def _preprocess_expression(self, expression: str) -> str:
        """Preprocess expression to handle common formatting issues."""
        # Remove extra spaces
        clean = re.sub(r'\s+', '', expression)
        
        # Check for invalid operator sequences (e.g., "2 + + 3")
        if re.search(r'[+*/]{2,}', clean) or re.search(r'[-]{3,}', clean):
            raise ValueError("Invalid operator sequence")
        
        # Check for scientific notation and reject it for now
        if re.search(r'\d+[eE][+-]?\d+', clean):
            raise ValueError("Scientific notation not supported")
        
        # Handle implicit multiplication (e.g., 2(3+4) -> 2*(3+4))
        clean = re.sub(r'(\d)(\()', r'\1*\2', clean)
        clean = re.sub(r'(\))(\d)', r'\1*\2', clean)
        clean = re.sub(r'(\))(\()', r'\1*\2', clean)
        
        # Ensure proper decimal handling
        clean = re.sub(r'\.+', '.', clean)  # Multiple dots to single dot
        
        return clean
    
    def _evaluate_node(self, node) -> Union[int, float]:
        """Recursively evaluate AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):  # For older Python versions
            return node.n
        elif isinstance(node, ast.UnaryOp):
            operand = self._evaluate_node(node.operand)
            return self.OPERATORS[type(node.op)](operand)
        elif isinstance(node, ast.BinOp):
            left = self._evaluate_node(node.left)
            right = self._evaluate_node(node.right)
            
            # Handle division by zero
            if isinstance(node.op, ast.Div) and right == 0:
                raise ZeroDivisionError("Division by zero")
            
            return self.OPERATORS[type(node.op)](left, right)
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")
    
    def format_number_input(self, current_input: str, new_char: str) -> str:
        """
        Handle number input formatting including decimal points.
        Implements standard calculator decimal point behavior.
        """
        if new_char == '.':
            # Don't allow multiple decimal points in the same number
            # Find the current number being typed
            operators = '+-*/()'
            last_operator_pos = -1
            
            for i in range(len(current_input) - 1, -1, -1):
                if current_input[i] in operators:
                    last_operator_pos = i
                    break
            
            current_number = current_input[last_operator_pos + 1:]
            if '.' in current_number:
                return current_input  # Don't add another decimal point
            
            # Add leading zero if decimal point is first character of number
            if not current_number or current_number[-1] in operators:
                return current_input + '0.'
        
        return current_input + new_char