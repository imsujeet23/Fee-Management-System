import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "fee_management.db"


class Database:
    def __init__(self, db_path: str | Path | None = None):
        """Open the application database (or an explicit database for tests)."""
        self.connection = sqlite3.connect(db_path or DB_PATH)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """)
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS courses(
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT UNIQUE NOT NULL,
    course_name TEXT NOT NULL,
    duration_months INTEGER NOT NULL,
    total_semesters INTEGER NOT NULL,
    annual_fee REAL NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('Active', 'Inactive')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            gender TEXT,
            dob TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            address TEXT,
            course TEXT,
            semester INTEGER,
            admission_date TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS fee_structure(
            fee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT NOT NULL,
            semester INTEGER NOT NULL,
            tuition_fee REAL DEFAULT 0,
            library_fee REAL DEFAULT 0,
            exam_fee REAL DEFAULT 0,
            miscellaneous_fee REAL DEFAULT 0,
            total_fee REAL DEFAULT 0
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments(
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            amount_paid REAL,
            payment_date TEXT,
            payment_method TEXT,
            receipt_number TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
        """)

        self.connection.commit()

    def execute(self, query, values=()):
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def fetchone(self, query, values=()):
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    def fetchall(self, query, values=()):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def get_connection(self):
        return self.connection

    def close(self):
        self.connection.close()
