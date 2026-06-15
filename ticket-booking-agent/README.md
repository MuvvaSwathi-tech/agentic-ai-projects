# Travel Booking Agent - SQLite Edition

## Overview
An intelligent travel booking agent with **SQLite-backed conversation memory** for persistent, file-based storage with no server setup.

## Features
- 💾 **File-based Storage**: Conversations stored in SQLite (no server needed)
- 👥 **Multi-user Support**: Different conversations for different users
- 📊 **Persistent Storage**: Memories automatically saved and survive agent restarts
- 🔄 **Multi-turn Conversations**: Agent remembers context from previous messages
- 🤖 **Powered by Gemini 2.5-flash**: Advanced language understanding
- 📈 **Conversation Analytics**: View history, summaries, and statistics
- ⚡ **Zero Setup**: Works out of the box with Python's built-in SQLite

## Architecture

```
User Input
    ↓
Agent (LangChain + Gemini)
    ↓
SQLite Memory (stores conversation in conversation_memory.db)
    ↓
Response Generation with Context
```

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variable:**
   ```bash
   # Windows PowerShell
   $env:GEMINI_API_KEY = "your-api-key-here"
   
   # Or create .env file
   GEMINI_API_KEY=your-api-key-here
   ```

3. **That's it!** SQLite is built into Python - no additional setup needed.

## Usage

### Basic Usage
```bash
python app.py
```

Then type your travel booking requests:
```
You: I want to book a flight to New York
Agent: I can help you with that! Here are some options...

You: What about hotels near Central Park?
Agent: Based on your trip to New York, here are some hotels...
```

### Commands
- **exit** - Quit the agent
- **clear** - Delete conversation history
- **history** - Show conversation summary
- **users** - List all conversations in SQLite database
- **switch USER_ID** - Switch to different user's conversation

### Example Multi-user Session
```
You: switch alice
✓ Switched to user: alice

You: Book me a flight to London
Agent: Great! Here are flights to London...

You: switch bob
✓ Switched to user: bob

You: I need trains to Paris
Agent: I can help with train bookings to Paris...

You: users
👥 Conversations stored in SQLite database:
   - alice
   - bob

You: switch alice
✓ Switched to user: alice

You: history
📊 Conversation Summary:
   Storage: SQLite
   User ID: alice
   Total Messages: 4
   User Messages: 2
   Agent Messages: 2
   Database: conversation_memory.db
```

## File Structure

```
ticket-booking-agent/
├── app.py                      # Main entry point - conversation loop
├── agent.py                    # TravelBookingAgent class
├── sqlite_memory.py            # SQLiteConversationMemory class
├── prompts.py                  # System prompts for the agent
├── memory.py                   # Alternative JSON-based memory (optional)
├── conversation_memory.db      # SQLite database (auto-created)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── SQLITE_SETUP.md            # Detailed SQLite configuration guide
└── [Redis files - deprecated]
    ├── redis_memory.py        # (Deprecated - use sqlite_memory.py)
    ├── REDIS_SETUP.md         # (Deprecated)
    └── ...
```

## Database Details

See [SQLITE_SETUP.md](SQLITE_SETUP.md) for:
- Database schema and structure
- Backup and recovery procedures
- Direct database querying with SQLite CLI
- Performance optimization tips
- Migration from Redis

## Key Differences from Redis Version

| Aspect | SQLite | Redis (Old) |
|--------|--------|-----------|
| Setup | None needed | Server installation required |
| Data Format | File-based `.db` | In-memory + optional disk |
| Scalability | Good for 1-100k messages | Better for millions |
| Backup | Copy file | Export snapshots |
| Dependencies | None (built-in) | `redis-py` package |
| Learning Curve | SQL optional | Key-value patterns |

## Memory Management

### Conversation History
- Stores all messages automatically
- Retrieves last 12-20 messages for LLM context
- Timestamps all messages for tracking

### Supported Operations
- **Store**: User and assistant messages with timestamps
- **Retrieve**: Full history or recent messages for context
- **Clear**: Delete single user's conversation
- **Query**: SQL queries directly on database

## Troubleshooting

**Issue: Database locked error**
- Only run one instance of the app per database file
- Ensure the database file has read/write permissions

**Issue: Missing conversation history**
- Check if `conversation_memory.db` exists in the app directory
- Use `history` command to verify stored messages
- Check user ID matches when switching users

**Issue: Large database file**
- Run `sqlite3 conversation_memory.db "VACUUM;"` to optimize storage
- Archive old conversations by exporting specific users

## Requirements

```
langchain
langchain-google-genai
python-dotenv
```

No Redis or other external services required!

## Environment Setup

Create a `.env` file:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

Get your Gemini API key from: https://aistudio.google.com/app/apikeys

## Notes

- Each user's conversation is isolated in the database
- Database is created automatically on first run
- All timestamps use ISO 8601 format
- Messages are stored with role ('user' or 'assistant') and content

## Next Steps

- Explore [SQLITE_SETUP.md](SQLITE_SETUP.md) for advanced configurations
- Customize system prompts in [prompts.py](prompts.py)
- Extend agent capabilities by modifying [agent.py](agent.py)
