from fastapi import HTTPException, status
from .models import Student, StudentCreate

students_db = [
    Student(id=1, name="Letícia Sayuri Imasato", email="leticia.sayuri@example.com")
]

next_id = 2


def get_all_students():
    return students_db


def get_student_by_id(student_id: int):
    for student in students_db:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")


def create_student_record(student: StudentCreate):
    for s in students_db:
        if s.email == student.email:
            raise HTTPException(
                status_code=400, detail="Already exists a student with this email."
            )

    new_id = max(s.id for s in students_db) + 1 if students_db else 1
    new_student = Student(id=new_id, name=student.name, email=student.email)
    students_db.append(new_student)
    return new_student
