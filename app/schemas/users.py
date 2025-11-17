from pydantic import BaseModel, ConfigDict


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


class UserUpdate(BaseModel):
    """Model for updating existing user data."""

    username: str | None
    email: str | None
    password: str | None

    model_config = ConfigDict(extra="forbid")
