from fastapi import FastAPI, status
from .crud import get_all_students, get_student_by_id, create_student_record
from .models import Student, StudentCreate

app = FastAPI(title="Student API")


@app.get("/students", response_model=list[Student])
def list_students():
    return get_all_students()


@app.get("/students/{student_id}", response_model=Student)
def search_student(student_id: int):
    return get_student_by_id(student_id)


@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    return create_student_record(student)
