from services.student_service import StudentService


class StudentController:

    def __init__(self):
        self.service = StudentService()

    def registration_number(self):
        return self.service.generate_registration_no()

    def get_courses(self):
        return self.service.get_courses()

    def get_students(self):
        return self.service.get_students()