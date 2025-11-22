# services/manager.py
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from models.student import Student
import uuid

class StudentManager:
    def __init__(self, filepath: str = "data/students.json"):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self._write_json([])
        self.students: List[Student] = self._load_all()

    def _read_json(self) -> List[Dict[str, Any]]:
        with self.filepath.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, data: List[Dict[str, Any]]) -> None:
        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _load_all(self) -> List[Student]:
        data = self._read_json()
        return [Student.from_dict(d) for d in data]

    def save(self) -> None:
        data = [s.to_dict() for s in self.students]
        self._write_json(data)

    def list_students(self) -> List[Student]:
        return list(self.students)

    def _generate_id(self) -> str:
        return str(uuid.uuid4())[:8]

    def add_student(self, student_data: Dict[str, Any]) -> Student:
        # ensure id present
        if "id" not in student_data or not student_data["id"]:
            student_data["id"] = self._generate_id()
        student = Student.from_dict(student_data)
        student.validate()
        # check unique id
        if any(s.id == student.id for s in self.students):
            raise ValueError("Student with this id already exists.")
        self.students.append(student)
        self.save()
        return student

    def find_by_id(self, student_id: str) -> Optional[Student]:
        for s in self.students:
            if s.id == student_id:
                return s
        return None

    def update_student(self, student_id: str, updates: Dict[str, Any]) -> Student:
        s = self.find_by_id(student_id)
        if not s:
            raise ValueError("Student not found.")
        # apply updates
        for k, v in updates.items():
            if k == "age":
                v = int(v)
            if k == "gpa":
                v = float(v)
            if hasattr(s, k):
                setattr(s, k, v)
        s.validate()
        self.save()
        return s

    def delete_student(self, student_id: str) -> bool:
        before = len(self.students)
        self.students = [s for s in self.students if s.id != student_id]
        changed = len(self.students) != before
        if changed:
            self.save()
        return changed

    # Search & filter
    def search(self, query: str) -> List[Student]:
        q = query.strip().lower()
        if not q:
            return self.list_students()
        results = []
        for s in self.students:
            if q in s.id.lower() or q in s.name.lower() or q in s.grade.lower() or q in s.notes.lower():
                results.append(s)
        return results

    def filter(self, min_age: Optional[int]=None, max_age: Optional[int]=None,
               min_gpa: Optional[float]=None, max_gpa: Optional[float]=None, grade: Optional[str]=None) -> List[Student]:
        res = self.students
        if min_age is not None:
            res = [s for s in res if s.age >= min_age]
        if max_age is not None:
            res = [s for s in res if s.age <= max_age]
        if min_gpa is not None:
            res = [s for s in res if s.gpa >= min_gpa]
        if max_gpa is not None:
            res = [s for s in res if s.gpa <= max_gpa]
        if grade:
            g = grade.strip().lower()
            res = [s for s in res if s.grade.strip().lower() == g]
        return res
