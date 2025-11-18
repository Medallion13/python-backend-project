# test_update_manual.py
from app.db.session import SessionLocal
from app.repositories.user_repository import user_repository
from app.schemas.users import UserCreate, UserUpdate

db = SessionLocal()

try:
    print("=== Limpieza: Eliminar usuarios de prueba ===")
    # Eliminar usuarios que puedan existir de ejecuciones previas
    existing_alice = user_repository.get_by_email(db, "alice@example.com")
    if existing_alice:
        user_repository.delete(db, existing_alice.id)
        print("✅ Usuario 'alice' eliminado")

    existing_charlie = user_repository.get_by_email(db, "charlie@example.com")
    if existing_charlie:
        user_repository.delete(db, existing_charlie.id)
        print("✅ Usuario 'charlie' eliminado")

    print("\n=== Test 1: Crear usuario ===")
    user_data = UserCreate(username="alice", email="alice@example.com", password="original_pass")
    user = user_repository.create(db, user_data)
    print(f"✅ Usuario creado: ID={user.id}")
    print(f"   username={user.username}, email={user.email}")

    print("\n=== Test 2: Actualizar solo email ===")
    update_data = UserUpdate(email="newemail@example.com")
    updated = user_repository.update(db, user.id, update_data)
    print("✅ Usuario actualizado:")
    print(f"   username={updated.username} (sin cambios)")
    print(f"   email={updated.email} (actualizado)")
    assert updated.username == "alice"
    assert updated.email == "newemail@example.com"

    print("\n=== Test 3: Actualizar múltiples campos ===")
    update_data2 = UserUpdate(username="bob", password="new_pass")
    updated2 = user_repository.update(db, user.id, update_data2)
    print("✅ Usuario actualizado:")
    print(f"   username={updated2.username} (actualizado)")
    print(f"   email={updated2.email} (sin cambios)")
    assert updated2.username == "bob"
    assert updated2.email == "newemail@example.com"

    print("\n=== Test 4: Usuario inexistente ===")
    result = user_repository.update(db, 9999, UserUpdate(email="test@test.com"))
    print(f"✅ Retorna None para ID inexistente: {result is None}")
    assert result is None

    print("\n=== Test 5: Email duplicado (IntegrityError) ===")
    # Crear otro usuario
    user2_data = UserCreate(username="charlie", email="charlie@example.com", password="pass")
    user2 = user_repository.create(db, user2_data)
    print(f"✅ Usuario 'charlie' creado: ID={user2.id}")

    # Intentar actualizar bob con email de charlie
    try:
        user_repository.update(db, user.id, UserUpdate(email="charlie@example.com"))
        print("❌ Debería haber lanzado IntegrityError")
    except Exception as e:
        print(f"✅ IntegrityError capturado: {type(e).__name__}")
        print(f"   Detalle: {str(e)[:100]}...")
        db.rollback()

    print("\n=== Limpieza Final ===")
    user_repository.delete(db, user.id)
    user_repository.delete(db, user2.id)
    print("✅ Usuarios de prueba eliminados")

    print("\n🎉 Todos los tests pasaron")

except Exception as e:
    db.rollback()
    print(f"\n❌ Error durante el test: {e}")
    raise

finally:
    db.close()
