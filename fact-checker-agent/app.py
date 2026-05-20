from agent import FactCheckerAgent

agent = FactCheckerAgent()

user_input = input("Enter statement: ")

result = agent.run(user_input)

print("\n===== FACT CHECK RESULT =====\n")

print(result)