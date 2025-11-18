"""
    Script temporal para validar app/db/session.py
"""

from sqlalchemy import text

from app.db.session import engine, get_db_session

print("Test 1: Validando conexión a PostgreSQL...")
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 as test"))
        print(f"✅ Conexión exitosa: {result.fetchone()}")
except Exception as e:
    print(f"❌ Error de conexión: {e}")

# test 2
print("\nTest 2: Validando get_db_session()...")
try:
    db_gen = get_db_session()
    db = next(db_gen)
    print(f"✅ Sesión creada: {db}")

    result = db.execute(text("SELECT COUNT(*) FROM users"))
    print(f"✅ Query ejecutada: {result.fetchone()}")

    # Cerrar el generator (ejecuta finally)
    try:
        next(db_gen)
    except StopIteration:
        print("✅ Generator cerrado correctamente")
except Exception as e:
    print(f"❌ Error: {e}")
