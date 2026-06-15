from agent import TravelBookingAgent

def main():
    """Multi-turn conversation loop for travel booking agent with SQLite memory."""
    
    print("=" * 60)
    print("Welcome to the Travel Booking Agent!")
    print("Powered by SQLite for persistent, file-based storage")
    print("=" * 60)
    
    # Initialize with default user
    agent = TravelBookingAgent(user_id="default_user")
    
    print("\nI can help you book flights, trains, buses, and more.")
    print("\nCommands:")
    print("  exit       - Quit the agent")
    print("  clear      - Clear conversation history")
    print("  history    - Show conversation summary")
    print("  users      - List all conversations in database")
    print("  switch ID  - Switch to different user (e.g., 'switch user123')")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == "exit":
                print("\nThank you for using Travel Booking Agent. Goodbye!")
                break
            
            if user_input.lower() == "clear":
                agent.clear_memory()
                print("✓ Conversation history cleared.\n")
                continue
            
            if user_input.lower() == "history":
                summary = agent.get_memory_summary()
                print(f"\n📊 Conversation Summary:")
                print(f"   Storage: {summary.get('storage', 'N/A')}")
                print(f"   User ID: {summary.get('user_id', 'N/A')}")
                print(f"   Total Messages: {summary['total_messages']}")
                print(f"   User Messages: {summary['user_messages']}")
                print(f"   Agent Messages: {summary['assistant_messages']}\n")
                continue
            
            if user_input.lower() == "users":
                conversations = agent.list_conversations()
                if conversations:
                    print(f"\n Conversations stored in SQLite database:")
                    for conv_id in conversations:
                        print(f"   - {conv_id}")
                    print()
                else:
                    print("   (No conversations found)\n")
                continue
            
            if user_input.lower().startswith("switch "):
                new_user_id = user_input[7:].strip()
                if new_user_id:
                    agent.switch_user(new_user_id)
                    print(f"✓ Switched to user: {new_user_id}\n")
                else:
                    print("Usage: switch <user_id>\n")
                continue
            
            # Process as travel booking request
            print("\nAgent: ", end="", flush=True)
            response = agent.run(user_input)
            print(f"{response}\n")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f" Error: {str(e)}\n")

if __name__ == "__main__":
    main()