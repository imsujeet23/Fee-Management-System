"""Business rules and persistence operations for courses."""

from __future__ import annotations

from database.database import Database


class CourseService:
    """Provides validated CRUD operations for the ``courses`` table."""

    VALID_STATUSES = {"Active", "Inactive"}

    def __init__(self, database: Database | None = None):
        self.db = database or Database()
        # The service is also safe to use from a script before Application starts.
        self.db.create_tables()

    @staticmethod
    def _normalise_code(course_code: str) -> str:
        return "".join(course_code.strip().upper().split())

    @staticmethod
    def _normalise_name(course_name: str) -> str:
        return " ".join(course_name.strip().split())

    def _validate(self, course_code, course_name, duration_months,
                  total_semesters, annual_fee, status) -> dict:
        code = self._normalise_code(str(course_code))
        name = self._normalise_name(str(course_name))

        if not code:
            raise ValueError("Course code is required.")
        if len(code) > 20:
            raise ValueError("Course code must be 20 characters or fewer.")
        if not name:
            raise ValueError("Course name is required.")
        if len(name) > 120:
            raise ValueError("Course name must be 120 characters or fewer.")

        try:
            duration = int(duration_months)
            semesters = int(total_semesters)
            fee = float(annual_fee)
        except (TypeError, ValueError) as error:
            raise ValueError("Duration, semesters, and annual fee must be valid numbers.") from error

        if duration <= 0:
            raise ValueError("Duration must be greater than zero.")
        if semesters <= 0:
            raise ValueError("Number of semesters must be greater than zero.")
        if fee < 0:
            raise ValueError("Annual fee cannot be negative.")
        if status not in self.VALID_STATUSES:
            raise ValueError("Status must be Active or Inactive.")

        return {
            "course_code": code,
            "course_name": name,
            "duration_months": duration,
            "total_semesters": semesters,
            "annual_fee": fee,
            "status": status,
        }

    def course_exists(self, course_code: str, exclude_course_id: int | None = None) -> bool:
        query = "SELECT 1 FROM courses WHERE UPPER(course_code) = UPPER(?)"
        values: tuple = (self._normalise_code(course_code),)
        if exclude_course_id is not None:
            query += " AND course_id != ?"
            values += (exclude_course_id,)
        return self.db.fetchone(query, values) is not None

    def course_name_exists(self, course_name: str, exclude_course_id: int | None = None) -> bool:
        query = "SELECT 1 FROM courses WHERE LOWER(TRIM(course_name)) = LOWER(TRIM(?))"
        values: tuple = (self._normalise_name(course_name),)
        if exclude_course_id is not None:
            query += " AND course_id != ?"
            values += (exclude_course_id,)
        return self.db.fetchone(query, values) is not None

    def create_course(self, course_code, course_name, duration_months,
                      total_semesters, annual_fee, status) -> int:
        course = self._validate(course_code, course_name, duration_months,
                                total_semesters, annual_fee, status)
        if self.course_exists(course["course_code"]):
            raise ValueError("A course with this code already exists.")
        if self.course_name_exists(course["course_name"]):
            raise ValueError("A course with this name already exists.")

        return self.db.execute(
            """
            INSERT INTO courses (
                course_code, course_name, duration_months,
                total_semesters, annual_fee, status
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                course["course_code"], course["course_name"],
                course["duration_months"], course["total_semesters"],
                course["annual_fee"], course["status"],
            ),
        )

    def get_all_courses(self, search_text: str = "") -> list[dict]:
        query = """
            SELECT course_id, course_code, course_name, duration_months,
                   total_semesters, annual_fee, status
            FROM courses
        """
        values: tuple = ()
        search = search_text.strip()
        if search:
            term = f"%{search}%"
            query += """ WHERE course_code LIKE ? COLLATE NOCASE
                         OR course_name LIKE ? COLLATE NOCASE
                         OR status LIKE ? COLLATE NOCASE """
            values = (term, term, term)
        query += " ORDER BY course_name COLLATE NOCASE, course_code COLLATE NOCASE"
        return [dict(row) for row in self.db.fetchall(query, values)]

    def get_course(self, course_id: int) -> dict | None:
        row = self.db.fetchone(
            """SELECT course_id, course_code, course_name, duration_months,
                      total_semesters, annual_fee, status
               FROM courses WHERE course_id = ?""",
            (course_id,),
        )
        return dict(row) if row else None

    def update_course(self, course_id, course_code, course_name, duration_months,
                      total_semesters, annual_fee, status) -> None:
        if not self.get_course(course_id):
            raise ValueError("The selected course no longer exists.")
        course = self._validate(course_code, course_name, duration_months,
                                total_semesters, annual_fee, status)
        if self.course_exists(course["course_code"], course_id):
            raise ValueError("A course with this code already exists.")
        if self.course_name_exists(course["course_name"], course_id):
            raise ValueError("A course with this name already exists.")

        self.db.execute(
            """UPDATE courses
               SET course_code = ?, course_name = ?, duration_months = ?,
                   total_semesters = ?, annual_fee = ?, status = ?
               WHERE course_id = ?""",
            (
                course["course_code"], course["course_name"],
                course["duration_months"], course["total_semesters"],
                course["annual_fee"], course["status"], course_id,
            ),
        )

    def delete_course(self, course_id: int) -> None:
        if not self.get_course(course_id):
            raise ValueError("The selected course no longer exists.")
        self.db.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
