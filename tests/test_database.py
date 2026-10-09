from app.database.connection import DATABASE_PATH
from app.database.models import initialize_database


initialize_database()

print()
print("=== DATABASE TEST ===")
print()

print("Database path:")
print(DATABASE_PATH)

if DATABASE_PATH.exists():
    print()
    print("DATABASE OK")
else:
    print()
    print("DATABASE FAILED")