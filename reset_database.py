from pathlib import Path

from database.database import Database
from controllers.auth_controller import AuthController

db_path = Path("database/fee_management.db")

if db_path.exists():
    db_path.unlink()
    print("Old database deleted.")

db = Database()
db.create_tables()

auth = AuthController()
auth.create_default_admin()

print("New database created successfully.")
print("Default Login")
print("Username : admin")
print("Password : admin123")