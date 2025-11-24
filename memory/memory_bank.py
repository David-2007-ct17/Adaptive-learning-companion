import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class MemoryBank:
    """Simple file-based memory system"""
    
    def __init__(self, filename: str = "data/learning_memory.json"):
        self.filename = filename
        self._ensure_data_directory()
        self.memory = self._load_memory()
    
    def _ensure_data_directory(self):
        """Ensure the data directory exists"""
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
    
    def _load_memory(self) -> Dict:
        """Load memory from file"""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"sessions": [], "study_plans": {}, "progress": {}, "user_profiles": {}}
    
    def save(self):
        """Save memory to file"""
        with open(self.filename, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def add_session(self, user_input: str, agent_responses: Dict, user_profile: Dict = None):
        """Record a complete learning session"""
        session = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "responses": agent_responses,
            "user_profile": user_profile or {}
        }
        self.memory["sessions"].append(session)
        self.save()
    
    def save_study_plan(self, topic: str, plan: str):
        """Save a study plan for future reference"""
        self.memory["study_plans"][topic] = {
            "plan": plan,
            "created_at": datetime.now().isoformat(),
            "sessions_count": self.memory["study_plans"].get(topic, {}).get("sessions_count", 0) + 1
        }
        self.save()
    
    def get_user_progress(self, user_id: str = "default") -> Dict:
        """Get learning progress for a user"""
        return self.memory["progress"].get(user_id, {
            "started_at": datetime.now().isoformat(),
            "total_sessions": 0,
            "topics_covered": [],
            "average_score": 0.0
        })
    
    def update_progress(self, topic: str, quiz_score: Optional[float] = None, user_id: str = "default"):
        """Update learning progress for a topic and user"""
        if user_id not in self.memory["progress"]:
            self.memory["progress"][user_id] = {
                "started_at": datetime.now().isoformat(),
                "total_sessions": 0,
                "topics_covered": [],
                "quiz_scores": [],
                "average_score": 0.0,
                "last_session": None
            }
        
        progress = self.memory["progress"][user_id]
        progress["total_sessions"] += 1
        progress["last_session"] = datetime.now().isoformat()
        
        if topic not in progress["topics_covered"]:
            progress["topics_covered"].append(topic)
        
        if quiz_score is not None:
            progress["quiz_scores"].append(quiz_score)
            progress["average_score"] = sum(progress["quiz_scores"]) / len(progress["quiz_scores"])
        
        self.save()

class EnhancedMemoryBank(MemoryBank):
    """Enhanced memory with analytics and compaction"""
    
    def __init__(self, filename: str = "data/learning_memory.json", max_sessions: int = 100):
        super().__init__(filename)
        self.max_sessions = max_sessions
    
    def compact_memory(self):
        """Remove oldest sessions if we exceed maximum"""
        sessions = self.memory.get("sessions", [])
        if len(sessions) > self.max_sessions:
            # Keep only the most recent sessions
            self.memory["sessions"] = sessions[-self.max_sessions:]
            self.save()
    
    def get_learning_insights(self, user_id: str = "default") -> Dict:
        """Generate insights from learning history"""
        sessions = self.memory.get("sessions", [])
        user_progress = self.get_user_progress(user_id)
        
        if not sessions:
            return {"message": "No learning data yet. Start your first session!"}
        
        total_sessions = len(sessions)
        topics_covered = list(set(session["user_input"] for session in sessions))
        
        # Calculate session completion rate
        complete_sessions = 0
        for session in sessions:
            if all(key in session["responses"] for key in ["study_plan", "explanation", "quiz"]):
                complete_sessions += 1
        
        # Recent activity
        recent_sessions = sessions[-5:] if sessions else []
        recent_topics = [session["user_input"] for session in recent_sessions]
        
        return {
            "total_sessions": total_sessions,
            "topics_covered": len(topics_covered),
            "completion_rate": f"{(complete_sessions/total_sessions)*100:.1f}%",
            "average_quiz_score": f"{user_progress.get('average_score', 0):.1f}%",
            "recent_topics": recent_topics,
            "learning_streak": self._calculate_learning_streak(sessions),
            "first_session": sessions[0]["timestamp"][:10] if sessions else "Never"
        }
    
    def _calculate_learning_streak(self, sessions: List[Dict]) -> int:
        """Calculate consecutive days of learning"""
        if not sessions:
            return 0
        
        # Get unique days with sessions
        session_days = set()
        for session in sessions:
            session_date = session["timestamp"][:10]  # YYYY-MM-DD
            session_days.add(session_date)
        
        # Sort dates and calculate streak
        sorted_days = sorted(session_days, reverse=True)
        streak = 0
        current_date = datetime.now().date()
        
        for day_str in sorted_days:
            day_date = datetime.strptime(day_str, "%Y-%m-%d").date()
            if (current_date - day_date).days == streak:
                streak += 1
            else:
                break
        
        return streak