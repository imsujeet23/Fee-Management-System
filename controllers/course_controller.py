"""Controller used by the Course Management page."""

from services.course_service import CourseService


class CourseController:
    def __init__(self, service: CourseService | None = None):
        self.service = service or CourseService()

    def add_course(self, code, name, duration, semesters, fee, status) -> int:
        return self.service.create_course(code, name, duration, semesters, fee, status)

    def get_courses(self, search_text: str = "") -> list[dict]:
        return self.service.get_all_courses(search_text)

    def get_course(self, course_id: int) -> dict | None:
        return self.service.get_course(course_id)

    def update_course(self, course_id, code, name, duration, semesters, fee, status) -> None:
        self.service.update_course(course_id, code, name, duration, semesters, fee, status)

    def delete_course(self, course_id: int) -> None:
        self.service.delete_course(course_id)
