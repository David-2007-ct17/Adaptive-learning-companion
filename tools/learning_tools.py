from agents.base_agent import BaseAgent

class LearningTools:
    """Custom tools for enhancing the learning experience"""
    
    def __init__(self):
        self.topic_analyzer = BaseAgent(
            "Topic Analyzer",
            "You break down complex topics into manageable subtopics. Return a clear list of 3-5 main subtopics."
        )
        
        self.analogy_creator = BaseAgent(
            "Analogy Creator",
            "You create simple, relatable analogies to explain complex concepts. Make them intuitive and memorable."
        )
        
        self.time_estimator = BaseAgent(
            "Time Estimator", 
            "You estimate realistic study times for learning topics. Consider different depth levels (basic, intermediate, comprehensive)."
        )
    
    def break_down_topic(self, topic: str) -> list:
        """Break down a complex topic into subtopics"""
        result = self.topic_analyzer.run(f"Break down this topic: {topic}")
        # Simple parsing - extract lines that look like list items
        lines = [line.strip('- ').strip() for line in result.split('\n') if line.strip()]
        return lines[:5]  # Return max 5 subtopics
    
    def generate_analogy(self, topic: str) -> str:
        """Generate a helpful analogy for understanding"""
        return self.analogy_creator.run(f"Create an analogy to explain: {topic}")
    
    def estimate_study_time(self, topic: str, level: str = "beginner") -> str:
        """Estimate required study time"""
        prompt = f"Estimate study time for a {level} to learn {topic}. Consider different depth levels."
        return self.time_estimator.run(prompt)