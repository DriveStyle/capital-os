from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..schemas.goal import GoalCreate, GoalResponse
from ..services.goal_service import GoalService

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(goal_in: GoalCreate, db: Session = Depends(get_db)):
    return GoalService.create_goal(db, goal_in)


@router.get("/user/{user_id}", response_model=List[GoalResponse])
def list_user_goals(user_id: UUID, db: Session = Depends(get_db)):
    return GoalService.list_goals_by_user(db, user_id)
