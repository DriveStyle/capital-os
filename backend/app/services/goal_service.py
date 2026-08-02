from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from ..models.goal import Goal
from ..schemas.goal import GoalCreate, GoalUpdate


class GoalService:
    @staticmethod
    def create_goal(db: Session, goal_in: GoalCreate) -> Goal:
        goal = Goal(
            title=goal_in.title,
            description=goal_in.description,
            target_amount=goal_in.target_amount,
            target_date=goal_in.target_date,
            user_id=goal_in.user_id,
        )
        db.add(goal)
        db.commit()
        db.refresh(goal)
        return goal

    @staticmethod
    def list_goals_by_user(db: Session, user_id: UUID) -> List[Goal]:
        return db.query(Goal).filter(Goal.user_id == user_id).all()
