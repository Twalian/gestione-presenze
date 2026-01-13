from datetime import datetime
from typing import List, Dict, Optional
from src.models import Course, Participant
from src.storage import StorageManager

class Manager:
    def __init__(self):
        self.storage = StorageManager()
        self.courses = self.storage.get_courses()
        self.participants = self.storage.get_participants()
        self.attendance = self.storage.get_attendance()

    def save_state(self):
        self.storage.save_courses(self.courses)
        self.storage.save_participants(self.participants)
        self.storage.save_attendance(self.attendance)

    # --- Course Logic ---
    def add_course(self, name: str, id: str):
        if any(c.id == id for c in self.courses):
            raise ValueError(f"Course with ID {id} already exists.")
        new_course = Course(id=id, name=name)
        self.courses.append(new_course)
        self.save_state()

    def remove_course(self, course: Course):
        self.courses.remove(course)
        # Check if we should remove attendance data for this course? 
        # For simplicity, keeping it clean:
        if course.id in self.attendance:
             del self.attendance[course.id]
        self.save_state()

    def update_course_status(self, course: Course, status: str):
        course.status = status
        self.save_state()

    # --- Participant Logic ---
    def add_participant(self, id: str, first_name: str, last_name: str):
        if any(p.id == id for p in self.participants):
            raise ValueError(f"Participant with ID {id} already exists.")
        new_participant = Participant(id=id, first_name=first_name, last_name=last_name)
        self.participants.append(new_participant)
        self.save_state()

    def enroll_participant(self, course: Course, participant: Participant):
        if participant.id not in course.participant_ids:
            course.participant_ids.append(participant.id)
            self.save_state()
        else:
            raise ValueError("Participant already enrolled in this course.")

    def unenroll_participant(self, course: Course, participant: Participant):
        if participant.id in course.participant_ids:
            course.participant_ids.remove(participant.id)
            
            if course.id in self.attendance:
                for date in self.attendance[course.id]:
                    if participant.id in self.attendance[course.id][date]:
                        del self.attendance[course.id][date][participant.id]
            
            is_enrolled_elsewhere = any(
                participant.id in c.participant_ids 
                for c in self.courses 
                if c.id != course.id
            )
            
            if not is_enrolled_elsewhere:
                self.participants.remove(participant)
            
            self.save_state()

    def get_course_participants(self, course: Course) -> List[Participant]:
        return [p for p in self.participants if p.id in course.participant_ids]

    # --- Attendance Logic ---
    def register_attendance(self, course: Course, date: str, attendance_dict: Dict[str, str]):
        # attendance_dict: participant_id -> status
        if course.id not in self.attendance:
            self.attendance[course.id] = {}
        
        self.attendance[course.id][date] = attendance_dict
        
        if date not in course.dates:
            course.dates.append(date)
            course.dates.sort()
        
        self.save_state()

    def get_attendance_for_course_date(self, course: Course, date: str) -> Dict[str, str]:
        return self.attendance.get(course.id, {}).get(date, {})

    def get_full_course_attendance(self, course: Course) -> Dict[str, Dict[str, str]]:
        # Returns date -> participant_id -> status
        return self.attendance.get(course.id, {})
