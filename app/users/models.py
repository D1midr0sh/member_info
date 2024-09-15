from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class HabitUserLink(SQLModel, table=True):
    habit_id: int | None = Field(default=None, foreign_key="habit.id", primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)


class Habit(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(default=None, nullable=False)

    users: list["User"] = Relationship(back_populates="habits", link_model=HabitUserLink)


class Role(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str | None = Field(default=None, nullable=False)
    permissions: str | None = Field(default=None, nullable=False)

    users: list["User"] = Relationship(back_populates="role")


class Follow(SQLModel, table=True):
    follower_id: int = Field(foreign_key="user.id", primary_key=True)
    followed_id: int = Field(foreign_key="user.id", primary_key=True)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str | None = Field(default=None, nullable=False)
    first_name: str | None = Field(default=None, nullable=False)
    last_name: str | None = Field(default=None, nullable=False)
    created_at: datetime | None = Field(default=datetime.now(), nullable=False)
    age: int | None = Field(default=None)

    following: list["User"] = Relationship(
        back_populates="followers",
        link_model=Follow,
        sa_relationship_kwargs=dict(
            primaryjoin="User.id == Follow.follower_id",
            secondaryjoin="User.id == Follow.followed_id",
        )
    )
    followers: list["User"] = Relationship(
        back_populates="following",
        link_model=Follow,
        sa_relationship_kwargs=dict(
            primaryjoin="User.id == Follow.followed_id",
            secondaryjoin="User.id == Follow.follower_id",
        )
    )

    role_id: int | None = Field(default=1, nullable=False, foreign_key="role.id")
    role: Role | None = Relationship(back_populates="users")

    habits: list[Habit] | None = Relationship(back_populates="users", link_model=HabitUserLink)
