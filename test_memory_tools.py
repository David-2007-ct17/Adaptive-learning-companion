#!/usr/bin/env python3
"""
Test script to verify Memory System & Learning Tools
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_memory_system():
    """Test the memory system functionality"""
    print("🧠 Testing Memory System...")
    
    try:
        from memory.memory_bank import EnhancedMemoryBank
        
        # Create memory instance
        memory = EnhancedMemoryBank("data/test_memory.json")
        
        # Test adding a session
        test_session = {
            "study_plan": "Test plan",
            "explanation": "Test explanation", 
            "quiz": "Test quiz"
        }
        
        memory.add_session("test topic", test_session, {"level": "beginner"})
        memory.update_progress("test topic", 85.0)
        
        # Test insights
        insights = memory.get_learning_insights()
        
        print("✅ Memory System Tests:")
        print(f"   - Sessions: {insights.get('total_sessions', 0)}")
        print(f"   - Topics Covered: {insights.get('topics_covered', 0)}")
        print(f"   - Completion Rate: {insights.get('completion_rate', '0%')}")
        
        # Clean up test file
        if os.path.exists("data/test_memory.json"):
            os.remove("data/test_memory.json")
            
        return True
        
    except Exception as e:
        print(f"❌ Memory System Error: {e}")
        return False

def test_learning_tools():
    """Test the learning tools functionality"""
    print("🛠️ Testing Learning Tools...")
    
    try:
        from tools.learning_tools import LearningTools
        
        tools = LearningTools()
        
        # Test topic breakdown
        subtopics = tools.break_down_topic("machine learning")
        print("✅ Learning Tools Tests:")
        print(f"   - Topic Breakdown: {len(subtopics)} subtopics")
        
        # Test analogy generation
        analogy = tools.generate_analogy("neural networks")
        print(f"   - Analogy Generated: {len(analogy) > 0}")
        
        # Test time estimation
        time_est = tools.estimate_study_time("python programming", "beginner")
        print(f"   - Time Estimate: {len(time_est) > 0}")
        
        return True
        
    except Exception as e:
        print(f"❌ Learning Tools Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Step 3: Memory System & Learning Tools\n")
    
    # Test memory system
    memory_ok = test_memory_system()
    
    # Test learning tools  
    tools_ok = test_learning_tools()
    
    if memory_ok and tools_ok:
        print("\n🎉 All Step 3 tests passed! Ready for Step 4: Web Interface!")
    else:
        print("\n💥 Some tests failed. Please check the errors above.")
        sys.exit(1)