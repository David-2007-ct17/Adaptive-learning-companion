import google.generativeai as genai
import time
from typing import Optional
from config import Config

class RateLimiter:
    """Simple rate limiter to avoid API limits"""
    def __init__(self, calls_per_minute: int = Config.RATE_LIMIT_CALLS_PER_MINUTE):
        self.calls_per_minute = calls_per_minute
        self.call_times = []
    
    def wait_if_needed(self):
        """Wait if we're approaching rate limits"""
        now = time.time()
        # Remove calls older than 1 minute
        self.call_times = [t for t in self.call_times if now - t < 60]
        
        if len(self.call_times) >= self.calls_per_minute:
            sleep_time = 60 - (now - self.call_times[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.call_times.append(now)

class BaseAgent:
    """Base class for all learning agents"""
    
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.model = genai.GenerativeModel(Config.MODEL_NAME)
        self.rate_limiter = RateLimiter()
        self.max_retries = Config.MAX_RETRIES
    
    def run(self, prompt: str) -> str:
        """Execute the agent with retry logic"""
        full_prompt = f"{self.system_prompt}\n\nUser input: {prompt}"
        
        for attempt in range(self.max_retries):
            try:
                self.rate_limiter.wait_if_needed()
                response = self.model.generate_content(full_prompt)
                
                if response.text:
                    return response.text
                else:
                    raise ValueError("Empty response from model")
                    
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return f"I apologize, but I'm having trouble processing your request right now. Error: {str(e)}"
                
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return "I'm unable to process this request at the moment. Please try again later."