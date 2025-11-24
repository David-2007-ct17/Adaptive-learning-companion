#!/usr/bin/env python3
"""
Adaptive Learning Companion - Flask Web Application
"""

import os
import sys
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our components
from memory.memory_bank import EnhancedMemoryBank
from tools.learning_tools import LearningTools
from agents.planner_agent import PlannerAgent
from agents.explainer_agent import ExplainerAgent
from agents.quizmaster_agent import QuizmasterAgent

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

class WebLearningCompanion:
    """Web version of the learning companion"""
    
    def __init__(self):
        self.memory = EnhancedMemoryBank()
        self.tools = LearningTools()
        self.agents = {
            "planner": PlannerAgent(),
            "explainer": ExplainerAgent(),
            "quizmaster": QuizmasterAgent()
        }
        self.user_profile = {}
    
    def run_learning_session(self, topic: str, user_profile: dict = None):
        """Run a complete learning session for the web"""
        if user_profile:
            self.user_profile = user_profile
        
        session_data = {}
        
        # Step 1: Planning Phase
        planning_prompt = f"""
        Create a study plan for: {topic}
        Student level: {self.user_profile.get('level', 'beginner')}
        Timeline: {self.user_profile.get('timeline', 'flexible')}
        Learning style: {self.user_profile.get('style', 'mixed')}
        """
        session_data["study_plan"] = self.agents["planner"].run(planning_prompt)
        
        # Step 2: Learning Tools
        session_data["subtopics"] = self.tools.break_down_topic(topic)
        session_data["analogy"] = self.tools.generate_analogy(topic)
        session_data["time_estimate"] = self.tools.estimate_study_time(
            topic, self.user_profile.get('level', 'beginner')
        )
        
        # Step 3: Explanation Phase
        explanation_prompt = f"""
        Explain the topic: {topic}
        Target audience: {self.user_profile.get('level', 'beginner')} level
        Learning style: {self.user_profile.get('style', 'mixed')}
        """
        session_data["explanation"] = self.agents["explainer"].run(explanation_prompt)
        
        # Step 4: Quiz Phase
        quiz_prompt = f"Create a 3-question quiz about: {topic}"
        session_data["quiz"] = self.agents["quizmaster"].run(quiz_prompt)
        
        # Simulate quiz score for demo
        session_data["score"] = 85.0
        
        # Save to memory
        self.memory.add_session(topic, session_data, self.user_profile)
        self.memory.update_progress(topic, quiz_score=session_data.get("score", 0))
        
        return session_data

# Initialize the companion
companion = WebLearningCompanion()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/learn')
def learn():
    """Learning page"""
    return render_template('learn.html')

@app.route('/api/learning-session', methods=['POST'])
def api_learning_session():
    """API endpoint for learning sessions"""
    try:
        data = request.json
        topic = data.get('topic', '').strip()
        user_profile = data.get('profile', {})
        
        if not topic:
            return jsonify({
                'success': False,
                'error': 'Please enter a topic to learn about'
            })
        
        # Run learning session
        session_data = companion.run_learning_session(topic, user_profile)
        
        return jsonify({
            'success': True,
            'session_data': session_data,
            'topic': topic
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/api/quick-demo')
def api_quick_demo():
    """API endpoint for quick demo"""
    try:
        demo_topics = [
            "machine learning basics",
            "neural networks", 
            "python programming",
            "climate change science",
            "world history overview"
        ]
        
        import random
        topic = random.choice(demo_topics)
        
        # Run demo session with default profile
        session_data = companion.run_learning_session(topic, {
            'level': 'beginner',
            'timeline': '1 week', 
            'style': 'mixed'
        })
        
        return jsonify({
            'success': True,
            'topic': topic,
            'session_data': session_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Demo error: {str(e)}'
        }), 500

@app.route('/dashboard')
def dashboard():
    """Learning dashboard"""
    insights = companion.memory.get_learning_insights()
    return render_template('dashboard.html', insights=insights)

@app.route('/history')
def history():
    """Learning history page"""
    sessions = companion.memory.memory.get("sessions", [])[-10:]
    return render_template('history.html', sessions=sessions)

@app.route('/api/dashboard-data')
def api_dashboard_data():
    """API endpoint for dashboard data"""
    insights = companion.memory.get_learning_insights()
    return jsonify(insights)

# Health check endpoint for deployment
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'service': 'Adaptive Learning Companion',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Validate configuration
    try:
        from config import Config
        Config.validate_config()
        print("✅ Configuration validated successfully!")
    except Exception as e:
        print(f"⚠️  Configuration warning: {e}")
        print("💡 The app will run in demo mode with simulated responses")
    
    print("🚀 Starting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)