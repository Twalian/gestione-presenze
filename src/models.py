from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Participant:
    id: str  # Matricola
    first_name: str
    last_name: str

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            first_name=data["first_name"],
            last_name=data["last_name"]
        )

@dataclass
class Course:
    id: str
    name: str
    participant_ids: List[str] = field(default_factory=list)
    status: str = "da iniziare"  # da iniziare, in corso, completato
    dates: List[str] = field(default_factory=list) # List of dates "YYYY-MM-DD"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "participant_ids": self.participant_ids,
            "status": self.status,
            "dates": self.dates
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            participant_ids=data.get("participant_ids", []),
            status=data.get("status", "da iniziare"),
            dates=data.get("dates", [])
        )
