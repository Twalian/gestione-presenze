import json
import os
from typing import List, Dict, Any
from src.models import Course, Participant

DB_PATH = "db/presenze.db"

class StorageManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        if not os.path.exists(self.db_path):
            self.save_data({
                "courses": [],
                "participants": [],
                "attendance": {}
            })

    def load_data(self) -> Dict[str, Any]:
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"courses": [], "participants": [], "attendance": {}}

    def save_data(self, data: Dict[str, Any]):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=4)

    def get_courses(self) -> List[Course]:
        data = self.load_data()
        return [Course.from_dict(c) for c in data.get("courses", [])]

    def save_courses(self, courses: List[Course]):
        data = self.load_data()
        data["courses"] = [c.to_dict() for c in courses]
        self.save_data(data)

    def get_participants(self) -> List[Participant]:
        data = self.load_data()
        return [Participant.from_dict(p) for p in data.get("participants", [])]

    def save_participants(self, participants: List[Participant]):
        data = self.load_data()
        data["participants"] = [p.to_dict() for p in participants]
        self.save_data(data)

    # Attendance: course_id -> date -> participant_id -> status
    def get_attendance(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        data = self.load_data()
        return data.get("attendance", {})

    def save_attendance(self, attendance: Dict[str, Dict[str, Dict[str, str]]]):
        data = self.load_data()
        data["attendance"] = attendance
        self.save_data(data)
