import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import SYSTEM_PROMPT

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

class TweetGeneratorAgent:

    def __init__(self):
        self.name = "Tweet Generator Agent"

    def run(self, user_input):

        final_prompt = f"""
        {SYSTEM_PROMPT}

        Topic:
        {user_input}
        """

        try:
            response = llm.invoke(final_prompt)
            return response.content
        except Exception as e:
            error_msg = str(e)
            if "NOT_FOUND" in error_msg or "not found" in error_msg:
                print("\nNote: The specified model is not available. Using gemini-pro instead.")
                print("If you have access to gemini-1.5-pro, update the model parameter in agent.py\n")
            raise