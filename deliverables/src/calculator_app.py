"""
Calculator App
Main application window with UI components and event handling.
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QGridLayout, QPushButton, QLineEdit, QComboBox,
                            QLabel, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QKeySequence, QShortcut

from calculator_engine import CalculatorEngine
from history_manager import HistoryManager


class CalculatorApp(QMainWindow):
    """Main calculator application window."""
    
    def __init__(self):
        """Initialize the calculator application."""
        super().__init__()
        
        # Initialize core components
        self.engine = CalculatorEngine()
        self.history = HistoryManager()
        
        # UI state
        self.current_expression = ""
        self.cursor_position = 0
        
        # Setup UI
        self.init_ui()
        self.setup_keyboard_shortcuts()
        
        # Setup real-time calculation timer
        self.calc_timer = QTimer()
        self.calc_timer.setSingleShot(True)
        self.calc_timer.timeout.connect(self.update_result)
        
        # Initialize display
        self.reset_calculator()
    
    def init_ui(self):
        """Initialize user interface components."""
        self.setWindowTitle("Professional Calculator")
        self.setFixedSize(400, 600)  # Fixed size, non-resizable
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create input section
        self.create_input_section(main_layout)
        
        # Create button section
        self.create_button_section(main_layout)
    
    def create_input_section(self, parent_layout):
        """Create the input display section."""
        input_frame = QFrame()
        input_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        input_frame.setLineWidth(1)
        
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 10, 10, 10)
        
        # Input field (60 characters wide)
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Monaco", 14))  # Monospace font
        self.input_field.setMaxLength(60)
        self.input_field.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.input_field.textChanged.connect(self.on_input_changed)
        self.input_field.cursorPositionChanged.connect(self.on_cursor_changed)
        
        # Equals label
        equals_label = QLabel("=")
        equals_label.setFont(QFont("Monaco", 14))
        equals_label.setMinimumWidth(20)
        
        # Result field
        self.result_field = QLabel("0")
        self.result_field.setFont(QFont("Monaco", 14))
        self.result_field.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.result_field.setMinimumWidth(120)
        self.result_field.setStyleSheet("QLabel { color: #666; }")
        
        input_layout.addWidget(self.input_field, 1)
        input_layout.addWidget(equals_label)
        input_layout.addWidget(self.result_field)
        
        parent_layout.addWidget(input_frame)
    
    def create_button_section(self, parent_layout):
        """Create the button grid section."""
        button_frame = QFrame()
        button_layout = QGridLayout(button_frame)
        button_layout.setSpacing(5)
        
        # Button definitions (iPhone calculator style + Save/Recall)
        buttons = [
            # Row 0: Function buttons
            ('Clear', 0, 0, 1, 2, 'function'),
            ('Save', 0, 2, 1, 1, 'function'),
            ('Recall', 0, 3, 1, 1, 'function'),
            
            # Row 1: Operators
            ('(', 1, 0, 1, 1, 'operator'),
            (')', 1, 1, 1, 1, 'operator'),
            ('÷', 1, 2, 1, 1, 'operator'),
            ('×', 1, 3, 1, 1, 'operator'),
            
            # Row 2: Numbers and operators
            ('7', 2, 0, 1, 1, 'number'),
            ('8', 2, 1, 1, 1, 'number'),
            ('9', 2, 2, 1, 1, 'number'),
            ('-', 2, 3, 1, 1, 'operator'),
            
            # Row 3: Numbers and operators
            ('4', 3, 0, 1, 1, 'number'),
            ('5', 3, 1, 1, 1, 'number'),
            ('6', 3, 2, 1, 1, 'number'),
            ('+', 3, 3, 1, 1, 'operator'),
            
            # Row 4: Numbers and operators
            ('1', 4, 0, 1, 1, 'number'),
            ('2', 4, 1, 1, 1, 'number'),
            ('3', 4, 2, 1, 1, 'number'),
            ('=', 4, 3, 2, 1, 'operator'),  # Spans 2 rows
            
            # Row 5: Zero and decimal
            ('0', 5, 0, 1, 2, 'number'),  # Spans 2 columns
            ('.', 5, 2, 1, 1, 'number'),
        ]
        
        # Create buttons
        self.buttons = {}
        for button_info in buttons:
            text, row, col, row_span, col_span, button_type = button_info
            button = QPushButton(text)
            button.setMinimumHeight(60)
            button.setFont(QFont("Arial", 16))
            
            # Style buttons by type
            if button_type == 'number':
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        border: 1px solid #ccc;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                    QPushButton:pressed {
                        background-color: #d0d0d0;
                    }
                """)
            elif button_type == 'operator':
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #ff9500;
                        color: white;
                        border: 1px solid #e6860e;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #e6860e;
                    }
                    QPushButton:pressed {
                        background-color: #cc7a0d;
                    }
                """)
            elif button_type == 'function':
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #a6a6a6;
                        color: white;
                        border: 1px solid #8c8c8c;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #8c8c8c;
                    }
                    QPushButton:pressed {
                        background-color: #737373;
                    }
                """)
            
            # Connect button click
            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            
            button_layout.addWidget(button, row, col, row_span, col_span)
            self.buttons[text] = button
        
        parent_layout.addWidget(button_frame)
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for calculator operations."""
        # Allow typing in input field to work normally
        pass
    
    def on_button_click(self, button_text: str):
        """Handle button clicks."""
        if button_text == 'Clear':
            self.reset_calculator()
        elif button_text == 'Save':
            self.save_current_calculation()
        elif button_text == 'Recall':
            self.show_recall_menu()
        elif button_text == '=':
            # Do nothing special, result is already showing
            pass
        else:
            # Handle number/operator input
            char_to_insert = button_text
            
            # Convert display symbols to calculation symbols
            if button_text == '×':
                char_to_insert = '*'
            elif button_text == '÷':
                char_to_insert = '/'
            
            self.insert_character(char_to_insert)
    
    def insert_character(self, char: str):
        """Insert character at cursor position."""
        if not self.engine.is_valid_input_character(char):
            return
        
        current_text = self.input_field.text()
        cursor_pos = self.input_field.cursorPosition()
        
        # Handle decimal point formatting
        if char == '.':
            new_text = self.engine.format_number_input(current_text[:cursor_pos], char)
            if len(new_text) > len(current_text[:cursor_pos]):
                # Character was added
                new_text = new_text + current_text[cursor_pos:]
                self.input_field.setText(new_text)
                self.input_field.setCursorPosition(cursor_pos + len(new_text) - len(current_text))
        else:
            # Regular character insertion
            new_text = current_text[:cursor_pos] + char + current_text[cursor_pos:]
            self.input_field.setText(new_text)
            self.input_field.setCursorPosition(cursor_pos + 1)
    
    def on_input_changed(self):
        """Handle input field text changes."""
        # Trigger calculation with small delay for real-time feedback
        self.calc_timer.start(100)  # 100ms delay
    
    def on_cursor_changed(self):
        """Handle cursor position changes."""
        self.cursor_position = self.input_field.cursorPosition()
    
    def update_result(self):
        """Update the result display based on current input."""
        expression = self.input_field.text().strip()
        
        if not expression:
            self.result_field.setText("0")
            return
        
        result = self.engine.evaluate_expression(expression)
        self.result_field.setText(str(result))
    
    def reset_calculator(self):
        """Reset calculator to initial state."""
        self.input_field.clear()
        self.result_field.setText("0")
        self.input_field.setFocus()
    
    def save_current_calculation(self):
        """Save current calculation to history."""
        expression = self.input_field.text().strip()
        result = self.result_field.text()
        
        if expression and result != "0":
            self.history.save_calculation(expression, result)
    
    def show_recall_menu(self):
        """Show recall menu with saved calculations."""
        history_items = self.history.get_history_items()
        
        if not history_items:
            return
        
        # Create dropdown menu (simplified - using dialog for now)
        # In a full implementation, this would be a proper dropdown
        from PyQt6.QtWidgets import QInputDialog
        
        items = [self.history.format_history_display(item) for item in history_items]
        
        item, ok = QInputDialog.getItem(
            self, 'Recall Calculation', 'Select calculation:', items, 0, False
        )
        
        if ok and item:
            # Find selected history item
            selected_index = items.index(item)
            selected_item = history_items[selected_index]
            
            # Load expression into input field
            self.input_field.setText(selected_item['expression'])
            self.input_field.setFocus()
    
    def keyPressEvent(self, event):
        """Handle keyboard input."""
        key = event.key()
        text = event.text()
        
        # Allow standard editing keys
        if key in (Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Home, Qt.Key.Key_End,
                  Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            super().keyPressEvent(event)
            return
        
        # Handle character input
        if text and self.engine.is_valid_input_character(text):
            # Let the input field handle it naturally
            super().keyPressEvent(event)
        else:
            # Ignore invalid characters
            event.ignore()