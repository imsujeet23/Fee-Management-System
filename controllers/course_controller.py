from services.course_service import CourseService


class CourseController:

    def __init__(self):
        self.service = CourseService()

    def add_course(
        self,
        code,
        name,
        duration,
        semesters,
        fee,
        status
    ):
        self.service.create_course(
            code,
            name,
            duration,
            semesters,
            fee,
            status
        )

    def get_courses(self):
        return self.service.get_all_courses()

    def delete_course(self, course_id):
        self.service.delete_course(course_id)