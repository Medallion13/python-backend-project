from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.repositories.user_repository import user_repository
from app.schemas.users import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db_session)) -> UserResponse:
    """
    Creates a new user in the database.

    Args:
        user (UserCreate): Data for the user to be created.
        db (Session): The database session.

    Returns:
        UserResponse: The created user.

    Raises:
        HTTPException: If a user with the same email already exists (code 409).

    Example:
        POST /users/
        {
            "email": "newuser@example.com", "username": "newuser", "password": "a_strong_password"
        }
    """

    if user_repository.get_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already a user registered with that email address",
        )

    new_user = user_repository.create(db=db, user_data=user)

    return UserResponse.model_validate(new_user)


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)
) -> list[UserResponse]:
    """
    Retrieves a list of users.

    Args:
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        db (Session): The database session.

    Returns:
        list[UserResponse]: A list of users.

    Example:
        GET /users/

    Example (with pagination):
        GET /users/?skip=5&limit=10
    """
    users = user_repository.get_all(db, skip=skip, limit=limit)

    return [UserResponse.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db_session)) -> UserResponse:
    """
    Retrieves a user by their ID.

    Args:
        user_id (int): ID of the user to retrieve.
        db (Session): The database session.

    Returns:
        UserResponse: The requested user.

    Raises:
        HTTPException: If the user is not found (code 404).

    Example:
        GET /users/1
    """
    user = user_repository.get_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
def update_user(
    user_id: int, update_data: UserUpdate, db: Session = Depends(get_db_session)
) -> UserResponse:
    """
    Updates an existing user.

    Args:
        user_id (int): ID of the user to update.
        update_data (UserUpdate): Data to update the user with.
        db (Session): The database session.

    Returns:
        UserResponse: The updated user.

    Raises:
        HTTPException: If the user to be updated is not found (code 404).

    Example:
        PATCH /users/1
        {
            "username": "new_username"
        }
    """

    if user_repository.get_by_id(db, id=user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doesn't exist the user to update",
        )

    updated_user = user_repository.update(db, user_id=user_id, user_data=update_data)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found to update"
        )

    return UserResponse.model_validate(updated_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db_session)) -> None:
    """
    Deletes a user from the database.

    Args:
        user_id (int): ID of the user to delete.
        db (Session): The database session.

    Returns:
        None

    Raises:
        HTTPException: If the user to be deleted is not found (code 404).

    Example:
        DELETE /users/1
    """
    deleted = user_repository.delete(db, user_id=user_id)

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
