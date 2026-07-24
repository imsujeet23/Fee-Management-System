from database.database import Database


class CourseController:

    def __init__(self):
        self.db = Database()

    def add_course(
        self,
        course_code,
        course_name,
        duration,
        total_semesters,
        annual_fee,
        status
    ):

        self.db.execute(
            """
            INSERT INTO courses(
                course_code,
                course_name,
                duration,
                total_semesters,
                annual_fee,
                status
            )

            VALUES(?,?,?,?,?,?)
            """,
            (
                course_code,
                course_name,
                duration,
                total_semesters,
                annual_fee,
                status
            )
        )

    def get_courses(self):

        return self.db.fetchall(
            """
            SELECT * FROM courses
            ORDER BY course_name
            """
        )

    def delete_course(self, course_id):

        self.db.execute(
            "DELETE FROM courses WHERE course_id=?",
            (course_id,)
        )