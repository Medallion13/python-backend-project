from fastapi import FastAPI, HTTPException, status

from app.api.routes import health
from app.schemas.users import UserCreate, UserInDB, UserResponse, UserUpdate

app = FastAPI(title="Python Backend Proyect", version="0.3.0")

# define the in-memory "database" to indicate that it is a list of UserInDB objects
db_users: list[UserInDB] = []

app.include_router(health.router, tags=["Health"])


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


@app.put("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, data: UserUpdate) -> UserInDB:
    """
    Update an existing user.

    Args:
        user_id (int): The ID of the user to update.
        user (UserUpdate): The user data to update.

    Returns:
        UserResponse: The updated user data.
        Httpexception: If the user is not found.

    """
    user_to_update = next((user for user in db_users if user.id == user_id), None)

    if not user_to_update:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user_to_update, key, value)

    return user_to_update


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int) -> None:
    """TODO"""
    user_to_delete = next((user for user in db_users if user.id == user_id), None)

    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")

    db_users.remove(user_to_delete)
