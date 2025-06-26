#!/usr/bin/env python3
"""
Professional Calculator App
A clean, professional calculator with real-time calculation and history management.

Entry point for the calculator application.
"""

import sys
import os
from calculator_app import CalculatorApp
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap


def load_calculator_icon():
    """Load calculator icon from Desktop."""
    # Use Calculator.png from Desktop without any scaling
    icon_path = os.path.expanduser("~/Desktop/Calculator.png")
    
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    else:
        # Fallback to default icon if file doesn't exist
        print(f"Calculator.png not found at {icon_path}, using default icon")
        return QIcon()  # Use default icon


def main():
    """Main entry point for the calculator application."""
    app = QApplication(sys.argv)
    
    # Set application properties for macOS dock visibility
    app.setApplicationName("Professional Calculator")
    app.setApplicationDisplayName("Professional Calculator")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Calculator App")
    
    # Set custom calculator icon
    calculator_icon = load_calculator_icon()
    app.setWindowIcon(calculator_icon)
    
    # Force app to appear in dock on macOS (simplified approach)
    import os
    if os.name == 'posix':  # macOS/Linux
        app.setQuitOnLastWindowClosed(True)
    
    # Create and show calculator window
    calculator = CalculatorApp()
    calculator.setWindowIcon(calculator_icon)  # Set icon on window too
    calculator.show()
    calculator.raise_()  # Bring to front
    calculator.activateWindow()  # Make active
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()