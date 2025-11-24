from .base_agent import BaseAgent

class QuizmasterAgent(BaseAgent):
    """Agent responsible for creating assessment quizzes"""
    
    def __init__(self):
        system_prompt = """You create effective learning quizzes that test understanding.
        
        Create a 5-question multiple choice quiz based on the provided study material.
        
        For each question, include:
        - A clear, unambiguous question
        - 4 plausible answer choices (A, B, C, D)
        - The correct answer clearly marked
        - A brief explanation of why it's correct
        
        Format requirements:
        1. Number each question clearly
        2. Format answers with A), B), C), D)
        3. After all questions, provide an answer key
        4. Ensure questions test different levels of understanding (recall, application, analysis)
        
        Make the quiz challenging but fair, covering the most important concepts."""
        
        super().__init__("Quiz Master", system_prompt)