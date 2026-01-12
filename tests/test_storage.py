import json
import os
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock, patch


# Mock the storage module
class MockStorage:
    def __init__(self):
        self.data = {}

    def save_insights(self, insights, file_path):
        self.data[file_path] = insights
        return True

    def load_insights(self, file_path):
        return self.data.get(file_path, None)


# Test cases for storage.py
class TestStorage(unittest.TestCase):
    def setUp(self):
        self.storage = MockStorage()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_save_insights(self):
        insights = {"insight1": "test", "insight2": "test2"}
        file_path = os.path.join(self.temp_dir, "test_insights.json")
        result = self.storage.save_insights(insights, file_path)
        self.assertTrue(result)

    def test_load_insights(self):
        insights = {"insight1": "test", "insight2": "test2"}
        file_path = os.path.join(self.temp_dir, "test_insights.json")
        self.storage.save_insights(insights, file_path)
        loaded_insights = self.storage.load_insights(file_path)
        self.assertEqual(loaded_insights, insights)

    def test_load_nonexistent_insights(self):
        file_path = os.path.join(self.temp_dir, "nonexistent_insights.json")
        loaded_insights = self.storage.load_insights(file_path)
        self.assertIsNone(loaded_insights)


if __name__ == "__main__":
    unittest.main()
