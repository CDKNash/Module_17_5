from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import *
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="User was not found")
    return task

@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="User was not found")
    db.execute(insert(Task).values(user_id=user_id,
                                   title=create_task.title,
                                   content=create_task.content,
                                   priority=create_task.priority,
                                   slug=slugify(create_task.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], user_id: int, update_task: UpdateTask):
    user = db.scalar(select(Task).where(Task.id == user_id))
    if user is None:
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
    else:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User was not found")

    db.execute(update(Task).where(Task.id == user_id).values(
                                                            title=update_task.title,
                                                            content=update_task.content,
                                                            priority=update_task.priority,
                                                            slug=slugify(update_task.title)))
    db.commit()

@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail="User was not found")
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}