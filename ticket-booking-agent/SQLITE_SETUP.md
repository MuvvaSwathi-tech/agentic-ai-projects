# SQLite Setup Guide

## Overview
The ticket-booking-agent now uses **SQLite** for conversation memory storage instead of Redis. SQLite provides:
- **No external dependencies**: File-based database (no server needed)
- **Persistent storage**: All conversation history is saved automatically
- **Easy backup**: Simply copy the `.db` file
- **Multi-user support**: Multiple user conversations in a single database

## Installation

SQLite is built into Python, so **no additional installation is required**!

## Database Structure

### Tables

#### `users` table
Stores information about each conversation participant:
```sql
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### `messages` table
Stores all conversation messages:
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,          -- 'user' or 'assistant'
    content TEXT NOT NULL,       -- Message text
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
```

An index is created on `(user_id, id DESC)` for fast message retrieval.

## Usage

### Running the Agent

```bash
python app.py
```

The database file `conversation_memory.db` will be created automatically on first run.

### Available Commands

| Command | Description |
|---------|-------------|
| `exit` | Quit the agent |
| `clear` | Clear current user's conversation history |
| `history` | Show conversation summary |
| `users` | List all user conversations in database |
| `switch <user_id>` | Switch to a different user (e.g., `switch john_doe`) |

### Example Session

```
You: I want to book a flight from New York to Paris

Agent: I'd be happy to help you book a flight from New York to Paris. 
To find the best options, I need a few details:
1. What date would you like to depart?
2. Is this a one-way or round-trip flight?
3. Do you have any airline preferences?

You: switch alice
✓ Switched to user: alice

You: hello

Agent: Welcome! I'm your travel booking assistant. How can I help you today?
```

## Database File Management

### Location
Default: `conversation_memory.db` (in the same directory as `app.py`)

You can specify a custom location:
```python
# In agent.py or your code
agent = TravelBookingAgent(db_path="path/to/custom_location.db", user_id="user123")
```

### Backup
To backup conversations, simply copy the database file:
```bash
cp conversation_memory.db conversation_memory_backup.db
```

### Reset
To start fresh, delete the database file:
```bash
rm conversation_memory.db
```

Or clear only a specific user's history using the `clear` command in-app.

## Advantages over Redis

| Feature | SQLite | Redis |
|---------|--------|-------|
| Installation | Built-in | Requires server |
| Setup Time | Seconds | Minutes |
| Persistence | Automatic | Configurable |
| Scalability | File-based | In-memory + disk |
| Multi-machine | Via file sharing | Network-based |
| Query flexibility | SQL | Key-value |
| Backup | Simple copy | RDB/AOF |

## Querying the Database

You can inspect the database directly using the SQLite CLI:

```bash
# Open database
sqlite3 conversation_memory.db

# View users
sqlite> SELECT * FROM users;

# View all messages for a user
sqlite> SELECT * FROM messages WHERE user_id = 'default';

# Count messages
sqlite> SELECT COUNT(*) FROM messages;

# View last 5 messages
sqlite> SELECT role, content FROM messages ORDER BY id DESC LIMIT 5;

# Exit
sqlite> .exit
```

## Performance Considerations

- **Index optimization**: Messages are indexed by user_id and id for fast lookups
- **LIMIT clauses**: By default, only the last 12-20 messages are retrieved for context
- **Vacuum**: To optimize storage, periodically run:
  ```bash
  sqlite3 conversation_memory.db "VACUUM;"
  ```

## Troubleshooting

### Issue: "database is locked"
**Cause**: Multiple processes writing simultaneously
**Solution**: Ensure only one instance of the app is running per database file

### Issue: "no such table"
**Cause**: Database file corrupted or deleted
**Solution**: Delete the database file and restart the app to recreate it

### Issue: Very large database file
**Cause**: Many years of conversation history
**Solution**: Run `VACUUM` command or archive old conversations

## Migration from Redis

If you were using the Redis version, here's what changed:

1. **Remove Redis requirements** from requirements.txt
2. **Update imports**: Change from `RedisConversationMemory` to `SQLiteConversationMemory`
3. **Update initialization**: Instead of Redis connection parameters, use `db_path`
4. **No server needed**: No need to run Redis server anymore

Old code:
```python
from redis_memory import RedisConversationMemory
agent = TravelBookingAgent(redis_host="localhost", redis_port=6379)
```

New code:
```python
from sqlite_memory import SQLiteConversationMemory
agent = TravelBookingAgent(db_path="conversation_memory.db")
```
