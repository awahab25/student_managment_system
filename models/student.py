# models/student.py
from dataclasses import dataclass, asdict
from typing import Dict, Any
import re

@dataclass
class Student:
    id: str            # unique id (string)
    name: str
    age: int
    grade: str         # e.g., "10" or "A" depending on system
    gpa: float         # performance metric (0.0 - 100.0 or 0.0 - 4.0 depending on your choice)
    notes: str = ""

    def validate(self) -> None:
        """Raise ValueError if any field is invalid."""
        if not self.id or not isinstance(self.id, str):
            raise ValueError("id must be a non-empty string.")
        if not self.name or not isinstance(self.name, str) or len(self.name.strip()) < 2:
            raise ValueError("name must be at least 2 characters.")
        if not isinstance(self.age, int) or not (3 <= self.age <= 120):
            raise ValueError("age must be an integer between 3 and 120.")
        if not isinstance(self.grade, str) or len(self.grade.strip()) == 0:
            raise ValueError("grade must be a non-empty string.")
        if not isinstance(self.gpa, (int, float)) or not (0.0 <= float(self.gpa) <= 100.0):
            # adjust bounds if you prefer GPA scale 0-4
            raise ValueError("gpa must be a number between 0 and 100.")
        if self.notes is not None and not isinstance(self.notes, str):
            raise ValueError("notes must be a string.")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Student":
        # minimal normalization
        d2 = dict(d)
        d2["age"] = int(d2["age"])
        d2["gpa"] = float(d2["gpa"])
        return Student(**d2)
