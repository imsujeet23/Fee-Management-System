import bcrypt
from database.database import Database


class AuthController:

    def __init__(self):
        self.db = Database()

    def create_default_admin(self):

        user = self.db.fetchone(
            "SELECT * FROM users WHERE username=?",
            ("admin",)
        )

        if user:
            return

        password = bcrypt.hashpw(
            "admin123".encode(),
            bcrypt.gensalt()
        ).decode()

        self.db.execute(
            """
            INSERT INTO users(username,password,role)
            VALUES(?,?,?)
            """,
            ("admin", password, "Admin")
        )

    def login(self, username, password):

        user = self.db.fetchone(
            """
            SELECT * FROM users
            WHERE username=?
            """,
            (username,)
        )

        if not user:
            return False

        return bcrypt.checkpw(
            password.encode(),
            user["password"].encode()
        )