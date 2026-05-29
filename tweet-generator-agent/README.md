# Tweet Generator Agent

## Overview
The Tweet Generator Agent is an AI-powered tool that creates engaging and creative tweets based on user-provided topics. It uses Google's Gemini AI model to analyze topics and generate professional, compelling tweets optimized for social media engagement.

## What It Does
This agent performs the following tasks:

1. **Analyzes Topics**: Takes user-provided topics as input
2. **Generates Tweets**: Uses advanced AI (Google Gemini 2.5 Flash) to create engaging tweets
3. **Ensures Quality**: Guarantees tweets are within character limits and professionally crafted
4. **Provides Explanations**: Includes a brief explanation for each generated tweet

## How It Works

### Components:
- **app.py**: Main entry point that handles user input and displays the generated tweet
- **agent.py**: Core agent class that generates tweets using Gemini AI
- **prompts.py**: Contains the system prompt that instructs the AI how to generate tweets

### Workflow:
1. User enters a topic via command line
2. The TweetGeneratorAgent processes the topic using Gemini AI
3. The AI generates a creative and engaging tweet
4. Results are displayed with the tweet text and explanation

## Setup & Usage

### Prerequisites:
- Python 3.8+
- Google Gemini API key

### Installation:
```bash
pip install -r requirements.txt
```

### Environment Configuration:
Create a `.env` file with your API key:
```
GEMINI_API_KEY=your_api_key_here
```

### Running the Agent:
```bash
python app.py
```

Then enter a topic to generate a tweet.

## Example

**Input:**
```
Enter topic for tweet: Artificial Intelligence
```

**Output:**
```
Text: 🤖 AI isn't replacing humanity—it's amplifying our potential. From healthcare to creativity, we're unlocking possibilities we only dreamed of. The future isn't about machines vs. humans; it's about humans + machines. Ready to build it together? #AI #Innovation

Explanation: This tweet highlights the positive impact of AI while addressing common concerns, making it engaging and thought-provoking for a tech-savvy audience.
```

## Model Used
- **Model**: Google Gemini 2.5 Flash (latest)
- **Temperature**: 0.3 (for consistent, reliable tweet generation)
