import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from prompts import SYSTEM_PROMPT

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

class FactCheckerAgent:

    def __init__(self):
        self.name = "Fact Checker Agent"

    def run(self, user_input):

        final_prompt = f"""
        {SYSTEM_PROMPT}

        User Statement:
        {user_input}
        """

        response = llm.invoke(final_prompt)

        return response.content