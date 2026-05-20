from typing import TypedDict

class AgentState(TypedDict):
    user_input: str
    final_answer: str