# Fact Checker Agent

## Overview
The Fact Checker Agent is an AI-powered tool that verifies the accuracy of statements and claims. It uses Google's Gemini AI model to analyze user input and determine whether claims are true, false, or partially true.

## What It Does
This agent performs the following tasks:

1. **Analyzes Statements**: Takes user-provided statements or claims as input
2. **Fact Verification**: Uses advanced AI (Google Gemini 2.5 Flash) to evaluate the truthfulness of the statement
3. **Provides Verdicts**: Returns one of three verdicts:
   - **TRUE**: The statement is factually accurate
   - **FALSE**: The statement is factually incorrect
   - **PARTIALLY TRUE**: The statement contains both true and false elements
4. **Explains Results**: Provides a clear explanation for each verdict

## How It Works

### Components:
- **app.py**: Main entry point that handles user input and displays results
- **agent.py**: Core agent class that processes statements using Gemini AI
- **prompts.py**: Contains the system prompt that instructs the AI how to fact-check
- **models.py**: Model configuration utilities
- **list_models.py**: Helper to list available AI models

### Workflow:
1. User enters a statement via command line
2. The FactCheckerAgent processes the statement using Gemini AI
3. The AI analyzes the claim and generates a verdict
4. Results are displayed with the verdict and explanation

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

Then enter any statement you want to fact-check.

## Example

**Input:**
```
The Earth is flat
```

**Output:**
```
Verdict: FALSE
Explanation: The Earth is a sphere (approximately). This has been scientifically proven through multiple methods including satellite imagery, physics, and direct observation.
```

## Model Used
- **Model**: Google Gemini 2.5 Flash (latest)
- **Temperature**: 0.3 (for consistent, reliable fact-checking)
