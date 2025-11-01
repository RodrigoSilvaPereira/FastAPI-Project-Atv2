from fastapi import APIRouter, HTTPException
from app.services.db import get_all_students, get_student_by_id, create_student

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/")
async def list_students():
    return get_all_students()


@router.get("/{student_id}")
async def get_student(student_id: int):
    student = get_student_by_id(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/")
async def add_student(student: dict):
    if "name" not in student or "email" not in student:
        raise HTTPException(status_code=400, detail="Missing name or email")
    new_student = create_student(student["name"], student["email"])
    return new_student
