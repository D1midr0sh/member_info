from fastapi import APIRouter, HTTPException
from sqlmodel import Session

from .models import User
from ..database import engine

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/")
def get_all_users():
    with Session(engine) as session:
        users = session.query(User).all()
        return users


@router.post("/")
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@router.post("/follow/{follower_id}")
def follow(follower_id: int, followed_id: int):
    with Session(engine) as session:
        following_user = session.query(User).filter(User.id == follower_id).first()
        if following_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        followed_user = session.query(User).filter(User.id == followed_id).first()
        if followed_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        followed_user.followers.append(following_user)
        session.add(followed_user)
        session.commit()
