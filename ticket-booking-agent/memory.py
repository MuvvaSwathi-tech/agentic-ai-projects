import json
import os
from datetime import datetime
from typing import List, Dict, Any

class ConversationMemory:
    """Manages conversation history for the travel booking agent."""
    
    def __init__(self, memory_file: str = "conversation_history.json"):
        self.memory_file = memory_file
        self.conversation_history: List[Dict[str, str]] = []
        self.load_history()
    
    def load_history(self) -> None:
        """Load conversation history from file if it exists."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    self.conversation_history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.conversation_history = []
        else:
            self.conversation_history = []
    
    def save_history(self) -> None:
        """Save conversation history to file."""
        with open(self.memory_file, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to conversation history.
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.save_history()
    
    def get_history(self) -> str:
        """Get formatted conversation history for context."""
        if not self.conversation_history:
            return "No previous conversation history."
        
        formatted = "Previous Conversation History:\n"
        for msg in self.conversation_history[-10:]:  # Last 10 messages for context window
            role = msg['role'].capitalize()
            formatted += f"{role}: {msg['content']}\n"
        return formatted
    
    def clear_history(self) -> None:
        """Clear all conversation history."""
        self.conversation_history = []
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of conversation."""
        user_msgs = sum(1 for msg in self.conversation_history if msg['role'] == 'user')
        assistant_msgs = sum(1 for msg in self.conversation_history if msg['role'] == 'assistant')
        
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": user_msgs,
            "assistant_messages": assistant_msgs,
            "history_file": self.memory_file
        }
