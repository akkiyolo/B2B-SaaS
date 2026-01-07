from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import AuthUser, get_current_user, require_view,require_create,require_delete,require_edit
from app.models.task import Task
from app.schemas.task import TaskCreate,TaskResponse,TaskStatus,TaskStatusUpdate,TaskUpdate

router=APIRouter(prefix="/api/tasks",tags=["tasks"])

@router.get(path="",response_model=List[TaskResponse])
def list_task(user:AuthUser=Depends(require_view),db:Session=Depends(get_db)):
  tasks=db.query(Task).filter(Task.org_id==user.org_id).all()
  return tasks

@router.post(path="",response_model=TaskResponse)
def list_task(
  task_data:TaskCreate,
  user:AuthUser=Depends(require_create),db:Session=Depends(get_db)
  ):
  tasks=db.query(Task).filter(Task.org_id==user.org_id).all()
  return tasks
