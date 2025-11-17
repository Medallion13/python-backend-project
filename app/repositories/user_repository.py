from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.users import UserCreate, UserUpdate


class UserRepository:
    """Repository for user-related database operations."""

    def create(self, db: Session, user_data: UserCreate) -> User:
        """
        Creates a new user in the database.

        Args:
            db (Session): The database session.
            user_data (UserCreate): The data for the new user.

        Raises:
            sqlalchemy.exc.IntegrityError: If the user with the same email or username already exists.

        Returns:
            User: The created user object.

        Example:
            new_user_data = UserCreate(
                username="john_doe", email="john.doe@example.com", password="secretpassword"
            )
            created_user = user_repository.create(db_session, new_user_data)
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

        Example:
            user = user_repository.get_by_id(db_session, 1)
            if user:
                print(user.username)

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

        Example:
            user = user_repository.get_by_email(db_session, "john.doe@example.com")
            if user:
                print(user.id)

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

        Example:
            all_users = user_repository.get_all(db_session)
            paginated_users = user_repository.get_all(db_session, skip=10, limit=10)
        """
        users = db.query(User).offset(skip).limit(limit).all()

        return users

    def delete(self, db: Session, user_id: int) -> bool:
        """
        Deletes a user by their ID.

        Args:
            db (Session): The database session.
            user_id (int): The ID of the user to delete.

        Raises:
            sqlalchemy.exc.IntegrityError: If deleting the user violates a foreign key constraint.

        Returns:
            bool: True if the user was deleted, False otherwise.

        Example:
            was_deleted = user_repository.delete(db_session, 1)
            print(f"User deleted: {was_deleted}")
        """
        user = self.get_by_id(db, user_id)

        if user:
            db.delete(user)
            db.commit()

            return True

        return False

    def update(self, db: Session, user_id: int, user_data: UserUpdate) -> User | None:
        """ """
        user = self.get_by_id(db, user_id)
        if not user:
            return None

        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return user


user_repository = UserRepository()
