#!/usr/bin/env python3
"""
Professional Calculator App
A clean, professional calculator with real-time calculation and history management.

Entry point for the calculator application.
"""

import sys
from calculator_app import CalculatorApp
from PyQt6.QtWidgets import QApplication


def main():
    """Main entry point for the calculator application."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Professional Calculator")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Calculator App")
    
    # Create and show calculator window
    calculator = CalculatorApp()
    calculator.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()