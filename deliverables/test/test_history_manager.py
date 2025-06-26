"""
Test History Manager
Tests for history management functionality.
"""

import pytest
import tempfile
import os
from pathlib import Path
from src.history_manager import HistoryManager


class TestHistoryManager:
    """Test cases for HistoryManager class."""
    
    def setup_method(self):
        """Setup test fixtures with temporary file."""
        # Create temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        
        # Create history manager with temporary file
        self.history = HistoryManager(max_items=3)  # Small limit for testing
        self.history.history_file = Path(self.temp_file.name)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_save_calculation(self):
        """Test saving calculations to history."""
        self.history.save_calculation("2 + 3", "5")
        items = self.history.get_history_items()
        
        assert len(items) == 1
        assert items[0]['expression'] == "2 + 3"
        assert items[0]['result'] == "5"
    
    def test_multiple_calculations(self):
        """Test saving multiple calculations."""
        self.history.save_calculation("2 + 3", "5")
        self.history.save_calculation("10 - 4", "6")
        self.history.save_calculation("6 * 7", "42")
        
        items = self.history.get_history_items()
        assert len(items) == 3
        
        # Most recent should be first
        assert items[0]['expression'] == "6 * 7"
        assert items[1]['expression'] == "10 - 4"
        assert items[2]['expression'] == "2 + 3"
    
    def test_max_items_limit(self):
        """Test maximum items limit enforcement."""
        # Add more items than the limit
        for i in range(5):
            self.history.save_calculation(f"{i} + 1", str(i + 1))
        
        items = self.history.get_history_items()
        assert len(items) == 3  # Should be limited to max_items
        
        # Should keep most recent items
        assert items[0]['expression'] == "4 + 1"
        assert items[1]['expression'] == "3 + 1"
        assert items[2]['expression'] == "2 + 1"
    
    def test_clear_history(self):
        """Test clearing all history."""
        self.history.save_calculation("2 + 3", "5")
        self.history.save_calculation("10 - 4", "6")
        
        assert len(self.history.get_history_items()) == 2
        
        self.history.clear_history()
        assert len(self.history.get_history_items()) == 0
    
    def test_persistent_storage(self):
        """Test saving and loading from file."""
        # Save some calculations
        self.history.save_calculation("2 + 3", "5")
        self.history.save_calculation("10 - 4", "6")
        
        # Create new history manager with same file
        new_history = HistoryManager(max_items=3)
        new_history.history_file = Path(self.temp_file.name)
        new_history.load_history()
        
        items = new_history.get_history_items()
        assert len(items) == 2
        assert items[0]['expression'] == "10 - 4"
        assert items[1]['expression'] == "2 + 3"
    
    def test_format_history_display(self):
        """Test history display formatting."""
        item = {'expression': '2 + 3', 'result': '5'}
        display = self.history.format_history_display(item)
        assert display == "2 + 3 = 5"
        
        # Test long expression truncation
        long_item = {
            'expression': '1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10',
            'result': '55'
        }
        display = self.history.format_history_display(long_item)
        assert len(display.split(' = ')[0]) <= 30
        assert display.endswith(' = 55')
    
    def test_invalid_file_handling(self):
        """Test handling of corrupted or invalid history files."""
        # Write invalid JSON to file
        with open(self.temp_file.name, 'w') as f:
            f.write("invalid json content")
        
        # Should handle gracefully
        new_history = HistoryManager()
        new_history.history_file = Path(self.temp_file.name)
        new_history.load_history()
        
        assert len(new_history.get_history_items()) == 0
    
    def test_empty_expressions(self):
        """Test handling of empty or invalid expressions."""
        self.history.save_calculation("", "?")
        self.history.save_calculation("2 + 3", "5")
        
        items = self.history.get_history_items()
        assert len(items) == 2
        assert items[0]['expression'] == "2 + 3"
        assert items[1]['expression'] == ""