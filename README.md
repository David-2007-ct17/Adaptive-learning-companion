# Adaptive Learning Companion 

A multi-agent AI system that creates personalized learning experiences through sequential AI agents working together to plan, explain, and assess your learning journey.

## Features

- **Multi-Agent System**: Sequential workflow of specialized AI agents
- **Personalized Learning**: Adaptive study plans based on your level and goals
- **Interactive Quizzes**: Knowledge assessment with immediate feedback
- **Long-term Memory**: Progress tracking across learning sessions
- **Learning Analytics**: Insights and recommendations for improvement
- **Custom Tools**: Topic breakdown, analogies, and time estimation

## Architecture

├──Planner Agent → Creates study plans
├──Explainer Agent → Generates explanations
├── Quizmaster Agent → Creates assessments
├──Learning Tools → Enhances learning
└──Memory Bank → Tracks progress

## Prerequisites

- Python 3.12+
- Google Gemini API key

## API Setup

### Getting Your Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" → "Create API Key"
4. Copy the key and add it to your `.env` file:

```env
GEMINI_API_KEY=AIzaSyBIRWCH4VjEOYxGCaXldXO-VNk3w58mRpk
