import sqlite3
import json
from typing import List, Dict, Any
from datetime import datetime
import os

class SQLiteConversationMemory:
    """Manages conversation history using SQLite for persistent, file-based storage."""
    
    def __init__(self, db_path: str = "conversation_memory.db", user_id: str = "default"):
        """
        Initialize SQLite conversation memory.
        
        Args:
            db_path: Path to the SQLite database file (default: conversation_memory.db)
            user_id: Unique identifier for the user/conversation (default: "default")
        """
        self.db_path = db_path
        self.user_id = user_id
        self.connected = False
        
        try:
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            
            # Create tables if they don't exist
            self._initialize_db()
            
            self.connected = True
            print(f"✓ Connected to SQLite at {db_path}")
        except Exception as e:
            self.connected = False
            print(f"⚠ SQLite connection failed: {str(e)}")
            raise
    
    def _initialize_db(self) -> None:
        """Initialize database tables."""
        # Create users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create messages table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Create index for faster queries
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_messages 
            ON messages(user_id, id DESC)
        """)
        
        # Insert user if doesn't exist
        self.cursor.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (self.user_id,)
        )
        
        self.conn.commit()
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to SQLite conversation history.
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        if not self.connected:
            raise ConnectionError("Not connected to SQLite database")
        
        try:
            self.cursor.execute(
                """
                INSERT INTO messages (user_id, role, content, timestamp)
                VALUES (?, ?, ?, ?)
                """,
                (self.user_id, role, content, datetime.now().isoformat())
            )
            
            # Update last accessed time
            self.cursor.execute(
                "UPDATE users SET last_accessed = ? WHERE user_id = ?",
                (datetime.now().isoformat(), self.user_id)
            )
            
            self.conn.commit()
        except Exception as e:
            print(f"Error adding message: {str(e)}")
            raise
    
    def get_history(self) -> str:
        """Get formatted conversation history for context."""
        if not self.connected:
            return "No SQLite connection."
        
        try:
            # Get last 20 messages (10 turns)
            self.cursor.execute(
                """
                SELECT role, content FROM messages 
                WHERE user_id = ? 
                ORDER BY id DESC 
                LIMIT 20
                """,
                (self.user_id,)
            )
            
            rows = self.cursor.fetchall()
            
            if not rows:
                return "No previous conversation history."
            
            # Reverse to get chronological order
            messages = list(reversed(rows))
            formatted = "Previous Conversation History:\n"
            
            for msg in messages:
                role = msg['role'].capitalize()
                formatted += f"{role}: {msg['content']}\n"
            
            return formatted
        except Exception as e:
            print(f"Error retrieving history: {str(e)}")
            return "Error retrieving history."
    
    def get_messages_for_context(self, limit: int = 12) -> list:
        """
        Get recent messages for LLM context (as dicts, not formatted).
        
        Args:
            limit: Maximum number of messages to return
            
        Returns:
            List of message dictionaries
        """
        if not self.connected:
            return []
        
        try:
            self.cursor.execute(
                """
                SELECT role, content, timestamp FROM messages 
                WHERE user_id = ? 
                ORDER BY id DESC 
                LIMIT ?
                """,
                (self.user_id, limit)
            )
            
            rows = self.cursor.fetchall()
            
            # Reverse to get chronological order and convert to dicts
            messages = []
            for row in reversed(rows):
                messages.append({
                    "role": row['role'],
                    "content": row['content'],
                    "timestamp": row['timestamp']
                })
            
            return messages
        except Exception as e:
            print(f"Error retrieving messages for context: {str(e)}")
            return []
    
    def clear_history(self) -> None:
        """Clear all conversation history for current user."""
        if not self.connected:
            raise ConnectionError("Not connected to SQLite database")
        
        try:
            self.cursor.execute(
                "DELETE FROM messages WHERE user_id = ?",
                (self.user_id,)
            )
            self.conn.commit()
            print(f"Conversation history cleared for user: {self.user_id}")
        except Exception as e:
            print(f"Error clearing history: {str(e)}")
            raise
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of conversation from SQLite."""
        if not self.connected:
            return {"error": "Not connected to SQLite"}
        
        try:
            # Total messages
            self.cursor.execute(
                "SELECT COUNT(*) as count FROM messages WHERE user_id = ?",
                (self.user_id,)
            )
            total = self.cursor.fetchone()['count']
            
            # User messages
            self.cursor.execute(
                "SELECT COUNT(*) as count FROM messages WHERE user_id = ? AND role = 'user'",
                (self.user_id,)
            )
            user_msgs = self.cursor.fetchone()['count']
            
            # Assistant messages
            self.cursor.execute(
                "SELECT COUNT(*) as count FROM messages WHERE user_id = ? AND role = 'assistant'",
                (self.user_id,)
            )
            assistant_msgs = self.cursor.fetchone()['count']
            
            return {
                "total_messages": total,
                "user_messages": user_msgs,
                "assistant_messages": assistant_msgs,
                "storage": "SQLite",
                "user_id": self.user_id,
                "db_path": self.db_path
            }
        except Exception as e:
            print(f"Error getting summary: {str(e)}")
            return {"error": str(e)}
    
    def get_all_conversations(self) -> List[str]:
        """Get all user IDs with stored conversations."""
        if not self.connected:
            return []
        
        try:
            self.cursor.execute("""
                SELECT DISTINCT user_id FROM messages 
                ORDER BY user_id
            """)
            
            rows = self.cursor.fetchall()
            return [row['user_id'] for row in rows]
        except Exception as e:
            print(f"Error retrieving conversations: {str(e)}")
            return []
    
    def switch_user(self, user_id: str) -> None:
        """Switch to a different user's conversation."""
        self.user_id = user_id
        
        try:
            # Ensure user exists in database
            self.cursor.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
                (user_id,)
            )
            self.conn.commit()
            print(f"Switched to user: {user_id}")
        except Exception as e:
            print(f"Error switching user: {str(e)}")
            raise
    
    def close(self) -> None:
        """Close SQLite connection."""
        if self.connected:
            self.conn.close()
            self.connected = False
            print("SQLite connection closed.")
    
    def __del__(self):
        """Ensure connection is closed when object is destroyed."""
        if self.connected:
            self.close()
