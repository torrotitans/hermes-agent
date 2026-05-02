"""
FN:session_db.py
Session database manager for SQLite persistence in Torro CLI.

Classes:
- SessionDB: SQLite database manager for conversation history

Functions:
- FN:create_session: Create new session (lines 55-75)
- FN:add_message: Add message to session (lines 77-95)
- FN:get_session: Retrieve session data (lines 97-115)
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from pathlib import Path


# Default database path
DEFAULT_DB_PATH = Path.home() / ".torro" / "sessions.db"


@dataclass
class Session:
    """Session metadata."""
    session_id: str
    mode: str
    created_at: str
    updated_at: str
    message_count: int = 0


@dataclass
class Message:
    """Message stored in session."""
    id: int
    session_id: str
    role: str
    content: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None


class SessionDB:
    """
    SQLite database manager for conversation history persistence.
    Provides CRUD operations for sessions and messages.
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the session database.

        Args:
            db_path: Optional custom database path
        """
        self.db_path = db_path or str(DEFAULT_DB_PATH)
        self._ensure_directory()
        self._init_db()

    def _ensure_directory(self):
        """Ensure database directory exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    mode TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    message_count INTEGER DEFAULT 0
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_session
                ON messages(session_id)
            """)

            conn.commit()

    def create_session(
        self,
        session_id: str,
        mode: str
    ) -> Session:
        """
        FN:create_session Create a new session.

        Args:
            session_id: Unique session identifier
            mode: Session mode (plan, execute, etc.)

        Returns:
            Created Session object
        """
        now = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO sessions (session_id, mode, created_at, updated_at, message_count)
                VALUES (?, ?, ?, ?, 0)
                """,
                (session_id, mode, now, now)
            )
            conn.commit()

        return Session(
            session_id=session_id,
            mode=mode,
            created_at=now,
            updated_at=now,
            message_count=0
        )

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        FN:add_message Add a message to a session.

        Args:
            session_id: Session identifier
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional metadata dict

        Returns:
            Message ID
        """
        now = datetime.now().isoformat()
        metadata_json = json.dumps(metadata) if metadata else None

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO messages (session_id, role, content, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?)
                """,
                (session_id, role, content, now, metadata_json)
            )
            message_id = cursor.lastrowid

            # Update session message count and timestamp
            conn.execute(
                """
                UPDATE sessions
                SET message_count = message_count + 1,
                    updated_at = ?
                WHERE session_id = ?
                """,
                (now, session_id)
            )
            conn.commit()

        return message_id

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        FN:get_session Retrieve session by ID.

        Args:
            session_id: Session identifier

        Returns:
            Session object or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()

            if not row:
                return None

            return Session(
                session_id=row[0],
                mode=row[1],
                created_at=row[2],
                updated_at=row[3],
                message_count=row[4]
            )

    def get_messages(self, session_id: str) -> List[Message]:
        """
        FN:get_messages Retrieve all messages for a session.

        Args:
            session_id: Session identifier

        Returns:
            List of Message objects
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM messages WHERE session_id = ? ORDER BY id",
                (session_id,)
            )

            messages = []
            for row in cursor.fetchall():
                metadata = json.loads(row[5]) if row[5] else None
                messages.append(Message(
                    id=row[0],
                    session_id=row[1],
                    role=row[2],
                    content=row[3],
                    timestamp=row[4],
                    metadata=metadata
                ))

            return messages

    def list_sessions(self, limit: int = 10) -> List[Session]:
        """
        FN:list_sessions List recent sessions.

        Args:
            limit: Maximum number of sessions to return

        Returns:
            List of Session objects
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM sessions ORDER BY updated_at DESC LIMIT ?",
                (limit,)
            )

            sessions = []
            for row in cursor.fetchall():
                sessions.append(Session(
                    session_id=row[0],
                    mode=row[1],
                    created_at=row[2],
                    updated_at=row[3],
                    message_count=row[4]
                ))

            return sessions

    def delete_session(self, session_id: str):
        """
        FN:delete_session Delete a session and its messages.

        Args:
            session_id: Session identifier
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "DELETE FROM messages WHERE session_id = ?",
                (session_id,)
            )
            conn.execute(
                "DELETE FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            conn.commit()

    def close(self):
        """
        FN:close Close database connection.
        """
        # SQLite connections are context-managed, but this ensures cleanup
        pass
