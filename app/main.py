from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Student API")

database = {
    1: {"id": 1, "name": "Letícia Sayuri Imasato"},
    2: {"id": 2, "name": "Renato Hioji Okamoto Odake"},
}


@app.get("/students/{student_id}")
def search_student(student_id: int):
    if student_id in database:
        return database[student_id]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
    )
