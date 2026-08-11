from database.database import Database


class StudentService:

    def __init__(self):
        self.db = Database()

    # -------------------------------------------------
    # Generate Student Registration Number
    # -------------------------------------------------

    def generate_registration_no(self):

        row = self.db.fetchone(
            "SELECT COUNT(*) AS total FROM students"
        )

        count = row["total"] + 1

        return f"STU{count:04d}"

    # -------------------------------------------------
    # Get Courses
    # -------------------------------------------------

    def get_courses(self):

        return self.db.fetchall(
        """
        SELECT course_id, course_name
        FROM courses
        WHERE status = 'Active'
        ORDER BY course_name
        """
    )

    # -------------------------------------------------
    # Get Students
    # -------------------------------------------------

    def get_students(self):

        return self.db.fetchall(
            """
            SELECT
                s.student_id,
                s.registration_no,
                s.first_name,
                s.last_name,
                c.course_name,
                s.semester,
                s.phone

            FROM students s

            JOIN courses c
            ON s.course_id = c.course_id

            ORDER BY s.registration_no
            """
        )

    # -------------------------------------------------
    # Create Student
    # -------------------------------------------------

    def create_student(
        self,
        registration_no,
        first_name,
        last_name,
        gender,
        dob,
        email,
        phone,
        address,
        course,
        semester,
        admission_date
    ):

        query = """
            INSERT INTO students (
                registration_no,
                first_name,
                last_name,
                gender,
                dob,
                email,
                phone,
                address,
                course,
                semester,
                admission_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        values = (
            registration_no,
            first_name,
            last_name,
            gender,
            dob,
            email,
            phone,
            address,
            course,
            semester,
            admission_date
        )

        self.db.execute(query, values)