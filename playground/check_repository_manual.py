# test_repository_manual.py (raíz del proyecto)
from app.db.session import SessionLocal
from app.repositories.user_repository import user_repository
from app.schemas.users import UserCreate

db = SessionLocal()

try:
    # Test 1: Crear usuario
    user_data = UserCreate(username="testuser", email="test@example.com", password="password123")
    user = user_repository.create(db, user_data)
    print(f"✅ Usuario creado: ID={user.id}, username={user.username}")

    # Test 2: Buscar por ID
    found = user_repository.get_by_id(db, user.id)
    print(f"✅ Usuario encontrado: {found.username}")

    # Test 3: Buscar por email
    found_email = user_repository.get_by_email(db, "test@example.com")
    print(f"✅ Usuario por email: {found_email.username}")

    # Test 4: Listar todos
    all_users = user_repository.get_all(db)
    print(f"✅ Total usuarios: {len(all_users)}")

    # Test 5: Eliminar
    deleted = user_repository.delete(db, user.id)
    print(f"✅ Usuario eliminado: {deleted}")

finally:
    db.close()
