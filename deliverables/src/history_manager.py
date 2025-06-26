"""
History Manager
Manages save/recall functionality with persistent storage.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional


class HistoryManager:
    """Manages calculation history with persistent storage."""
    
    def __init__(self, max_items: int = 10):
        """Initialize history manager."""
        self.max_items = max_items
        self.history_file = Path.home() / '.calculator_history.json'
        self.history_items: List[Dict[str, str]] = []
        self.load_history()
    
    def save_calculation(self, expression: str, result: str) -> None:
        """
        Save a calculation to history.
        Maintains maximum number of items by removing oldest.
        """
        # Create history item
        item = {
            'expression': expression,
            'result': result
        }
        
        # Add to beginning of list (most recent first)
        self.history_items.insert(0, item)
        
        # Maintain max items limit
        if len(self.history_items) > self.max_items:
            self.history_items = self.history_items[:self.max_items]
        
        # Save to file
        self._save_to_file()
    
    def get_history_items(self) -> List[Dict[str, str]]:
        """Get all history items (most recent first)."""
        return self.history_items.copy()
    
    def clear_history(self) -> None:
        """Clear all history items."""
        self.history_items.clear()
        self._save_to_file()
    
    def load_history(self) -> None:
        """Load history from persistent storage."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        # Validate items
                        valid_items = []
                        for item in data:
                            if (isinstance(item, dict) and 
                                'expression' in item and 'result' in item and
                                isinstance(item['expression'], str) and
                                isinstance(item['result'], str)):
                                valid_items.append(item)
                        
                        self.history_items = valid_items[:self.max_items]
        except (json.JSONDecodeError, IOError, OSError):
            # If file is corrupted or unreadable, start fresh
            self.history_items = []
    
    def _save_to_file(self) -> None:
        """Save current history to persistent storage."""
        try:
            # Ensure parent directory exists
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write history to file
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history_items, f, indent=2, ensure_ascii=False)
        except (IOError, OSError):
            # If we can't save, continue without persistent storage
            pass
    
    def format_history_display(self, item: Dict[str, str]) -> str:
        """Format history item for display in dropdown."""
        expression = item['expression']
        result = item['result']
        
        # Truncate long expressions for display
        max_expr_length = 30
        if len(expression) > max_expr_length:
            display_expr = expression[:max_expr_length - 3] + '...'
        else:
            display_expr = expression
        
        return f"{display_expr} = {result}"