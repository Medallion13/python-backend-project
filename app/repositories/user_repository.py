from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.users import UserCreate


class UserRepository:
    """Repository for user-related database operations."""

    def create(self, db: Session, user_data: UserCreate) -> User:
        """
        Creates a new user in the database.

        Args:
            db (Session): The database session.
            user_data (UserCreate): The data for the new user.

        Returns:
            User: The created user object.
        """
        user = User(**user_data.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def get_by_id(self, db: Session, id: int) -> User | None:
        """
        Retrieves a user by their ID.

        Args:
            db (Session): The database session.
            id (int): The ID of the user to retrieve.

        Returns:
            User | None: The user object if found, otherwise None.
        """
        user = db.query(User).filter(User.id == id).first()

        return user

    def get_by_email(self, db: Session, email: str) -> User | None:
        """
        Retrieves a user by their email.

        Args:
            db (Session): The database session.
            email (str): The email of the user to retrieve.

        Returns:
            User | None: The user object if found, otherwise None.
        """
        user = db.query(User).filter(User.email == email).first()

        return user

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Retrieves a list of users with pagination.

        Args:
            db (Session): The database session.
            skip (int): The number of users to skip.
            limit (int): The maximum number of users to return.

        Returns:
            list[User]: A list of user objects.
        """
        users = db.query(User).offset(skip).limit(limit).all()

        return users

    def delete(self, db: Session, user_id: int) -> bool:
        """
        Deletes a user by their ID.

        Args:
            db (Session): The database session.
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the user was deleted, False otherwise.
        """
        user = self.get_by_id(db, user_id)

        if user:
            db.delete(user)
            db.commit()

            return True

        return False


user_repository = UserRepository()
