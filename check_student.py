import sqlite3

connection = sqlite3.connect("database/fee_management.db")
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

print("\n=== STUDENTS TABLE STRUCTURE ===")

cursor.execute("PRAGMA table_info(students)")

columns = cursor.fetchall()

for column in columns:
    print(dict(column))

print("\n=== EXISTING STUDENTS ===")

cursor.execute("SELECT * FROM students")

students = cursor.fetchall()

print("Number of students:", len(students))

for student in students:
    print(dict(student))

connection.close()