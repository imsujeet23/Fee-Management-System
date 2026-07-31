from controllers.course_controller import CourseController

controller = CourseController()

controller.add_course(
    "CS",
    "Computer Science",
    24,
    4,
    4500,
    "Active"
)

print(controller.get_courses())