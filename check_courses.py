import sqlite3

connection = sqlite3.connect("database/fee_management.db")
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

print("\n=== COURSES TABLE STRUCTURE ===")

cursor.execute("PRAGMA table_info(courses)")

for column in cursor.fetchall():
    print(dict(column))

print("\n=== COURSES DATA ===")

cursor.execute("SELECT * FROM courses")

courses = cursor.fetchall()

print("Number of courses:", len(courses))

for course in courses:
    print(dict(course))

connection.close()