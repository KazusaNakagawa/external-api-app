"""sqlite3 database connection

This module contains the sqlite3 database connection.

DATABASE:
  1. instagram.db

TABLES:
  1. ig_hashtag_id

COLUMNS:
  1. id
  2. name
  3. ig_hashtag_id
  4. timestamp

"""

import os
import pytz
import sqlite3
from datetime import datetime

from src.utils.logger import Logger

logger = Logger().get_logger()

_DATA_DIR = "db/"


class Database:
    def __init__(self, db_name: str = None):
        """sqlite3 database connection."""
        self.db_name = db_name if db_name else "instagram.db"
        if not os.path.exists(f"{_DATA_DIR}/{self.db_name}"):
            self.connect()
            self.create_table()
        else:
            self.connect()

    def connect(self) -> None:
        """Connect to database."""
        self.conn = sqlite3.connect(os.path.join(_DATA_DIR, self.db_name))
        self.cur = self.conn.cursor()

    def create_table(self):
        """Create table."""
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ig_hashtag_id (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                ig_hashtag_id INTEGER NOT NULL UNIQUE,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def utc_to_jst(self) -> str:
        """Convert UTC to JST."""
        now_utc = datetime.utcnow()
        tokyo_tz = pytz.timezone("Asia/Tokyo")
        return now_utc.astimezone(tokyo_tz)

    def insert_ig_hashtag_id(self, name: str, ig_hashtag_id: str):
        """Insert ig_hashtag_id."""
        self.cur.execute(
            """
            INSERT INTO ig_hashtag_id (name, ig_hashtag_id, timestamp)
            VALUES (?, ?, ?)
            """,
            (name, ig_hashtag_id if ig_hashtag_id else None, self.utc_to_jst()),
        )
        self.conn.commit()

    def select_ig_hashtag_id(self, name: str) -> str:
        """Select ig_hashtag_id."""
        self.cur.execute(
            """
            SELECT ig_hashtag_id FROM ig_hashtag_id WHERE name = ?
            """,
            (name,),
        )
        ig_hashtag_id = self.cur.fetchone()
        return ig_hashtag_id[0] if ig_hashtag_id else None

    def close(self):
        """Close database connection."""
        self.cur.close()
        self.conn.close()
        logger.info("close database connection")
