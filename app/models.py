from pydantic import BaseModel, EmailStr


class Student(BaseModel):
    id: int
    name: str
    email: EmailStr


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
