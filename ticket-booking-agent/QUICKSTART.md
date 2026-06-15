# Quick Start Guide - Ticket Booking Agent with SQLite

## 🚀 Get Started in 2 Minutes

### Step 1: Install Dependencies
```bash
cd ticket-booking-agent
pip install -r requirements.txt
```

### Step 2: Set Your API Key
Create a `.env` file in the `ticket-booking-agent` directory:
```
GEMINI_API_KEY=your-api-key-here
```

Get your free API key: https://aistudio.google.com/app/apikeys

### Step 3: Run the Agent
```bash
python app.py
```

### Step 4: Start Chatting!
```
You: I want to book a flight to Paris
Agent: I'd be happy to help you book a flight to Paris...
```

---

## 📝 Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| Any text | Ask for travel booking | `Book me a flight to NYC` |
| `exit` | Quit the app | `exit` |
| `clear` | Delete conversation history | `clear` |
| `history` | Show conversation stats | `history` |
| `users` | List all user conversations | `users` |
| `switch <id>` | Switch to different user | `switch alice` |

---

## 🎯 Example Session

```
You: I need a flight from London to Tokyo
Agent: Great! I can help you book a flight from London to Tokyo. 
To find the best options, I need a few details:
1. What date would you like to depart?
2. When would you like to return?
3. Do you have any airline preferences?

You: Depart May 15, return June 15, prefer ANA

Agent: Perfect! Here are some ANA flight options...

You: history
📊 Conversation Summary:
   Storage: SQLite
   User ID: default_user
   Total Messages: 4
   User Messages: 2
   Agent Messages: 2
```

---

## 📂 What Gets Stored

- **File**: `conversation_memory.db` (auto-created in app directory)
- **Size**: ~5-10KB per 100 messages
- **Backup**: Just copy the file!

---

## ✨ Key Features

✅ **No server setup** - SQLite is built-in to Python  
✅ **Automatic persistence** - All conversations saved  
✅ **Multi-user** - Different conversations per user  
✅ **Context-aware** - Agent remembers previous messages  
✅ **Easy backup** - Simple file copy  

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'langchain'"
```bash
# Install dependencies
pip install -r requirements.txt
```

### "Invalid API key"
- Check `.env` file exists in the directory
- Verify your API key from https://aistudio.google.com/app/apikeys

### "database is locked"
- Ensure only one instance of the app is running
- Close any other instances

---

## 📚 Documentation

- **[README.md](README.md)** - Full documentation and usage guide
- **[SQLITE_SETUP.md](SQLITE_SETUP.md)** - Database configuration and advanced features
- **[MIGRATION_REDIS_TO_SQLITE.md](MIGRATION_REDIS_TO_SQLITE.md)** - If upgrading from Redis

---

## 🎓 How It Works

```
Your Input
    ↓
Agent analyzes your request
    ↓
Retrieves conversation history from SQLite
    ↓
Generates response using Gemini AI
    ↓
Saves response to SQLite
    ↓
Returns answer to you
```

---

## 💡 Tips

1. **Clear history when switching users**: Each user has separate conversations
2. **Use specific requests**: "Book me a round-trip flight from NYC to London on May 15, returning May 22" works better than "Find flights"
3. **Review history**: Use `history` command to see conversation stats
4. **Export conversations**: Use `sqlite3 conversation_memory.db ".mode csv" "SELECT * FROM messages;" > export.csv`

---

## 🆘 Getting Help

### Check Documentation
1. Main guide: [README.md](README.md)
2. Database setup: [SQLITE_SETUP.md](SQLITE_SETUP.md)
3. Migration guide: [MIGRATION_REDIS_TO_SQLITE.md](MIGRATION_REDIS_TO_SQLITE.md)

### Verify Setup
```bash
# Check database created
ls -la conversation_memory.db

# Check messages stored
sqlite3 conversation_memory.db "SELECT COUNT(*) FROM messages;"

# View recent messages
sqlite3 conversation_memory.db "SELECT role, content FROM messages ORDER BY id DESC LIMIT 5;"
```

---

## 🎉 You're Ready!

```bash
python app.py
```

Enjoy using the Travel Booking Agent! 🚀

---

**Last Updated**: 2026-06-03  
**Storage Backend**: SQLite  
**Python Version**: 3.8+
