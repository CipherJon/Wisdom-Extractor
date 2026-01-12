import json
import os
import pickle
from typing import Any, Dict, List, Optional


class StorageManager:
    """
    A utility class for handling file-based persistence operations.
    Supports JSON and pickle serialization for storing and retrieving data.
    """

    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str) -> None:
        """
        Save data to a JSON file.

        Args:
            data: The data to be saved.
            file_path: Path to the JSON file.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """
        Load data from a JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            The loaded data as a dictionary.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file is not valid JSON.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save_pickle(data: Any, file_path: str) -> None:
        """
        Save data to a pickle file.

        Args:
            data: The data to be saved.
            file_path: Path to the pickle file.
        """
        with open(file_path, "wb") as f:
            pickle.dump(data, f)

    @staticmethod
    def load_pickle(file_path: str) -> Any:
        """
        Load data from a pickle file.

        Args:
            file_path: Path to the pickle file.

        Returns:
            The loaded data.

        Raises:
            FileNotFoundError: If the file does not exist.
            pickle.PickleError: If the file is not valid pickle.
        """
        with open(file_path, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def save_csv(data: List[Dict[str, Any]], file_path: str) -> None:
        """
        Save a list of dictionaries to a CSV file.

        Args:
            data: List of dictionaries where keys are column headers.
            file_path: Path to the CSV file.
        """
        if not data:
            return

        import csv

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def ensure_directory_exists(directory_path: str) -> None:
        """
        Ensure that a directory exists. If not, create it.

        Args:
            directory_path: Path to the directory.
        """
        os.makedirs(directory_path, exist_ok=True)
