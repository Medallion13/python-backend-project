from fastapi import FastAPI, HTTPException, status

from app.models import UserCreate, UserInDB, UserResponse

app = FastAPI()

# define the in-memory "database" to indicate that it is a list of UserInDB objects
db_users: list[UserInDB] = []


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> UserInDB:
    """
    Create a new User

    Args:
        user (UserCreate): The user data to create.

    Returns:
        UserResponse: The created user data.
    """
    # simulate auto-incrementing primary key
    user_id = len(db_users) + 1

    # create UserInDB instance
    new_user = UserInDB(
        id=user_id,
        username=user.username,
        email=user.email,
        password=user.password,
    )

    db_users.append(new_user)
    return new_user


@app.get("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int) -> UserInDB:
    """
    Get a user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        UserResponse: The user data.
        Httpexception: If the user is not found.
    """
    response_user = next((user for user in db_users if user.id == user_id), None)

    if not response_user:
        raise HTTPException(status_code=404, detail="User not found")

    return response_user
