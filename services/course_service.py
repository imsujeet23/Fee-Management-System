from database.database import Database


class CourseService:

    def __init__(self):
        self.db = Database()

    def course_exists(self, course_code):
        result = self.db.fetchone(
            "SELECT 1 FROM courses WHERE course_code = ?",
            (course_code,)
        )
        return result is not None

    def create_course(
        self,
        course_code,
        course_name,
        duration_months,
        total_semesters,
        annual_fee,
        status
    ):

        if self.course_exists(course_code):
            raise ValueError("Course code already exists.")

        self.db.execute(
            """
            INSERT INTO courses(
                course_code,
                course_name,
                duration_months,
                total_semesters,
                annual_fee,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                course_code,
                course_name,
                duration_months,
                total_semesters,
                annual_fee,
                status
            )
        )

    def get_all_courses(self):
        return self.db.fetchall(
            """
            SELECT *
            FROM courses
            ORDER BY course_name
            """
        )

    def delete_course(self, course_id):
        self.db.execute(
            "DELETE FROM courses WHERE course_id=?",
            (course_id,)
        )