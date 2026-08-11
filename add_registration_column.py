import sqlite3

connection = sqlite3.connect("database/fee_management.db")

cursor = connection.cursor()

cursor.execute("""
    ALTER TABLE students
    ADD COLUMN registration_no TEXT
""")

connection.commit()
connection.close()

print("registration_no column added successfully.")