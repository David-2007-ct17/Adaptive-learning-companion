#!/usr/bin/env python3
"""
Test script to verify the web application
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_web_imports():
    """Test if we can import all web components"""
    print("Testing web application imports...")
    
    try:
        # Test Flask app import
        from app import app, WebLearningCompanion
        print("✅ Flask app imports work")
        
        # Test companion initialization
        companion = WebLearningCompanion()
        print("✅ Web learning companion initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Web app import error: {e}")
        return False

def test_flask_routes():
    """Test basic Flask functionality"""
    print("\nTesting Flask routes...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Test home route
            response = client.get('/')
            assert response.status_code == 200
            print("✅ Home route works")
            
            # Test health check
            response = client.get('/health')
            assert response.status_code == 200
            print("✅ Health check works")
            
            # Test learn route
            response = client.get('/learn')
            assert response.status_code == 200
            print("✅ Learn route works")
            
            # Test dashboard route
            response = client.get('/dashboard')
            assert response.status_code == 200
            print("✅ Dashboard route works")
            
        return True
        
    except Exception as e:
        print(f"❌ Flask route error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Step 4: Web Application\n")
    
    imports_ok = test_web_imports()
    routes_ok = test_flask_routes()
    
    if imports_ok and routes_ok:
        print("\n🎉 Web application tests passed!")
        print("\n🚀 To run the web application:")
        print("   python app.py")
        print("\n🌐 Then open: http://localhost:5000")
    else:
        print("\n💥 Some web app tests failed.")
        sys.exit(1)