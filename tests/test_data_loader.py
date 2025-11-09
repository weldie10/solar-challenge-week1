"""
Unit tests for data_loader module.
"""

import unittest
from pathlib import Path
import sys

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from data_loader import get_data_path, load_solar_data, get_dataset_info


class TestDataLoader(unittest.TestCase):
    """Test cases for data loading functions."""
    
    def test_get_data_path(self):
        """Test getting data file path."""
        path = get_data_path('benin-malanville.csv')
        self.assertTrue(path.exists())
        self.assertTrue(path.suffix == '.csv')
    
    def test_get_dataset_info(self):
        """Test getting dataset information."""
        datasets = get_dataset_info()
        self.assertIsInstance(datasets, dict)
        self.assertGreater(len(datasets), 0)
    
    def test_load_solar_data(self):
        """Test loading solar data."""
        df = load_solar_data('benin-malanville.csv')
        self.assertIsNotNone(df)
        self.assertGreater(len(df), 0)
        self.assertGreater(len(df.columns), 0)


if __name__ == '__main__':
    unittest.main()

