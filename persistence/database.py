
import sqlite3
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

class Database:
    """
    A class to handle database operations using SQLite.
    Provides methods for connecting to the database, executing queries, and managing transactions.
    """

    def __init__(self, db_path: str = "wisdom_extractor.db"):
        """
        Initialize the database connection.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        """
        Context manager for handling database connections.
        Ensures the connection is closed after use.
        """
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = (), fetch: bool = False) -> Optional[List[Dict[str, Any]]]:
        """
        Execute a SQL query with optional parameters.

        Args:
            query (str): SQL query to execute.
            params (tuple): Parameters for the query.
            fetch (bool): Whether to fetch results.

        Returns:
            Optional[List[Dict[str, Any]]]: Fetched results if `fetch` is True, else None.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                columns = [column[0] for column in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return results
            conn.commit()

    def create_table(self, table_name: str, schema: str) -> None:
        """
        Create a table in the database.

        Args:
            table_name (str): Name of the table to create.
            schema (str): SQL schema for the table.
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
        self.execute_query(query)

    def insert_data(self, table_name: str, data: Dict[str, Any]) -> None:
        """
        Insert data into a table.

        Args:
            table_name (str): Name of the table.
            data (Dict[str, Any]): Data to insert.
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(data.values()))

    def fetch_data(self, table_name: str, condition: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Fetch data from a table based on a condition.

        Args:
            table_name (str): Name of the table.
            condition (str): SQL condition for filtering.
            params (tuple): Parameters for the condition.

        Returns:
            List[Dict[str, Any]]: Fetched data.
        """
        query = f"SELECT * FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        return self.execute_query(query, params, fetch=True)
