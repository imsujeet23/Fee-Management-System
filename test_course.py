from controllers.student_controller import StudentController

controller = StudentController()

courses = controller.get_courses()

print("Courses found:", len(courses))

for course in courses:
    print(course)