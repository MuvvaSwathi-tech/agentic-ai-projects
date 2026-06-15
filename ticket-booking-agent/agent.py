import os
import json
from typing import Optional, Any, Dict
from datetime import datetime, timedelta
import random

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from prompts import SYSTEM_PROMPT
from sqlite_memory import SQLiteConversationMemory

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

# ============= BOOKING FUNCTIONS (unwrapped) =============

def search_flights_impl(origin: str, destination: str, date: str) -> Dict[str, Any]:
    """Search for available flights."""
    flights = [
        {"id": "FL001", "airline": "AeroLine", "departure": "08:00", "arrival": "11:30", "price": 250, "duration": "3h 30m"},
        {"id": "FL002", "airline": "SkyWings", "departure": "10:15", "arrival": "14:00", "price": 180, "duration": "3h 45m"},
        {"id": "FL003", "airline": "JetStar", "departure": "14:30", "arrival": "18:15", "price": 220, "duration": "3h 45m"},
        {"id": "FL004", "airline": "FastAir", "departure": "18:00", "arrival": "21:45", "price": 150, "duration": "3h 45m"},
    ]
    return {"found": len(flights), "flights": flights, "date": date, "route": f"{origin} -> {destination}"}

def search_trains_impl(origin: str, destination: str, date: str) -> Dict[str, Any]:
    """Search for available trains."""
    trains = [
        {"id": "TR001", "operator": "FastRail", "departure": "07:00", "arrival": "12:30", "price": 120, "duration": "5h 30m"},
        {"id": "TR002", "operator": "CityTrain", "departure": "09:45", "arrival": "15:15", "price": 95, "duration": "5h 30m"},
        {"id": "TR003", "operator": "ExpressRail", "departure": "16:00", "arrival": "21:30", "price": 110, "duration": "5h 30m"},
    ]
    return {"found": len(trains), "trains": trains, "date": date, "route": f"{origin} -> {destination}"}

def search_buses_impl(origin: str, destination: str, date: str) -> Dict[str, Any]:
    """Search for available buses."""
    buses = [
        {"id": "BU001", "operator": "BusMax", "departure": "06:00", "arrival": "14:30", "price": 45, "duration": "8h 30m"},
        {"id": "BU002", "operator": "ComfortBus", "departure": "09:00", "arrival": "17:30", "price": 55, "duration": "8h 30m"},
        {"id": "BU003", "operator": "QuickBus", "departure": "15:00", "arrival": "23:30", "price": 40, "duration": "8h 30m"},
    ]
    return {"found": len(buses), "buses": buses, "date": date, "route": f"{origin} -> {destination}"}

def book_ticket_impl(transport_type: str, ticket_id: str, passenger_name: str, email: str) -> Dict[str, Any]:
    """Book a ticket."""
    reference_number = f"BK{random.randint(100000, 999999)}"
    return {
        "success": True,
        "reference_number": reference_number,
        "ticket_id": ticket_id,
        "transport_type": transport_type,
        "passenger_name": passenger_name,
        "email": email,
        "booking_date": datetime.now().isoformat(),
        "confirmation_sent": f"Confirmation sent to {email}",
        "status": "CONFIRMED"
    }

def get_booking_status_impl(reference_number: str) -> Dict[str, Any]:
    """Get booking status."""
    return {
        "reference_number": reference_number,
        "status": "CONFIRMED",
        "booking_date": datetime.now().isoformat(),
        "payment_status": "Paid",
        "can_modify": True,
        "can_cancel": True
    }

# ============= WRAPPED TOOLS =============

@tool
def search_flights(origin: str, destination: str, date: str) -> Dict[str, Any]:
    """Search for available flights between two cities on a specific date."""
    return search_flights_impl(origin, destination, date)

@tool
def search_trains(origin: str, destination: str, date: str) -> Dict[str, Any]:
    """Search for available trains between two cities on a specific date."""
    return search_trains_impl(origin, destination, date)

@tool
def search_buses(origin: str, destination: str, date: str) -> Dict[str, Any]:
    """Search for available buses between two cities on a specific date."""
    return search_buses_impl(origin, destination, date)

@tool
def book_ticket(transport_type: str, ticket_id: str, passenger_name: str, email: str) -> Dict[str, Any]:
    """Book a ticket for a specific transport option."""
    return book_ticket_impl(transport_type, ticket_id, passenger_name, email)

@tool
def get_booking_status(reference_number: str) -> Dict[str, Any]:
    """Get the status of an existing booking."""
    return get_booking_status_impl(reference_number)

# ============= AGENT CLASS =============

class TravelBookingAgent:   
    def __init__(self, db_path: str = "conversation_memory.db", user_id: str = "default"):
        """Initialize the Travel Booking Agent with SQLite memory and tools."""
        self.name = "Travel Booking Agent"
        self.memory = SQLiteConversationMemory(
            db_path=db_path,
            user_id=user_id
        )
        
        # Define tools
        self.tools = [
            search_flights,
            search_trains,
            search_buses,
            book_ticket,
            get_booking_status
        ]
        
        # Tool mapping for direct function calls
        self.tool_map = {
            "search_flights": search_flights_impl,
            "search_trains": search_trains_impl,
            "search_buses": search_buses_impl,
            "book_ticket": book_ticket_impl,
            "get_booking_status": get_booking_status_impl
        }
    
    def run(self, user_input: str) -> str:
        """
        Process user input with tool usage for booking.
        
        Args:
            user_input: User's travel booking request
            
        Returns:
            Agent's response
        """
        # Add user message to memory
        self.memory.add_message("user", user_input)
        
        # Build message history for multi-turn conversation
        messages = self._build_message_history()
        
        try:
            # Bind tools to the LLM
            llm_with_tools = llm.bind_tools(self.tools)
            
            # Get response from LLM
            response = llm_with_tools.invoke(messages)
            
            # Check if LLM wants to call tools
            if response.tool_calls:
                # Process tool calls
                tool_results = []
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    
                    # Execute the tool
                    if tool_name in self.tool_map:
                        tool_result = self.tool_map[tool_name](**tool_args)
                        tool_results.append({
                            "tool": tool_name,
                            "result": tool_result
                        })
                
                # Build follow-up prompt with tool results
                messages.append(response)
                
                # Add tool results to messages
                for tool_result in tool_results:
                    messages.append(
                        ToolMessage(
                            content=json.dumps(tool_result["result"]),
                            tool_call_id=None,
                            name=tool_result["tool"]
                        )
                    )
                
                # Get final response after tool execution
                final_response = llm.invoke(messages)
                assistant_response = final_response.content
            else:
                # No tool calls, just use the response
                assistant_response = response.content
            
            # Add assistant response to memory
            self.memory.add_message("assistant", assistant_response)
            
            return assistant_response
            
        except Exception as e:
            error_msg = str(e)
            if "NOT_FOUND" in error_msg or "not found" in error_msg:
                print("\nNote: The specified model is not available. Using gemini-pro instead.")
                print("If you have access to gemini-2.5-pro, update the model parameter in agent.py\n")
            raise
    
    def _build_message_history(self) -> list:
        """Build message history including system prompt and conversation history."""
        messages = [SystemMessage(content=SYSTEM_PROMPT)]
        
        # Get last 6 conversation turns (12 messages) for context
        recent_messages = self.memory.get_messages_for_context(limit=12)
        
        for msg in recent_messages:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            else:
                messages.append(AIMessage(content=msg['content']))
        
        return messages
    
    def clear_memory(self) -> None:
        """Clear conversation history."""
        self.memory.clear_history()
    
    def get_memory_summary(self) -> dict:
        """Get summary of conversation memory."""
        return self.memory.get_summary()
    
    def get_conversation_history(self) -> str:
        """Get formatted conversation history."""
        return self.memory.get_history()
    
    def list_conversations(self) -> list:
        """List all conversations."""
        return self.memory.get_all_conversations()
    
    def switch_user(self, user_id: str) -> None:
        """Switch to a different user's conversation."""
        self.memory.switch_user(user_id)