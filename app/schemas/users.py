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

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """Model for updating existing user data."""

    username: str | None = None
    email: str | None = None
    password: str | None = None

    model_config = ConfigDict(extra="forbid")
