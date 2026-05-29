from agent import TweetGeneratorAgent

agent = TweetGeneratorAgent()

user_input = input("Enter topic for tweet: ")

result = agent.run(user_input)

print(result)