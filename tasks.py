from typing import Annotated, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import User, Task
from database import LocalSession
from auth import get_current_user

router = APIRouter(prefix="", tags=["tasks"])


class CreateTaskRequest(BaseModel):
    title: str
    description: str


# get db with context manager, so it closes itself if it encounters an exception or when the db is no longer being used
def get_db():
    with LocalSession() as db:
        yield db


# dependency injection, we inject the db connection to the endpoints that need it
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_user_from_db(user: Optional[dict], db: Session) -> User:
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not logged in")
    user_db = db.query(User).filter(User.id == user.get("id")).first()

    if not user_db:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="User not found in DB")

    return user_db


@router.get("/tasks")
async def get_user_tasks(user: user_dependency, db: db_dependency):
    user_db = get_user_from_db(user, db)

    return user_db.tasks


@router.post("/tasks")
async def add_user_task(
    user: user_dependency, db: db_dependency, create_task_request: CreateTaskRequest
):
    user_db = get_user_from_db(user, db)

    task_model = Task(
        title=create_task_request.title,
        description=create_task_request.description,
        user_id=user_db.id,
    )

    db.add(task_model)
    db.commit()


@router.patch("/tasks/{id}")
async def mark_completed_user_task(id: int, db: db_dependency):
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Task not found in DB")

    task.completed = True

    db.commit()
    db.refresh(task)

    return task
