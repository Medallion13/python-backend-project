from pydantic import BaseModel


class UserBase(BaseModel):
    """Base model for user data."""

    username: str
    email: str


class UserCreate(UserBase):
    """Model for creating a new user."""

    password: str


class UserResponse(UserBase):
    """Model for user data response."""

    id: int


class UserInDB(UserResponse):
    """Model for user data stored in the database."""

    password: str
