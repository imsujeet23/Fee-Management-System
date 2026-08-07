from controllers.student_controller import StudentController

controller = StudentController()

print(controller.registration_number())

print()

for course in controller.get_courses():
    print(course["course_name"])