#!/usr/bin/env python3
"""
Quick test to verify the fixes
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if we can import all modules"""
    print("Testing imports...")
    
    try:
        from memory.memory_bank import MemoryBank, EnhancedMemoryBank
        print("✅ Memory imports work")
        
        from tools.learning_tools import LearningTools
        print("✅ Tools imports work")
        
        from agents.base_agent import BaseAgent
        print("✅ Agent imports work")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_memory():
    """Test memory functionality"""
    print("\nTesting memory...")
    
    try:
        from memory.memory_bank import EnhancedMemoryBank
        
        memory = EnhancedMemoryBank("data/test_fix.json")
        memory.add_session("test topic", {"test": "data"})
        insights = memory.get_learning_insights()
        
        print(f"✅ Memory works - Sessions: {insights.get('total_sessions', 0)}")
        
        # Clean up
        if os.path.exists("data/test_fix.json"):
            os.remove("data/test_fix.json")
            
        return True
    except Exception as e:
        print(f"❌ Memory error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing fixes...\n")
    
    imports_ok = test_imports()
    memory_ok = test_memory()
    
    if imports_ok and memory_ok:
        print("\n🎉 All fixes working! Now run the original test:")
        print("python test_memory_tools.py")
    else:
        print("\n💥 Still having issues. Let me know the specific error.")