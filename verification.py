from src.controllers import Manager
from src.storage import DB_PATH
import os

# Clean up before test
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

print("Starting verification...")
manager = Manager()

# 1. Add Course
print("Adding course...")
manager.add_course("Math 101", "MATH101")
assert len(manager.courses) == 1
assert manager.courses[0].name == "Math 101"

# 2. Add Participant
print("Adding participant...")
manager.add_participant("12345", "Mario", "Rossi")
assert len(manager.participants) == 1
assert manager.participants[0].first_name == "Mario"

# 3. Enroll
print("Enrolling...")
course = manager.courses[0]
participant = manager.participants[0]
manager.enroll_participant(course, participant)
assert "12345" in course.participant_ids

# 4. Attendance
print("Registering attendance...")
manager.register_attendance(course, "2023-10-27", {"12345": "present"})
attendance = manager.get_attendance_for_course_date(course, "2023-10-27")
assert attendance["12345"] == "present"

print("Verification SUCCESS!")
