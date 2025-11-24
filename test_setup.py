#!/usr/bin/env python3
"""
Test script to verify Gemini 2.5 setup
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test if API key is loaded
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file")
    sys.exit(1)

print("✅ Gemini API Key loaded successfully!")
print(f"🔑 Key: {api_key[:10]}...{api_key[-5:]}")

# Test if we can import our config
try:
    from config import Config
    Config.validate_config()
    print("✅ Configuration validated successfully!")
except Exception as e:
    print(f"❌ Configuration error: {e}")
    sys.exit(1)

print("🎉 All setup tests passed! You're ready for Step 3.")